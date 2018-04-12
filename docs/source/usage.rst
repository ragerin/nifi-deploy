Usage
=====

``nifi-deploy [-v] {export, import} [opts]``

Show help
"""""""""

.. code-block:: bash

    $ nifi-deploy --help
    $ nifi-deploy export --help   # Export specific help
    $ nifi-deploy import --help   # Import specific help


General parameters
""""""""""""""""""

=================== ======= ===========
Parameter           Alias   Description
=================== ======= ===========
``--version``       ``-v``  Outputs nifi-deploy version and exits without any other action  
=================== ======= ===========


Export parameters
"""""""""""""""""

.. code-block:: bash

    $ nifi-deploy export <uuid> <name> [-n <hostname>] [-u <username>] [-p <password>] [-d <description>] [-f <filename>] [-q] [-k]


===================  =======  ===========
Parameter            Alias    Description
===================  =======  ===========
``uuid``             ``n/a``  ``Required`` The UUID of a process group located on ``NIFI_HOST``
``name``             ``n/a``  ``Required`` The name of the exported template (as presented within the Nifi template repository
``--nifi_host``      ``-n``   Hostname of the Nifi server, where the `/nifi-api/` endpoint is hosted. If not supplied, nifi-deploy will look for the ``NIFI_HOST`` environment variable
``--username``       ``-u``   Username to authenticate as for the API request. If not supplied, nifi-deploy will look for the ``NIFI_USERNAME`` environment variable
``--password``       ``-p``   Password for the user. If not supplied, nifi-deploy will first look for the ``NIFI_PASSWORD`` environment variable. If not set, nifi-deploy will prompt for the password through the terminal (this requires direct user action)
``--description``    ``-d``   A description of the template to show within the Nifi template repository
``--filename``       ``-f``   Filename to write the template XML to
``--quiet``          ``-q``   Do not output anything, even if ``--filename`` is not supplied. Useful for automated tests
``--keep_template``  ``-k``   Retain the template in the Nifi template repository, after exporting
===================  =======  ===========


Import parameters
"""""""""""""""""

.. code-block:: bash

    $ nifi-deploy import <filename> [-n <hostname>] [-u <username>] [-p <password>]


===================  =======  ===========
Parameter            Alias    Description
===================  =======  ===========
``filename``         ``n/a``  Template XML file to upload as a template to the Nifi template repository
``--nifi_host``      ``-n``   Hostname of the Nifi server, where the `/nifi-api/` endpoint is hosted. If not supplied, nifi-deploy will look for the ``NIFI_HOST`` environment variable
``--username``       ``-u``   Username to authenticate as for the API request. If not supplied, nifi-deploy will look for the ``NIFI_USERNAME`` environment variable
``--password``       ``-p``   Password for the user. If not supplied, nifi-deploy will first look for the ``NIFI_PASSWORD`` environment variable. If not set, nifi-deploy will prompt for the password through the terminal (this requires direct user action)
===================  =======  ===========


Environment variables
"""""""""""""""""""""

For improved usability and even some security concerns, it may be beneficial to
set the following environment variables, instead of providing them at use-time:

=================  ===========
Variable           Description
=================  ===========
``NIFI_HOST``      Hostname of the Nifi-server, ending with the port-number and optionally `/nifi-api/`
``NIFI_USERNAME``  Username of the user authenticating with the API
``NIFI_PASSWORD``  If not set and not supplied as an argument parameter, will prompt as non-echoing input
=================  ===========


Exporting
"""""""""

Export a process group and output the XML to `stdout`:

.. code-block:: bash

    $ nifi-deploy export -n https://nifihost:9090 -u john -p badpractice 0a7361fd-015f-1000-ffff-ffffd2cbc7a7 my_great_template -d template description -f c:\\temp\\my_great_template_export.xml --keep_template

