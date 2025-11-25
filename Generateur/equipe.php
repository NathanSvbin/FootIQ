<?php
include('../db.php');

$dir = __DIR__ . '/../Equipes/';
if (!is_dir($dir)) mkdir($dir, 0777, true);

// Fonction pour créer des noms de fichiers sûrs
function sanitize_filename($name) {
    $name = iconv('UTF-8', 'ASCII//TRANSLIT', $name);
    $name = preg_replace('/[^A-Za-z0-9_-]/', '_', $name);
    return $name;
}

// Récupération des équipes avec infos liées
$sql = "
    SELECT 
        e.Id, e.Nom AS nom_equipe,
        c.Nom AS nom_championnat,
        p.Nom AS nom_pays,
        co.Nom AS nom_continent
    FROM Equipe e
    JOIN Championnat c ON e.Id_Championnat = c.Id
    JOIN Pays p ON c.Id_Pays = p.Id
    JOIN Continent co ON p.Id_Continent = co.Id
";
$result = $conn->query($sql);

while ($row = $result->fetch_assoc()) {

    // 🔥 Récupération des joueurs
    $sql_joueurs = "SELECT Nom, Prenom FROM Joueurs WHERE Id_club = {$row['Id']} ORDER BY 1";
    $joueurs_result = $conn->query($sql_joueurs);

    // Génération du contenu HTML
    $content = "<!DOCTYPE html>
<html lang='fr'>
<head>
    <meta charset='UTF-8'>
    <title>{$row['nom_equipe']}</title>
    <style>
        body { font-family: Arial, sans-serif; background: #fafafa; padding: 40px; }
        .card { background: white; border-radius: 8px; padding: 20px; max-width: 700px; margin: auto; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { text-align: center; }
        p, li { font-size: 18px; }
        a { display: block; margin-top: 20px; text-align: center; color: #007bff; text-decoration: none; }
        h2 { margin-top: 30px; }
    </style>
</head>
<body>
    <div class='card'>
        <h1>{$row['nom_equipe']}</h1>
        <p><strong>Championnat :</strong> {$row['nom_championnat']}</p>
        <p><strong>Pays :</strong> {$row['nom_pays']}</p>
        <p><strong>Continent :</strong> {$row['nom_continent']}</p>
        <h2>Joueurs de l'équipe</h2>";

    if ($joueurs_result->num_rows > 0) {
        $content .= "<ul>";
        while ($j = $joueurs_result->fetch_assoc()) {
            $content .= "<li>" . htmlspecialchars($j['Prenom'] . " " . $j['Nom']) . "</li>";
        }
        $content .= "</ul>";
    } else {
        $content .= "<p>Aucun joueur dans cette équipe.</p>";
    }

    $content .= "<a href='../index.php'>← Retour à la liste</a>
    </div>
</body>
</html>";

    // Sauvegarde du fichier
    $filename = $dir . sanitize_filename($row['nom_equipe']) . '.html';
    file_put_contents($filename, $content);
}

echo "Pages équipes générées avec mise en page complète !\n";
