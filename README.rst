nifi-deploy
===========

|docs|


CLI tool for exporting and importing Nifi templates.


What it does
------------

* Export Process Groups as Nifi template XML
* Import Nifi template XML into Nifi as a template


What it's for
-------------

This tool stems from the need for a stricter governance for Nifi flow development.
``nifi-deploy`` is primarily aimed at a continuous integration pipeline for 
Nifi templates/general-usage Nifi flows.

This CLI tool wraps the great `NiPyAPI by Chaffelson <https://github.com/Chaffelson/nipyapi>`_ 
and enables developers to integrate version control of Nifi flows in their regular
workflow with VCS.



.. |docs| image:: https://readthedocs.org/projects/nifi-deploy/badge/?version=latest/
    :alt: Documentation Status
    :scale: 100%
    :target: https://readthedocs.io/projects/nifi-deploy/badge/
