package org.aueb.ir;

/**
 * Created by mitsakos on 7/1/16.
 */

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.ResponseHandler;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Iterator;

public class ResultsParser
{
    public static void main(String[] args) throws Exception
    {
        try
        {
            BufferedReader br = new BufferedReader(new FileReader("../query-text"));

            PrintWriter out = new PrintWriter("results.test");

            String line;
            while ((line = br.readLine()) != null)
            {
                CloseableHttpClient httpClient = HttpClients.createDefault();
                HttpGetWithEntity httpget = new HttpGetWithEntity("http://83.212.119.231:9200/documents/doc/_search");

                String[] query = line.split(";");

                StringEntity input = new StringEntity("{ \"from\" : 0 , \"size\" : 500, \"query\": { \"multi_match\": { \"query\": \"" + query[1] + "\", \"fields\": [\"text^2\", \"relq^3\", \"note\"] } } }");

                input.setContentType("application/x-www-form-urlencoded");
                httpget.setEntity(input);

                System.out.println("Executing request " + httpClient.execute(httpget));
                // Create a custom response handler
                ResponseHandler<String> responseHandler = new ResponseHandler<String>()
                {

                    public String handleResponse(
                            final HttpResponse response) throws ClientProtocolException, IOException
                    {
                        int status = response.getStatusLine().getStatusCode();
                        if (status >= 200 && status < 300)
                        {
                            HttpEntity entity = response.getEntity();
                            return entity != null ? EntityUtils.toString(entity) : null;
                        }
                        else
                        {
                            throw new ClientProtocolException("Unexpected response status: " + status);
                        }
                    }

                };
                String responseBody = httpClient.execute(httpget, responseHandler);
                System.out.println("----------------------------------------");

                JSONParser parser = new JSONParser();
                JSONObject json = (JSONObject) parser.parse(responseBody);

                JSONArray msg = (JSONArray) ((JSONObject) json.get("hits")).get("hits");
                Iterator<JSONObject> iterator = msg.iterator();
                int counter = 1;
                while (iterator.hasNext())
                {
                    JSONObject result = (JSONObject) iterator.next();
                    //query_id    Q0    document_id    position    _score    STANDARD
                    out.println(query[0] + " Q0 " + result.get("_id") + " " + (counter++) + " " + result.get("_score") + " STANDARD");
                }

                httpClient.close();
                //System.out.println(responseBody);
            }
        }
        finally
        {
            //httpClient.close();
        }
    }

}
