import os
import getpass
import requests

from nipyapi import nifi, config, templates, canvas

# Disable urllib3 certificate warnings
from urllib3 import disable_warnings
disable_warnings()






class NifiInstance:
    def __init__(self, url=None, username=None, password=None, verify_ssl=False):
        self.username = username
        config.nifi_config.host = self._get_url(url)
        config.nifi_config.verify_ssl = verify_ssl

        self.authenticate(username, password)


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


    def authenticate(self, username=None, password=None):
        # TODO: Attempt get username/password from env vars
        if not username:
            try:
                self.username = os.environ['NIFI_USERNAME']
            except KeyError:
                self.username = input('Username: ')

        if not password:
            try:
                password = os.environ['NIFI_PASSWORD']
            except KeyError:
                password = getpass.getpass('Password: ')

        try:
            access_token = nifi.AccessApi().create_access_token(username=username,password=password)
            config.nifi_config.api_key[username] = access_token
            config.nifi_config.api_client = nifi.ApiClient(header_name='Authorization', header_value='Bearer {}'.format(access_token))
            
        except nifi.rest.ApiException as e:
            print("Exception when calling AccessApi->create_access_token: %s\n" % e)


    def create_template(self, pg_id, name, desc=''):
        template = templates.create_template(
            pg_id=pg_id,
            name=name,
            desc=desc
            )
        return template
    

    def export_template(self, template_id, file_path=None):
        # This implementation is a workaround for
        # https://github.com/Chaffelson/nipyapi/issues/42
        from urllib3 import PoolManager, util
        con = PoolManager()
        headers = {'Authorization':'Bearer {}'.format(config.nifi_config.api_key[self.username])}
        url = config.nifi_config.host + '/templates/' + template_id + '/download'
        response = con.request('GET', url, headers=headers, preload_content=False)

        if file_path:
            file_path = file_path.strip('\'"')
            if os.path.isdir(file_path):
                file_path = os.path.join(file_path, 'template.xml')
            with open(file_path, 'w') as fd:
                fd.write(response.data.decode())

        return response.data.decode()
    

    def import_template(self, file_path=None):
        canvas_id = canvas.get_root_pg_id()
        file_path = file_path.strip('\'"')
        with open(file_path, 'r') as fd:
            filename = os.path.basename(fd.name)
            filedata = fd.read()
            
            files = {'template': (filename, filedata, 'text/xml')}
            headers = {'Authorization': 'Bearer {}'.format(config.nifi_config.api_key[self.username])}

            url = config.nifi_config.host + '/process-groups/' + canvas_id + '/templates/upload'

            response = requests.post(url, headers=headers, files=files, verify=config.nifi_config.verify_ssl)

            print(response.text)

            # print(response)
            # print(response.text)
            # print(response.data)

            # response = con.request('POST', url, headers=headers, field={
            #     'filefield':(filename, filedata, 'text/xml')
            # })
        