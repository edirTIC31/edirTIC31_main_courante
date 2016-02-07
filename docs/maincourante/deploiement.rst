Déploiement de la main courante
===============================

Ce petit guide indique comment déployer le projet Django ``edirtic`` sur une Raspberry-Pi.

NB: Les lignes de code commençant par ``#`` sont à éxécuter en root et celles par ``$`` par un utilisateur normal.

NB2: pour l'installation sous Odroid-C1 / Ubuntu, voir la fin du document

Installation de Raspbian
------------------------

* Télécharger `Raspbian Jessie Lite <https://downloads.raspberrypi.org/raspbian_lite_latest>`_.
* Dézipper le fichier :

.. code::

    $ unzip 2015-11-21-raspbian-jessie-lite.zip

* Copier l’image sur la carte SD (ici, celle-ci s’appelle ``mmcblk0``) :

.. code::

    $ sudo dd bs=4M if=2015-11-21-raspbian-jessie-lite.img of=/dev/mmcblk0

* S’assurer que toutes les données ont bien été écrite :

.. code::

    $ sync

* Retirer la carte SD puis la remettre pour provoquer une relecture des partitions par le noyau.

* Monter la deuxième partition :

.. code::

    $ sudo mount /dev/mmcblk0p2 /mnt

* Rajouter une clef ssh pour se connecter en tant que root :

.. code::

    $ sudo mkdir /mnt/root/.ssh
    $ sudo cp /home/<user>/.ssh/id_rsa.pub /mnt/root/.ssh/authorized_keys
    $ sudo umount /mnt


Configuration de Raspbian
-------------------------

* Se connecter à la raspberry pi en tant que root grâce à la clef ssh.

* La configurer: Étendre le système de fichier, mettre la locale fr_FR.UTF-8 et la timezone Europe/Paris, et éventuelle renseigner l’Hostname, puis la rebooter, avec :

.. code::

    # raspi-config


* La mettre à jour :

.. code::

    # apt-get update && apt-get dist-upgrade

* Installer quelques paquets :

.. code::

    # apt-get install git htop tmux vim python3-virtualenv \
                      uwsgi uwsgi-plugin-python3 apache2

* Créer un compte système ``edirtic`` :

.. code::

    # mkdir /srv/www
    # useradd -r edirtic -d /srv/www/edirtic -m

* Rajouter ``www-data`` au groupe ``edirtic`` :

.. code::

    # usermod -aG edirtic www-data

..

 Ceci permettera à *apache* de lire les fichiers statiques appartenant à *edirtic*.

* Créer le fichier ``~edirtic/.bashrc`` :

.. code::

    # su edirtic
    $ cd
    $ cat > .bashrc << EOF

    #
    # ~/.bashrc
    #

    # If not running interactively, don't do anything
    [[ $- != *i* ]] && return

    export EDITOR="vim"

    alias ls='ls --color=auto'
    alias ll='ls --color=auto -hl'
    alias l='ls --color=auto -al'

    alias rm='rm -i'
    alias cp='cp -i'
    alias mv='mv -i'

    PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '

    umask 0027

    export DJANGO_SETTINGS_MODULE=edirtic.rpi_settings

    . ~/venv/bin/activate

    EOF

* Cloner le dépôt git dans le dossier ``edirtic`` :

.. code::

    $ git clone --recursive https://github.com/edirTIC31/edirTIC31_main_courante ~/edirtic

Virtualenv
``````````

* Créer un *virtualenv* :

.. code::

    $ python3 -m virtualenv -p /usr/bin/python3 ~/venv

* Charger le *virtualenv* :

.. code::

    $ source ~/venv/bin/activate

..

 Il est également possible de se déconnecter puis de se réconnecter.
 Le *virtualenv* sera alors automatiquement activé grâce au ``.bashrc``.

* Installer les paquets python nécessaire :

.. code::

    $ pip3 install -U pip
    $ pip3 install -U -r ~/edirtic/django/requirements.txt

Django
``````

* Créer le dossier qui va contenir les paramètres secrets :

.. code::

    $ exit
    # mkdir -p /etc/django/edirtic/
    # chown edirtic:edirtic /etc/django/edirtic
    # chmod 755 /etc/django
    # chmod 750 /etc/django/edirtic
    # su edirtic

* Créer une secret key :

.. code::

    $ openssl rand -hex 16 > /etc/django/edirtic/SECRET_KEY

* Créer un dossier pour les logs Django et apache :

.. code::

    $ mkdir ~/log

* Créer la base de données et sa structure :

.. code::

    $ cd ~/edirtic/django/
    $ ./manage.py migrate

* Créer un super utilisateur :

.. code::

    $ ./manage.py createsuperuser

* Collecter les fichiers statiques :

.. code::

    $ ./manage.py collectstatic

..

  Ceux-ci sont placés dans le dossier ``~/static``.

uwsgi
`````

* Activer la configuration *uwsgi* :

.. code::

    $ touch ~/touch-to-reload
    $ exit
    # cd /etc/uwsgi/apps-enabled
    # ln -s /srv/www/edirtic/edirtic/conf/uwsgi.ini edirtic.ini

* Redémarrer *uwsgi* :

.. code::

    # systemctl restart uwsgi

* Vérifier les logs *uwsgi* :

.. code::

    # tail /var/log/uwsgi/app/edirtic.log

* Vérifier que *uwsgi* est bien lancé :

.. code::

    # ps aux | grep uwsgi

* Vérifier que çamarche™ :

.. code::

    # nc -v 127.0.0.1 8010
    Connection to 127.0.0.1 8010 port [tcp/*] succeeded!
    ^C

* Les logs Django se trouve dans le fichier ``~/log/debug.log``.

Apache
``````

* Copier la configuration *apache* :

.. code::

    # cd /etc/apache2/sites-enabled
    # rm 000-default.conf
    # ln -s /srv/www/edirtic/edirtic/conf/apache.conf edirtic.conf

* Créer le dossier ``/var/empty`` pour éviter un warning :

.. code::

    # mkdir /var/empty

* Activer les modules apache ``proxy`` et ``proxy_http`` :

.. code::

    # a2enmod proxy proxy_http
    # service apache2 restart
    
Installation de sous Odroid-C1/Ubuntu
-------------------------------------

Actuellement, la distribution Ubuntu est 14.04 LTS

L'installation décrite ci-dessus reste valable à l'exception de virtualenv et uwsgi.

* Pour installer virtualenv pour Python 3 qui passe par pip

.. code::

   # sudo apt-get install python3-pip
   # sudo pip3 install virtualenvwrapper
   
* Pour redémarrer uwsgi, on passe par init.d
   
.. code::

   # /etc/init.d/uwsgi restart
