# -*- coding: utf-8 -*-
#BEGIN_HEADER
import six
from DataFileUtil.DataFileUtilClient import DataFileUtil
import os
import tempfile
import base64
from WsLargeDataIO.WsLargeDataIOClient import WsLargeDataIO
import time
#END_HEADER


class HTMLFileSetUtils:
    '''
    Module Name:
    HTMLFileSetUtils

    Module Description:
    A utility for uploading HTML file sets to the KBase data stores.
    '''

    ######## WARNING FOR GEVENT USERS #######
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    #########################################
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/mrcreosote/HTMLFileSetUtils"
    GIT_COMMIT_HASH = "1b944d4436faf3aa3dce235ff5aea1783493a0c4"

    #BEGIN_CLASS_HEADER
    MAX_ZIP_SIZE = 500000000

    # needs to be a multiple of 3 to handle b64 encoding correctly
    CHUNKSIZE = 3 * 300

    def log(self, message, prefix_newline=False):
        print(('\n' if prefix_newline else '') +
              str(time.time()) + ': ' + message)

    def xor(self, a, b):
        return bool(a) != bool(b)
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.scratch = config['scratch']
        #END_CONSTRUCTOR
        pass

    def upload_html_set(self, ctx, params):
        """
        Upload an HTML file set to the KBase data stores.
        :param params: instance of type "UploadHTMLSetInput" (Input to the
           upload_html_set function. Required arguments: One of: wsid - the
           id of the workspace where the reads will be saved (preferred).
           wsname - the name of the workspace where the reads will be saved.
           One of: objid - the id of the workspace object to save over name -
           the name to which the workspace object will be saved path - the
           path to the directory with the HTML files. This directory will be
           compressed and loaded into the KBase stores.) -> structure:
           parameter "wsid" of Long, parameter "wsname" of String, parameter
           "objid" of Long, parameter "name" of String, parameter "path" of
           String
        :returns: instance of type "UploadHTMLSetOutput" (Output of the
           upload_html_set function. obj_ref - a reference to the new
           Workspace object in the form X/Y/Z, where X is the workspace ID, Y
           is the object ID, and Z is the version.) -> structure: parameter
           "obj_ref" of String
        """
        # ctx is the context object
        # return variables are: out
        #BEGIN upload_html_set
        del ctx
        wsid = params.get('wsid')
        wsname = params.get('wsname')
        if not self.xor(wsid, wsname):
            raise ValueError(
                'Exactly one of the workspace ID or name must be provided')
        dfu = DataFileUtil(self.callback_url)
        if wsname:
            self.log('Translating workspace name to id')
            if not isinstance(wsname, six.string_types):
                raise ValueError('wsname must be a string')
            wsid = dfu.ws_name_to_id(wsname)
            self.log('translation done')
        del wsname
        objid = params.get('objid')
        name = params.get('name')
        if not self.xor(objid, name):
            raise ValueError(
                'Exactly one of the object ID or name must be provided')
        htmlpath = params.get('path')
        if not htmlpath:
            raise ValueError('path parameter is required')
        htmlpath = os.path.abspath(os.path.expanduser(htmlpath))
        if not os.path.isdir(htmlpath):
            raise ValueError('path must be a directory')
        zipfile = dfu.pack_file({'file_path': htmlpath,
                                 'pack': 'zip'})['file_path']
        if os.path.getsize(zipfile) > self.MAX_ZIP_SIZE:
            os.remove(zipfile)
            raise ValueError('Zipfile from specified directory is greater ' +
                             'than maximum size allowed: ' +
                             str(self.MAX_ZIP_SIZE))
        fh, tf = tempfile.mkstemp(dir=self.scratch)
        os.close(fh)
        with open(tf, 'w') as objfile, open(zipfile, 'rb') as z:
            objfile.write('{"file":"')
            d = z.read(self.CHUNKSIZE)
            while d:
                objfile.write(base64.b64encode(d))
                d = z.read(self.CHUNKSIZE)
            objfile.write('"}')
        os.remove(zipfile)
        so = {'type': 'HTMLFileSetUtils.HTMLFileSet-0.1',  # TODO release
              'data_json_file': tf
              }
        if name:
            so['name'] = name
        else:
            so['objid'] = objid
        wsio = WsLargeDataIO(self.callback_url, service_ver='dev')  # TODO remove dev @IgnorePep8
        ret = wsio.save_objects({'id': wsid,
                                 'objects': [so]
                                 })[0]
        os.remove(tf)
        out = {'obj_ref': str(ret[6]) + '/' + str(ret[0]) + '/' + str(ret[4])}
        #END upload_html_set

        # At some point might do deeper type checking...
        if not isinstance(out, dict):
            raise ValueError('Method upload_html_set return value ' +
                             'out is not type dict as required.')
        # return the results
        return [out]

    def status(self, ctx):
        #BEGIN_STATUS
        del ctx
        returnVal = {'state': "OK", 'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
