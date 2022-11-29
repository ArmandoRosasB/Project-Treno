<?php
$distance = $_GET['dis'];
$estado = $_GET['est'];
$num_signal = $_GET['num'];

echo "La distancia es: ".$distance." <br>El estado del sensor es: ".$estado."<br>El numero de señal es: ".$num_signal."<br>";

$usuario = 'root';
$password = '';
$host = 'localhost';
$baseDeDatos = 'treno';

$link = mysqli_connect($host, $usuario, $password) or die ("No se ha posiso conectar al servidor de la base de datos");

$db = mysqli_select_db($link, $baseDeDatos) or die ("No se ha podido seleccionar la base de datos");

$fecha = time();

$device = 1258;
if($distance != 0){
    $query = "INSERT INTO Input (num_signal, created_at, device_key , distance, device_state) VALUES (".$num_signal.", ".$fecha.", ".$device.",".$distance.", ".$estado.")";
    $resultado = mysqli_query($link, $query);
}

?>