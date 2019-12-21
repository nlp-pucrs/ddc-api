using System.IO;
using System.Net.Http;

namespace Post
{
    class Program
    {
        static void Main(string[] args)
        {
            using (var client = new HttpClient())
            using (var formData = new MultipartFormDataContent())
            {
                formData.Add(new StringContent("1"), "userid");
                formData.Add(new StreamContent(File.Open(@"..\data\test.csv.gz", FileMode.Open)), "file", "test.csv.gz");
                var tRequest = client.PostAsync("http://127.0.0.1:5000/score", formData);
                tRequest.Wait();
                if (tRequest.Result.IsSuccessStatusCode)
                {
                    var tBytes = tRequest.Result.Content.ReadAsByteArrayAsync();
                    tBytes.Wait();

                    File.WriteAllBytes(@"example.csv.gz", tBytes.Result);
                }
            }
        }
    }
}
