Pré-production
==============

L’objectif de ce guide est de documenter la mise en place d’un serveur de pré-production.

Ce serveur permet de tester en ligne plusieurs branches du projet django, en les actualisant à chaque nouveau commit dans leur branche respective.

On suppose vouloir tester les branches `master` et `release`.

Différences avec le guide de déploiement pour Raspberry-PI
----------------------------------------------------------

* On clonera le dépot dans le dossier `edirtic.BRANCH`, autant de fois qu’il y a de branche à tester.
* On créera un dossier `home` contenant par exemple une page statique avec la liste des branches disponibles.

UWSGI
-----

`/etc/uwsgi/edirtic/master.ini` :

.. code::

  [uwsgi]
  
  uid = edirtic
  gid = edirtic
  
  chdir=/srv/http/edirtic/edirtic.master/edirtic
  
  env=DJANGO_SETTINGS_MODULE=edirtic.local_settings
  virtualenv=/srv/http/edirtic/edirtic.master/env
  plugin=python
  
  module=edirtic.wsgi:application
  master=True
  
  touch-reload=/srv/http/edirtic/edirtic.master/touch-to-reload
  
  max-requests=5000
  http-socket=127.0.0.1:8010

Pour les autres branches, on copie le fichier `master.ini` en `branche.ini`, on remplace `master` et on change le port `8010` par un autre.

TODO: Essayer d’utiliser des variables pour éviter à devoir copier le fichier.

Apache
------

Exemple avec `master` sur le port `8010` et `release` sur le port `8011`.

.. code::

  <VirtualHost *:80>
      ServerAdmin webmaster@edirtic.eu.org
      ServerName edirtic.eu.org
      DocumentRoot "/srv/http/edirtic/home"
      ErrorLog "/srv/http/edirtic/log/error.log"
      CustomLog "/srv/http/edirtic/log/access.log" combined
      <Location /master/>
          ProxyPass http://127.0.0.1:8010/
          ProxyPassReverse http://127.0.0.1:8010/master/
      </Location>
      <Location /release/>
          ProxyPass http://127.0.0.1:8011/
          ProxyPassReverse http://127.0.0.1:8011/release/
      </Location>
      Alias /static/ /srv/http/edirtic/static/
      <Directory /srv/http/edirtic/static/>
          Options -Indexes
          Require all granted
      </Directory>
  </VirtualHost>

Django
------

Par exemple pour la branche `master`, le dépot est cloné dans le dossier `~edirtic/edirtic.master`.
On placera le venv associé dans ce dossier (cf conf uwsgi) (ainsi on a un venv différent par branche).

Le fichier de configuration `local_settings.py` contient quelques paramètres spécifiques à ce déploiement dans un sous-dossier :

.. code::

  from .settings import *
  
  SECRET_KEY = "****************"
  
  DEBUG = False
  TEMPLATE_DEBUG = False
  
  ALLOWED_HOSTS = ['*']
  
  ADMINS = (
          ("EDIR TIC Team", "django@edirtic.eu.org"),
          )
  MANAGERS = ADMINS
  
  SERVER_EMAIL = 'django@edirtic.eu.org'
  DEFAULT_FROM_EMAIL = 'django@edirtic.eu.org'
  
  
  STATIC_ROOT = '/srv/http/edirtic/static/master'
  STATIC_URL = '/static/master/'
  
  FORCE_SCRIPT_NAME = '/master'
  LOGIN_REDIRECT_URL = FORCE_SCRIPT_NAME + LOGIN_REDIRECT_URL
  LOGIN_URL = FORCE_SCRIPT_NAME + '/accounts/login'
  
  EMAIL_SUBJECT_PREFIX = "[master] "
  
  LOGGING = {
      "version": 1,
      "disable_existing_loggers": False,
      'handlers': {
          'file': {
              'level': 'WARNING',
              'class': 'logging.FileHandler',
              'filename': '/srv/http/edirtic/log/debug.master.log',
          },
          'mail_admins': {
              'class': 'django.utils.log.AdminEmailHandler',
              'level': 'ERROR',
               # But the emails are plain text by default - HTML is nicer
              'include_html': True,
          },
      },
      'loggers': {
          'django.request': {
              'handlers': ['file', 'mail_admins'],
              'level': 'WARNING',
              'propagate': True,
          },
      },
  }

