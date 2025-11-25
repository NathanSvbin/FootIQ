<?php
include('../db.php');  // garde ton fichier de connexion existant

header("Content-Type: application/json; charset=UTF-8");

$sql = "
    SELECT 
        ch.Id AS id_championnat,
        ch.Nom AS nom_championnat,
        p.Nom AS nom_pays,
        co.Nom AS nom_continent
    FROM Championnat ch
    JOIN Pays p ON ch.Id_Pays = p.Id
    JOIN Continent co ON p.Id_Continent = co.Id
    ORDER BY 1;
";

$result = $conn->query($sql);

$championnats = [];

while ($row = $result->fetch_assoc()) {
    $championnats[] = [
        "id"        => $row["id_championnat"],
        "nom"       => $row["nom_championnat"],
        "pays"      => $row["nom_pays"],
        "continent" => $row["nom_continent"]
    ];
}

echo json_encode($championnats, JSON_UNESCAPED_UNICODE);
