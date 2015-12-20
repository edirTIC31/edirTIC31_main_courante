API
===

Évènement
---------

* Base URL: ``/api/v1/evenement/``
* Allowed methods: GET

TODO: rajouter POST

Évènement (détails)
-------------------

* Base URL: ``/api/v1/evenement/<slug>/``
* Allowed methods: GET

Indicatifs
----------

* Base URL: ``/api/v1/indicatif/``
* Allowed methods: GET
* Filtering: ``evenement=<id>``

TODO: rajouter POST

Indicatifs (détails)
--------------------

* Base URL: ``/api/v1/indicatif/<pk>/``
* Allowed methods: GET

Messages
--------

* Base URL: ``/api/v1/message``
* Allowed methods: GET, POST (add)
* Filtering:

  * ``evenement=<id>`` (mandatory)
  * ``newer-than=<datetime>`` (format %Y-%m-%dT%H:%M:%S.%f, example: 2015-12-20T19:58:35.089133)

Messages (détails)
------------------

* Base URL: ``/api/v1/message/<pk>/``
* Allowed methods: GET, PUT (modify), DELETE

Lors d’une requête DELETE, il faut rajouter un paramètre GET ``reason``
donnant la raison de la suppression du message (*e.g.* ``DELETE /api/v1/message/42/?reason=intervention%20annulée``).
