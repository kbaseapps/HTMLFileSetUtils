# -*- coding: utf-8 -*-
#BEGIN_HEADER
import six
from DataFileUtil.DataFileUtilClient import DataFileUtil
import os
import tempfile
import base64
from WsLargeDataIO.WsLargeDataIOClient import WsLargeDataIO
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
    GIT_COMMIT_HASH = "ae0cc4b030a8fecc464ca75a4e00fe984e8cc378"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = config['SDK_CALLBACK_URL']
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
           "obj_id" of String
        """
        # ctx is the context object
        # return variables are: returnVal
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
        if htmlpath == os.path.sep:
            raise ValueError("No, you can't zip up the root directory")
        if not os.path.isdir(htmlpath):
            raise ValueError('path must be a directory')
        zipfile = dfu.pack_file({'file_path': htmlpath, 'pack': 'zip'})
        tf = tempfile.mkstemp()
        with open(tf, 'w') as objfile, open(zipfile) as z:
            objfile.write('{"file":')
            base64.encode(z, tf)
            objfile.write('}')
        so = {'type': 'HtmlFileSetUtils.HtmlFileSet',
              'data_json_file': tf
              }
        if name:
            so['name'] = name
        else:
            so['objid'] = objid
        wsio = WsLargeDataIO(self.callback_url)
        ret = wsio.save_objects({'id': wsid,
                                 'objects': [so]
                                 })[0]
        out = {'obj_ref': str(ret[6]) + '/' + str(ret[0]) + '/' + str(ret[4])}
        #END upload_html_set

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method upload_html_set return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def status(self, ctx):
        #BEGIN_STATUS
        del ctx
        returnVal = {'state': "OK", 'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
