# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url

from private_messages.views import InboxView, MessageView, SendMessageView


urlpatterns = [
    url(r'^messages/$', InboxView.as_view(), name='inbox'),
    url(r'^messages/(?P<pk>[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15})/$', MessageView.as_view(), name='read_message'),
    url(r'^messages/new/$', SendMessageView.as_view(), name='send_message'),
]
