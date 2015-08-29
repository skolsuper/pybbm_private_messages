=====
PYBBM Private Messages
=====

This is a plugin to add private messaging to the django forum solution `pybb`

Prerequisites:

1. `Django>=1.8`
2. `pybbm>=0.17`

Quick Start

1. `pip install pybbm-private-messages`
2. Add `private_messages` to your `INSTALLED_APPS` in `settings.py` BEFORE `pybb` (it overrides some templates)
3. Run `manage.py migrate private_messages`
4. Add the urls to your project `urls.py` file, e.g.:
```
    urlpatterns = [
        ...
        url(r'^forum/', include('pybb.urls', namespace='pybb')),
        url(r'^forum/', include('private_messages.urls', namespace='private_messages')),
    ]
```
4. Add `'private_messages.context_processors.unread_messages'` to your template context processors in settings.
5. Adding a `{% block private_messages %}{% endblock %}` to your `PYBB_TEMPLATE` will place a link to the inbox with the text: "Inbox" and a bootstrap badge adjacent to it with the number of unread messages, if there are any. For just the number of unread messages, use `{% block unread_msgs %}{% endblock %}`.
