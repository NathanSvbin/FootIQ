<?php
$host = "db5018979326.hosting-data.io";
$user = "dbu2312522";
$pass = "Mana212972";
$dbname = "dbs14948470";

$conn = new mysqli($host, $user, $pass, $dbname);

if ($conn->connect_error) {
    die("Erreur de connexion : " . $conn->connect_error);
}
?>
