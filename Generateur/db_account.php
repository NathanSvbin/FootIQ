<?php
// Informations de connexion
$host = "db5018979326.hosting-data.io";
$dbname = "dbs14948470";
$user = "dbu2312522";
$pass = "Mana212972";

try {
    // Création de la connexion PDO
    $pdo_account = new PDO(
        "mysql:host=$host;dbname=$dbname;charset=utf8",
        $user,
        $pass,
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false
        ]
    );
} catch (PDOException $e) {
    die("Erreur de connexion : " . $e->getMessage());
}
?>