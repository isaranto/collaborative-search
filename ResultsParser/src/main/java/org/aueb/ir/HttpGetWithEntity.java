package org.aueb.ir;

/**
 * Created by mitsakos on 7/1/16.
 */

import org.apache.http.client.methods.HttpPost;

import java.net.URI;

public class HttpGetWithEntity extends HttpPost
{

    public final static String METHOD_NAME = "GET";

    public HttpGetWithEntity(URI url) {
        super(url);
    }

    public HttpGetWithEntity(String url) {
        super(url);
    }

    @Override
    public String getMethod() {
        return METHOD_NAME;
    }
}
