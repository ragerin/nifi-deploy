"""
Provides a NifiInstance class facilitating easy to use
methods utilizing the NiPyApi (https://github.com/Chaffelson/nipyapi)
wrapper library.
"""

import os
import sys
import getpass
import requests

from nipyapi import nifi, config, templates, canvas

# Disable urllib3 certificate warnings
requests.packages.urllib3.disable_warnings()


class NifiInstance:
    """ The NifiInstance class facilitating easy to use
    methods utilizing the NiPyApi (https://github.com/Chaffelson/nipyapi)
    wrapper library.

    Arguments:
        url         (str): Nifi host url, defaults to environment variable `NIFI_HOST`.
        username    (str): Nifi username, defaults to environment variable `NIFI_USERNAME`.
        password    (str): Nifi password, defaults to environment variable `NIFI_PASSWORD`.
        verify_ssl  (bool): Whether to verify SSL connection - UNUSED as of now.

    """
    def __init__(self, url=None, username=None, password=None, verify_ssl=False):
        config.nifi_config.host = self._get_url(url)
        config.nifi_config.verify_ssl = verify_ssl
        config.nifi_config.username = username
        self._authenticate(username, password)


    def _get_url(self, url):
        if not url:
            try:
                url = os.environ['NIFI_HOST']
            except KeyError:
                url = input('Nifi host: ')
        if not '/nifi-api' in url:
            if not url[-1] == '/':
                url = url + '/'
            url = url + 'nifi-api'
        return url


    def _authenticate(self, username=None, password=None):
        if not username:
            try:
                config.nifi_config.username = os.environ['NIFI_USERNAME']
            except KeyError:
                config.nifi_config.username = input('Username: ')

        if not password:
            try:
                password = os.environ['NIFI_PASSWORD']
            except KeyError:
                password = getpass.getpass('Password: ')

        try:
            access_token = nifi.AccessApi().create_access_token(username=username,password=password)            
        except nifi.rest.ApiException as e:
            print("Exception when calling AccessApi->create_access_token: %s\n" % e)

        config.nifi_config.api_key[username] = access_token
        config.nifi_config.api_client = nifi.ApiClient(header_name='Authorization', header_value='Bearer {}'.format(access_token))        


    def create_template(self, pg_id, name, desc=''):
        """ Create a template from process group id.

        Arguments:
            pg_id   (str): Process group ID to create the template from.
            name    (str): Name of the template to create.
            desc    (str): Optional, description of the template to create.
        
        Returns:
            nipyapi.nifi.TemplateEntity 
        """

        template = templates.create_template(
            pg_id=pg_id,
            name=name,
            desc=desc
            )

        return template

    
    def delete_template(self, template_id):
        """ Delete a template from Nifi template registry.

        Arguments:
            template_id (str): ID of the template to delete.
        
        Returns:
            None
        """
        templates.delete_template(template_id)


    def export_template(self, template_id, file_path=None):
        """ Export a template as XML, and optionally write it to a file or stdout.

        Arguments:
            template_id (str): ID of the template to export.
            file_path   (str): Optional, path of file to write the XML to.
                               If `None`, write to stdout instead.
        
        Returns:
            requests.Response
        """

        # This implementation is a workaround for
        # https://github.com/Chaffelson/nipyapi/issues/42
        headers = {'Authorization':'Bearer {}'.format(config.nifi_config.api_key[config.nifi_config.username])}
        url = config.nifi_config.host + '/templates/' + template_id + '/download'
        response = requests.get(url, headers=headers, verify=config.nifi_config.verify_ssl)
        if file_path:
            file_path = file_path.strip('\'"')
            if os.path.isdir(file_path):
                file_path = os.path.join(file_path, 'template.xml')
            with open(file_path, 'w') as fd:
                fd.write(response.content.decode())
        else:
            sys.stdout.write(response.content.decode())

        return response
    

    def import_template(self, file_path):
        """ Imports a template XML into Nifi's template store.

        Arguments:
            file_path   (str): Path of the XML file to import into Nifi as a template.
        
        Returns:
            requests.Response
        """

        # This implementation is a workaround for
        # https://github.com/Chaffelson/nipyapi/issues/42
        file_path = file_path.strip('\'"')
        with open(file_path, 'r') as fd:
            filename = os.path.basename(fd.name)
            filedata = fd.read()
            
            files = {'template': (filename, filedata, 'text/xml')}
            headers = {'Authorization': 'Bearer {}'.format(config.nifi_config.api_key[config.nifi_config.username])}

            canvas_id = canvas.get_root_pg_id()            
            url = config.nifi_config.host + '/process-groups/' + canvas_id + '/templates/upload'
            response = requests.post(url, headers=headers, files=files, verify=config.nifi_config.verify_ssl)

        return response