=====
PYBBM Private Messages
=====

This is a plugin to add private messaging to the django forum solution `pybb`

Prerequisites:

1. `Django>=1.7`
2. `pybbm>=0.16`

Quick Start

1. `pip install pybbm-private-messages`
2. Add `private_messages` to your `INSTALLED_APPS` in `settings.py` BEFORE `pybb` (it overrides some templates)
3. Add the urls to your project `urls.py` file, e.g.:
    urlpatterns = [
        ...
        url(r'^forum/', include('pybb.urls', namespace='pybb')),
        url(r'^forum/', include('private_messages.urls', namespace='private_messages')),
    ]
