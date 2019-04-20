let request = require('request');
let fs = require('fs');

const options = {
  url: 'http://127.0.0.1:5000/score',
  headers: {
    'Content-Type': 'multipart/form-data'
  },
  formData : {
    'userid': 'hospital',
    'file' : fs.createReadStream('../../data/test.csv.gz')
  },
  encoding: null
};

request.post(options, function (err, res, body) {
  if(err) console.log(err);

  console.log('Response status: ', res.statusCode);

  if (res.statusCode === 200) {
    const fileName = 'output.csv.gz';
    fs.writeFileSync(fileName, body);
    console.log('File created: ', fileName);
  } 
});