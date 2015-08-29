# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from pybb.compat import get_user_model_path
from pybb.models import RenderableItem


class MessageHandler(models.Model):

    message = models.ForeignKey('PrivateMessage')
    receiver = models.ForeignKey(get_user_model_path())
    read = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)


class MessageThread(models.Model):

    @property
    def head(self):
        return self.messages.earliest()

    @property
    def tail(self):
        return self.messages.latest()

    def get_parent(self, message):
        assert message in self.messages.all(), "Cannot get parent of a message not in this thread"

        try:
            parent = message.thread.messages.filter(sent__lt=message.sent).latest()
        except PrivateMessage.DoesNotExist:
            return None
        return parent

    def get_children(self, message):
        assert message in self.messages.all(), "Cannot get parent of a message not in this thread"

        return message.thread.messages.filter(sent__gt=message.sent)



@python_2_unicode_compatible
class PrivateMessage(RenderableItem):

    class Meta(object):
        verbose_name = _('Private Message')
        verbose_name_plural = _('Private Messages')
        get_latest_by = 'sent'
        ordering = ['sent']

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sender = models.ForeignKey(get_user_model_path(),
                               related_name='sent_messages',
                               verbose_name=_('Sender'))
    sender_ip = models.IPAddressField(_('Sender IP'),
                                      blank=True,
                                      default='0.0.0.0')
    sent = models.DateTimeField(_('Sent'), auto_now_add=True, db_index=True)
    subject = models.CharField(max_length=100, blank=True, default='[No Subject]')
    receivers = models.ManyToManyField(get_user_model_path(),
                                       through='MessageHandler',
                                       related_name='recd_messages',
                                       verbose_name=_('Recipients'))
    # Expected behaviour when deleting a sent message is that the recipient still has their copy
    sender_deleted = models.BooleanField(default=False)
    thread = models.ForeignKey(MessageThread, related_name='messages')

    def __str__(self):
        return '{0} {1} {2}'.format(self.sender, _('Private Message'), self.uuid)

    def get_absolute_url(self):
        return reverse('private_messages:read_message', kwargs={'pk': self.uuid})

    def save(self, *args, **kwargs):
        self.render()
        super(PrivateMessage, self).save(*args, **kwargs)
