package htmlfilesetutils;

import java.io.File;
import java.util.LinkedHashMap;
import java.util.Map;
import us.kbase.auth.AuthToken;
import us.kbase.common.service.JsonServerMethod;
import us.kbase.common.service.JsonServerServlet;
import us.kbase.common.service.JsonServerSyslog;
import us.kbase.common.service.RpcContext;

//BEGIN_HEADER
//END_HEADER

/**
 * <p>Original spec-file module name: HTMLFileSetUtils</p>
 * <pre>
 * A utility for uploading HTML file sets to the KBase data stores.
 * </pre>
 */
public class HTMLFileSetUtilsServer extends JsonServerServlet {
    private static final long serialVersionUID = 1L;
    private static final String version = "0.0.1";
    private static final String gitUrl = "https://github.com/mrcreosote/HTMLFileSetUtils";
    private static final String gitCommitHash = "b6572a1105b328629760e57d18a947908837ab4c";

    //BEGIN_CLASS_HEADER
    //END_CLASS_HEADER

    public HTMLFileSetUtilsServer() throws Exception {
        super("HTMLFileSetUtils");
        //BEGIN_CONSTRUCTOR
        //END_CONSTRUCTOR
    }

    /**
     * <p>Original spec-file function name: upload_html_set</p>
     * <pre>
     * Upload an HTML file set to the KBase data stores.
     * </pre>
     * @param   params   instance of type {@link htmlfilesetutils.UploadHTMLSetInput UploadHTMLSetInput}
     * @return   instance of type {@link htmlfilesetutils.UploadHTMLSetOutput UploadHTMLSetOutput}
     */
    @JsonServerMethod(rpc = "HTMLFileSetUtils.upload_html_set", async=true)
    public UploadHTMLSetOutput uploadHtmlSet(UploadHTMLSetInput params, AuthToken authPart, RpcContext jsonRpcContext) throws Exception {
        UploadHTMLSetOutput returnVal = null;
        //BEGIN upload_html_set
        //END upload_html_set
        return returnVal;
    }
    @JsonServerMethod(rpc = "HTMLFileSetUtils.status")
    public Map<String, Object> status() {
        Map<String, Object> returnVal = null;
        //BEGIN_STATUS
        returnVal = new LinkedHashMap<String, Object>();
        returnVal.put("state", "OK");
        returnVal.put("message", "");
        returnVal.put("version", version);
        returnVal.put("git_url", gitUrl);
        returnVal.put("git_commit_hash", gitCommitHash);
        //END_STATUS
        return returnVal;
    }

    public static void main(String[] args) throws Exception {
        if (args.length == 1) {
            new HTMLFileSetUtilsServer().startupServer(Integer.parseInt(args[0]));
        } else if (args.length == 3) {
            JsonServerSyslog.setStaticUseSyslog(false);
            JsonServerSyslog.setStaticMlogFile(args[1] + ".log");
            new HTMLFileSetUtilsServer().processRpcCall(new File(args[0]), new File(args[1]), args[2]);
        } else {
            System.out.println("Usage: <program> <server_port>");
            System.out.println("   or: <program> <context_json_file> <output_json_file> <token>");
            return;
        }
    }
}
