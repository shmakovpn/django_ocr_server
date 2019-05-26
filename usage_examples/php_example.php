<?php
//Initialise the cURL var
$ch = curl_init();

//Get the response from cURL
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

//Set the Url
curl_setopt($ch, CURLOPT_URL, 'http://localhost:8000/upload/');

//Create a POST array with the file in it
$file='example.png';
$mime=getimagesize($file)['mime'];
$name=pathinfo($file)['basename'];
$postData = array(
    'file' => new CURLFile($file, $mime, $name),
);

curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);

// Execute the request
$response = curl_exec($ch);
echo($response);

curl_close ($ch);

?>
