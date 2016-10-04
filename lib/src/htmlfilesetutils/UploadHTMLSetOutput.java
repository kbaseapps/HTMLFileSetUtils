
package htmlfilesetutils;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: UploadHTMLSetOutput</p>
 * <pre>
 * Output of the upload_html_set function.
 *         obj_ref - a reference to the new Workspace object in the form X/Y/Z,
 *                 where X is the workspace ID, Y is the object ID, and Z is the
 *                 version.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "obj_id"
})
public class UploadHTMLSetOutput {

    @JsonProperty("obj_id")
    private String objId;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("obj_id")
    public String getObjId() {
        return objId;
    }

    @JsonProperty("obj_id")
    public void setObjId(String objId) {
        this.objId = objId;
    }

    public UploadHTMLSetOutput withObjId(String objId) {
        this.objId = objId;
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
        return ((((("UploadHTMLSetOutput"+" [objId=")+ objId)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
