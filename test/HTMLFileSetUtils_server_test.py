# -*- coding: utf-8 -*-
import unittest
import time
import requests

from os import environ
import shutil
import os
try:
    from ConfigParser import ConfigParser  # py2 @UnusedImport
except:
    from configparser import ConfigParser  # py3 @UnresolvedImport @Reimport

from Workspace.WorkspaceClient import Workspace  # @UnresolvedImport
from HTMLFileSetUtils.HTMLFileSetUtilsImpl import HTMLFileSetUtils
from HTMLFileSetUtils.HTMLFileSetUtilsServer import MethodContext


class HTMLFileSetUtilsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        user_id = requests.post(
            'https://kbase.us/services/authorization/Sessions/Login',
            data='token={}&fields=user_id'.format(token)).json()['user_id']
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'HTMLFileSetUtils',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('HTMLFileSetUtils'):
            cls.cfg[nameval[0]] = nameval[1]
        cls.ws = Workspace(cls.cfg['workspace-url'], token=cls.token)
        cls.impl = HTMLFileSetUtils(cls.cfg)
        suffix = int(time.time() * 1000)
        shutil.rmtree(cls.cfg['scratch'])
        os.mkdir(cls.cfg['scratch'])
        wsName = 'test_HTMLFileSetUtils_' + str(suffix)
        cls.ws_info = cls.ws.create_workspace({'workspace': wsName})

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'ws_info'):
            cls.ws.delete_workspace({'id': cls.ws_info[0]})
            print('Test workspace was deleted')

    def write_file(self, filename, content):
        tmp_dir = self.cfg['scratch']
        file_path = os.path.join(tmp_dir, filename)
        with open(file_path, 'w') as fh1:
            fh1.write(content)
        return file_path

    def test_upload(self):
        tmp_dir = os.path.join(self.cfg['scratch'], 'uploadtest')
        os.makedirs(tmp_dir)
        self.write_file('uploadtest/in1.txt', 'tar1')
        self.write_file('uploadtest/in2.txt', 'tar2')
        obj_ref = self.impl.upload_html_set({'wsname': self.ws_info[7],
                                             'name': 'pants',
                                             'path': tmp_dir})
        newobj = self.ws.get_objects([{'ref': obj_ref}])[0]['data']
        print(newobj)
        # TODO check contents
#         with tarfile.open(new_file_path) as t:
#             self.assertEqual(set(t.getnames()),
#                              set(['.', './intar1.txt', './intar2.txt']))
