# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.vary import vary_on_cookie
from pybb import defaults
from pybb.util import get_markup_engine
from pybb.views import PaginatorMixin

from private_messages.forms import MessageForm
from private_messages.models import PrivateMessage, MessageHandler, MessageThread

MarkupEngine = get_markup_engine()


class InboxView(PaginatorMixin, generic.ListView):
    paginate_by = defaults.PYBB_TOPIC_PAGE_SIZE
    context_object_name = 'message_list'
    template_name = 'pybb/private_messages/inbox.html'

    def get_queryset(self):
        return MessageThread.objects.filter(messages__receivers=self.request.user).distinct()

    @method_decorator(login_required)
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(InboxView, self).dispatch(request, *args, **kwargs)


class OutboxView(InboxView):

    def get_queryset(self):
        return MessageThread.objects.filter(messages__sender=self.request.user).distinct()


class MessageView(generic.DetailView):

    queryset = PrivateMessage.objects.all()
    template_name = 'pybb/private_messages/message.html'
    context_object_name = 'thread'
    http_method_names = ['get', ]

    @method_decorator(login_required)
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(MessageView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        message = super(MessageView, self).get_object(queryset)
        if message.sender != self.request.user:
            if self.request.user not in message.receivers.all():
                raise PermissionDenied
            handler = MessageHandler.objects.get(message=message, receiver=self.request.user)
            handler.read = True
            handler.save()
        thread = filter(None, [message.get_parent(), message])
        thread.extend(list(message.get_children()))
        return thread

    def get_context_data(self, **kwargs):
        ctx = super(MessageView, self).get_context_data(**kwargs)
        ctx['this_message'] = super(MessageView, self).get_object()
        return ctx


class SendMessageView(generic.CreateView):

    template_name = 'pybb/private_messages/new.html'
    form_class = MessageForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SendMessageView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        receivers = self.request.GET.getlist('to')
        parent_pk = self.request.GET.get('reply')
        reply_all = self.request.GET.get('all')
        if receivers:
            return {'receivers': receivers}
        if parent_pk:
            parent = get_object_or_404(PrivateMessage, pk=parent_pk)
            if self.request.user not in parent.receivers.all() and self.request.user != parent.sender:
                raise PermissionDenied
            body = MarkupEngine.quote(parent.body)
            initial = {
                'subject': reply_subject(parent.subject),
                'body': body,
                'receivers': [parent.sender],
                'parent': parent_pk
            }
            if reply_all == 'true':
                initial['receivers'] += parent.receivers.exclude(self.request.user)
            return initial

    def form_valid(self, form):
        parent_pk = form.cleaned_data['parent']
        if not parent_pk:
            thread = MessageThread.objects.create()
        else:
            try:
                parent = PrivateMessage.objects.get(pk=parent_pk)
            except PrivateMessage.NotFound:
                raise SuspiciousOperation
            thread = parent.thread
        self.object = PrivateMessage.objects.create(
            thread=thread,
            sender=self.request.user,
            sender_ip=self.request.META.get('REMOTE_ADDR', ''),
            subject=form.cleaned_data['subject'],
            body=form.cleaned_data['body'],
            )
        for receiver in form.cleaned_data['receivers']:
            MessageHandler.objects.create(message=self.object, receiver=receiver)

        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return self.object.get_absolute_url()


def reply_subject(string):
    if string.startswith('RE:'):
        return string
    return 'RE: ' + string
