/*
A utility for uploading HTML file sets to the KBase data stores.
*/

module HTMLFileSetUtils {

	/* A HTML file set as saved in the Workspace Service.
		file - a base64 encoded zip file containing HTML files.
	 */
	typedef structure {
		string file;
	} HTMLFileSet;

	/* Input to the upload_html_set function.
	
		Required arguments:
		One of:
		wsid - the id of the workspace where the reads will be saved
			(preferred).
		wsname - the name of the workspace where the reads will be saved.

		One of:
		objid - the id of the workspace object to save over
		name - the name to which the workspace object will be saved
		
		path - the path to the directory with the HTML files. This directory
			will be compressed and loaded into the KBase stores.
	 */
	typedef structure {
		int wsid;
		string wsname;
		int objid;
		string name;
		string path;
	} UploadHTMLSetInput;
	
	/* Output of the upload_html_set function.
	
		obj_ref - a reference to the new Workspace object in the form X/Y/Z,
			where X is the workspace ID, Y is the object ID, and Z is the
			version.
	 */
	typedef structure {
		string obj_ref;
	} UploadHTMLSetOutput;
	
	/* Upload an HTML file set to the KBase data stores. */
	funcdef upload_html_set(UploadHTMLSetInput params)
		returns(UploadHTMLSetOutput out) authentication required;
};
