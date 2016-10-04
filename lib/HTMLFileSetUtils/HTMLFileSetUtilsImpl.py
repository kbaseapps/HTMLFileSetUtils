# -*- coding: utf-8 -*-
#BEGIN_HEADER
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
        #END upload_html_set

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method upload_html_set return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK", 'message': "", 'version': self.VERSION, 
                     'git_url': self.GIT_URL, 'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
