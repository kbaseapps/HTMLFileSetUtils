# -*- coding: utf-8 -*-
import unittest
import time
import requests

from os import environ
import shutil
import os
import base64
import zipfile
try:
    from ConfigParser import ConfigParser  # py2 @UnusedImport
except:
    from configparser import ConfigParser  # py3 @UnresolvedImport @Reimport

from Workspace.WorkspaceClient import Workspace
from HTMLFileSetUtils.HTMLFileSetUtilsImpl import HTMLFileSetUtils
from HTMLFileSetUtils.HTMLFileSetUtilsServer import MethodContext
from DataFileUtil.baseclient import ServerError as DFUError
from WsLargeDataIO.baseclient import ServerError as WSIOError


class HTMLFileSetUtilsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token = environ.get('KB_AUTH_TOKEN', None)
        user_id = requests.post(
            'https://kbase.us/services/authorization/Sessions/Login',
            data='token={}&fields=user_id'.format(cls.token)).json()['user_id']
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': cls.token,
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
        obj_ref = self.impl.upload_html_set(
            self.ctx, {'wsname': self.ws_info[1],
                       'name': 'pants',
                       'path': tmp_dir})[0]['obj_ref']
        encf = self.ws.get_objects([{'ref': obj_ref}])[0]['data']['file']
        zipf = base64.b64decode(encf)
        tf = self.write_file('uploadtestout', zipf)
        with zipfile.ZipFile(tf) as z:
            self.assertEqual(set(z.namelist()),
                             set(['in1.txt', 'in2.txt']))

        # now that an object exists in the ws, can test with an object id
        self.write_file('uploadtest/in3.txt', 'tar3')
        obj_ref = self.impl.upload_html_set(
            self.ctx, {'wsid': self.ws_info[0],
                       'objid': 1,
                       'path': tmp_dir})[0]['obj_ref']
        encf = self.ws.get_objects([{'ref': obj_ref}])[0]['data']['file']
        zipf = base64.b64decode(encf)
        tf = self.write_file('uploadtestout', zipf)
        with zipfile.ZipFile(tf) as z:
            self.assertEqual(set(z.namelist()),
                             set(['in1.txt', 'in2.txt', 'in3.txt']))

    def test_upload_small_chunks(self):
        chz = HTMLFileSetUtils.CHUNKSIZE
        HTMLFileSetUtils.CHUNKSIZE = 3 * 31
        tmp_dir = os.path.join(self.cfg['scratch'], 'uploadtestsmall')
        os.makedirs(tmp_dir)
        self.write_file('uploadtestsmall/in1.txt', 'tar1')
        self.write_file('uploadtestsmall/in2.txt', 'tar2')
        obj_ref = self.impl.upload_html_set(
            self.ctx, {'wsname': self.ws_info[1],
                       'name': 'whee',
                       'path': tmp_dir})[0]['obj_ref']
        encf = self.ws.get_objects([{'ref': obj_ref}])[0]['data']['file']
        zipf = base64.b64decode(encf)
        tf = self.write_file('uploadtestsmallout', zipf)
        with zipfile.ZipFile(tf) as z:
            self.assertEqual(set(z.namelist()),
                             set(['in1.txt', 'in2.txt']))
        HTMLFileSetUtils.CHUNKSIZE = chz

    def test_fail_upload_no_ws_id(self):
        self.fail_upload(
            {}, 'Exactly one of the workspace ID or name must be provided')

    def test_fail_upload_bad_ws_name(self):
        self.fail_upload(
            {'wsname': 1}, 'wsname must be a string')

    def test_fail_upload_illegal_char_ws_name(self):
        self.fail_upload(
            {'wsname': 'foo*bar'},
            'Illegal character in workspace name foo*bar: *', DFUError)

    def test_fail_upload_both_ws_id(self):
        self.fail_upload(
            {'wsname': 'foo', 'wsid': 'bar'},
            'Exactly one of the workspace ID or name must be provided')

    def test_fail_upload_no_obj_id(self):
        self.fail_upload(
            {'wsid': self.ws_info[0]},
            'Exactly one of the object ID or name must be provided')

    def test_fail_upload_both_obj_id(self):
        self.fail_upload(
            {'wsid': self.ws_info[0], 'name': 'bar', 'objid': 'baz'},
            'Exactly one of the object ID or name must be provided')

    def test_fail_upload_no_path(self):
        self.fail_upload(
            {'wsid': self.ws_info[0], 'name': 'bar', 'path': ''},
            'path parameter is required')

    def test_fail_upload_root_path(self):
        self.fail_upload(
            {'wsid': self.ws_info[0], 'name': 'bar', 'path': '/'},
            'Packing root is not allowed', DFUError)

    def test_fail_upload_file_path(self):
        p = self.cfg['scratch'] + '/test_fail_upload_file_path'
        with open(p, 'w') as f:
            f.write('p')

        self.fail_upload(
            {'wsid': self.ws_info[0], 'name': 'bar', 'path': p},
            'path must be a directory')

    def test_fail_upload_big_zip(self):
        zsz = HTMLFileSetUtils.MAX_ZIP_SIZE
        HTMLFileSetUtils.MAX_ZIP_SIZE = 30
        tmp_dir = os.path.join(self.cfg['scratch'], 'uploadfailbig')
        os.makedirs(tmp_dir)
        self.write_file('uploadfailbig/in1.txt', 'tar1')
        self.write_file('uploadfailbig/in2.txt', 'tar2')

        self.fail_upload(
            {'wsid': self.ws_info[0], 'name': 'bar', 'path': tmp_dir},
            'Zipfile from specified directory is greater ' +
            'than maximum size allowed: 30')
        HTMLFileSetUtils.MAX_ZIP_SIZE = zsz

    def test_fail_upload_no_such_ws_id(self):
        tmp_dir = os.path.join(self.cfg['scratch'], 'uploadfailwsid')
        os.makedirs(tmp_dir)
        self.write_file('uploadfailwsid/in1.txt', 'tar1')
        self.write_file('uploadfailwsid/in2.txt', 'tar2')

        self.fail_upload(
            {'wsid': 1000000000000, 'name': 'bar', 'path': tmp_dir},
            'No workspace with id 1000000000000 exists', WSIOError)

    def fail_upload(self, params, error, exception=ValueError):
        with self.assertRaises(exception) as context:
            self.impl.upload_html_set(self.ctx, params)
        self.assertEqual(error, str(context.exception.message))
