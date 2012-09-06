==========================
Manual de Bones pràctiques
==========================

Aquest document exposa algunes de les bones pràctiques que es recomanen quan desenvolopeu el projecte Genweb.

PEP8
----

És important mantindre un codi d'estil unificat basat en l'estàndar Python PEP8. Aquest codi el podeu trobar a::

    http://www.python.org/dev/peps/pep-0008/

Hi han eines validadores de codi (linters) pels editors més comuns que validen PEP8, per exemple SublimeText2 te un plugin linter per PEP8.

Vistes
------

Genweb disposa del framework de desenvolupament Grok, que permet declarar vistes i viewlets de manera imperativa via Python sense necessitat de declarar-los via ZCML. Així es manté unificat el codi i la declaració de la vista.

En la mida de lo possible, utilitzarem Grok per totes les vistes i viewlets. En cas de haver de fer overrides, es farà via ZCML.
