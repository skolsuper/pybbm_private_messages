# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    replaces = [(b'private_messages', '0001_initial'), (b'private_messages', '0002_auto_20150826_1413'), (b'private_messages', '0003_auto_20150828_1434'), (b'private_messages', '0004_auto_20150828_1520')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageHandler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('read', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PrivateMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField(verbose_name='Message')),
                ('body_html', models.TextField(verbose_name='HTML version')),
                ('body_text', models.TextField(verbose_name='Text version')),
                ('sender_ip', models.IPAddressField(default='0.0.0.0', verbose_name='Sender IP', blank=True)),
                ('sent', models.DateTimeField(auto_now_add=True, verbose_name='Sent', db_index=True)),
                ('subject', models.CharField(default='[No Subject]', max_length=100, blank=True)),
                ('sender_deleted', models.BooleanField(default=False)),
                ('receivers', models.ManyToManyField(related_name='inbox', verbose_name='Recipients', through='private_messages.MessageHandler', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='outbox', verbose_name='Sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Private Message',
                'verbose_name_plural': 'Private Messages',
            },
        ),
        migrations.AddField(
            model_name='messagehandler',
            name='message',
            field=models.ForeignKey(to='private_messages.PrivateMessage'),
        ),
        migrations.AddField(
            model_name='messagehandler',
            name='receiver',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterModelOptions(
            name='privatemessage',
            options={'ordering': ['sent'], 'get_latest_by': 'sent', 'verbose_name': 'Private Message', 'verbose_name_plural': 'Private Messages'},
        ),
        migrations.RemoveField(
            model_name='privatemessage',
            name='id',
        ),
        migrations.AddField(
            model_name='privatemessage',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True),
        ),
        migrations.CreateModel(
            name='MessageThread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AlterField(
            model_name='privatemessage',
            name='receivers',
            field=models.ManyToManyField(related_name='recd_messages', verbose_name='Recipients', through='private_messages.MessageHandler', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='privatemessage',
            name='sender',
            field=models.ForeignKey(related_name='sent_messages', verbose_name='Sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='privatemessage',
            name='thread',
            field=models.ForeignKey(related_name='messages', default=1, to='private_messages.MessageThread'),
            preserve_default=False,
        ),
    ]