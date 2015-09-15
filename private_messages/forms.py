# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from django_select2.fields import HeavyModelSelect2MultipleChoiceField

from pybb import defaults, util
from private_messages.models import PrivateMessage
from private_messages.views import ReceiversSelect2View


class MessageForm(forms.ModelForm):

    parent = forms.UUIDField(required=False, widget=forms.HiddenInput)
    receivers = HeavyModelSelect2MultipleChoiceField(data_view=ReceiversSelect2View)

    class Meta(object):
        model = PrivateMessage
        fields = ('receivers', 'subject', 'body', 'parent')
        widgets = {
            'body': util.get_markup_engine().get_widget_cls(),
        }
        labels = {
            'receivers': _('To'),
        }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.available_smiles = defaults.PYBB_SMILES
        self.smiles_prefix = defaults.PYBB_SMILES_PREFIX
