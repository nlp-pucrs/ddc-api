// Ubuntu instalation
// sudo apt install default-jdk 
// Tutorial: https://www.techcoil.com/blog/how-to-upload-a-file-via-a-http-multipart-request-in-java-without-using-any-external-libraries/
// WARNING: Example still not working

import java.io.DataOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

public class example {

    public static void main(String[] args) throws Exception {

		URL url = new URL("http://127.0.0.1:5000/score");
		HttpURLConnection con = (HttpURLConnection) url.openConnection();
		con.setRequestMethod("POST");
		con.addRequestProperty("Content-Type", "multipart/form-data;");
        con.setDoOutput(true);
        con.setDoInput(true);

		con.connect();

		OutputStream output = con.getOutputStream();
		DataOutputStream writer = new DataOutputStream(output);
		String post = "userid=hospital";
		writer.writeBytes(post);

        File gzippedData = new File("../data/test.csv.gz");
        FileInputStream input = new FileInputStream(gzippedData);

		int bytesRead;
		byte[] dataBuffer = new byte[1024];
		while((bytesRead = input.read(dataBuffer)) != -1) {
		    output.write(dataBuffer, 0, bytesRead);
		}
		output.flush();

		System.out.println(con.getResponseCode());
		BufferedReader resultado = new BufferedReader(
                new InputStreamReader(con.getInputStream()));

		con.disconnect();

    }

}

