
package us.kbase.htmlfilesetutils;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: UploadHTMLSetInput</p>
 * <pre>
 * Input to the upload_html_set function.
 *         Required arguments:
 *         One of:
 *         wsid - the id of the workspace where the reads will be saved
 *                 (preferred).
 *         wsname - the name of the workspace where the reads will be saved.
 *         One of:
 *         objid - the id of the workspace object to save over
 *         name - the name to which the workspace object will be saved
 *         
 *         path - the path to the directory with the HTML files. This directory
 *                 will be compressed and loaded into the KBase stores.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "wsid",
    "wsname",
    "objid",
    "name",
    "path"
})
public class UploadHTMLSetInput {

    @JsonProperty("wsid")
    private Long wsid;
    @JsonProperty("wsname")
    private String wsname;
    @JsonProperty("objid")
    private Long objid;
    @JsonProperty("name")
    private String name;
    @JsonProperty("path")
    private String path;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("wsid")
    public Long getWsid() {
        return wsid;
    }

    @JsonProperty("wsid")
    public void setWsid(Long wsid) {
        this.wsid = wsid;
    }

    public UploadHTMLSetInput withWsid(Long wsid) {
        this.wsid = wsid;
        return this;
    }

    @JsonProperty("wsname")
    public String getWsname() {
        return wsname;
    }

    @JsonProperty("wsname")
    public void setWsname(String wsname) {
        this.wsname = wsname;
    }

    public UploadHTMLSetInput withWsname(String wsname) {
        this.wsname = wsname;
        return this;
    }

    @JsonProperty("objid")
    public Long getObjid() {
        return objid;
    }

    @JsonProperty("objid")
    public void setObjid(Long objid) {
        this.objid = objid;
    }

    public UploadHTMLSetInput withObjid(Long objid) {
        this.objid = objid;
        return this;
    }

    @JsonProperty("name")
    public String getName() {
        return name;
    }

    @JsonProperty("name")
    public void setName(String name) {
        this.name = name;
    }

    public UploadHTMLSetInput withName(String name) {
        this.name = name;
        return this;
    }

    @JsonProperty("path")
    public String getPath() {
        return path;
    }

    @JsonProperty("path")
    public void setPath(String path) {
        this.path = path;
    }

    public UploadHTMLSetInput withPath(String path) {
        this.path = path;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((("UploadHTMLSetInput"+" [wsid=")+ wsid)+", wsname=")+ wsname)+", objid=")+ objid)+", name=")+ name)+", path=")+ path)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
