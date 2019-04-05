<?php

# Ubuntu PHP Instalation
# sudo apt install php7.2-cli
# sudo apt install php7.2-curl

$url = 'http://127.0.0.1:5000/score';
$cFile = curl_file_create('../data/test.csv.gz');
$post = array('userid' => 'hospital','file'=> $cFile);

$curl = curl_init();
curl_setopt($curl, CURLOPT_POST, 1);
curl_setopt($curl, CURLOPT_POSTFIELDS, $post);
curl_setopt($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
$result = curl_exec($curl);
curl_close($curl);

file_put_contents('example.csv.gz', $result, FILE_BINARY);