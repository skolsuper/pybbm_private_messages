# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from django_select2.fields import HeavyModelSelect2MultipleChoiceField
from pybb import util

from private_messages.models import PrivateMessage

User = get_user_model()


class MessageForm(forms.ModelForm):

    parent = forms.UUIDField(required=False, widget=forms.HiddenInput)
    receivers = HeavyModelSelect2MultipleChoiceField(
        data_view='private_messages:receivers_json', queryset=User.objects.all())

    class Meta(object):
        model = PrivateMessage
        fields = ('receivers', 'subject', 'body', 'parent')
        widgets = {
            'body': util.get_markup_engine().get_widget_cls(),
        }
        labels = {
            'receivers': _('To'),
        }
