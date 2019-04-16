// Ubuntu instalation
// sudo apt install default-jdk 
// You can make this code simpler if you use a lib like HttpClient (https://hc.apache.org/httpcomponents-client-ga/index.html)
// examples at: https://www.baeldung.com/httpclient-post-http-request (POST Multipart Request)

import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Example {

	private static final String CRLF = "\r\n";
	private static final String CHARSET = StandardCharsets.UTF_8.name();

	public static void main(String[] args) throws Exception {
		String url = "http://127.0.0.1:5000/score";
		String uploadFilePath = "../data/test.csv.gz";
		String outputFilePath = "output.csv.gz";

		File binaryFile = new File(uploadFilePath);
		String boundary = Long.toHexString(System.currentTimeMillis());

		URLConnection connection = new URL(url).openConnection();
		connection.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);
		connection.setDoOutput(true);

		try (
			OutputStream output = connection.getOutputStream();
			PrintWriter writer = new PrintWriter(new OutputStreamWriter(output, CHARSET), true);
		) {
			// add userid
			addString(writer, boundary, "userid", "hospital");

			// add file
			addFile(writer, output, boundary, "file", binaryFile);

			writer.append("--" + boundary + "--").append(CRLF).flush();
		}

		Files.copy(((HttpURLConnection) connection).getInputStream(), Paths.get(outputFilePath));
		System.out.println("Response code: " + ((HttpURLConnection) connection).getResponseCode());
		System.out.println("Response content: " + outputFilePath);
	}

	private static void addString(PrintWriter writer, String boundary, String paramKey, String paramValue) {
		writer.append("--" + boundary).append(CRLF);
		writer.append("Content-Disposition: form-data; name=\"" + paramKey + "\"").append(CRLF);
		writer.append("Content-Type: text/plain; charset=" + CHARSET).append(CRLF);
		writer.append(CRLF).append(paramValue).append(CRLF).flush();
	}

	private static void addFile(PrintWriter writer, OutputStream output, String boundary, String paramKey,
			File binaryFile) throws IOException {
		writer.append("--" + boundary).append(CRLF);
		writer.append(
			"Content-Disposition: form-data; name=\"" + paramKey + "\"; filename=\"" + binaryFile.getName() + "\""
		).append(CRLF);
		writer.append("Content-Type: " + URLConnection.guessContentTypeFromName(binaryFile.getName())).append(CRLF);
		writer.append("Content-Transfer-Encoding: binary").append(CRLF);
		writer.append(CRLF).flush();

		Files.copy(binaryFile.toPath(), output);
		output.flush();

		writer.append(CRLF).flush();
	}
	
}
