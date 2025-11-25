<?php
include('db.php');

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Fonction pour créer des noms de fichiers sûrs
function sanitize_filename($name) {
    $name = iconv('UTF-8', 'ASCII//TRANSLIT', $name);
    $name = preg_replace('/[^A-Za-z0-9_-]/', '_', $name);
    return $name;
}

if (!isset($_GET['query']) || empty(trim($_GET['query']))) {
    die("Veuillez entrer un terme de recherche.");
}

$term = $conn->real_escape_string($_GET['query']); // Sécurisé

// 🔹 Rechercher dans Equipe
$sql_equipes = "SELECT Nom FROM Equipe WHERE Nom LIKE '%$term%'";
// 🔹 Rechercher dans Joueurs
$sql_joueurs = "SELECT Nom, Prenom FROM Joueurs WHERE Nom LIKE '%$term%' OR Prenom LIKE '%$term%'";
// 🔹 Rechercher dans Championnat
$sql_championnats = "SELECT Nom FROM Championnat WHERE Nom LIKE '%$term%'";
// 🔹 Rechercher dans Pays
$sql_pays = "SELECT Nom FROM Pays WHERE Nom LIKE '%$term%'";

// Exécution
$result_equipes = $conn->query($sql_equipes);
$result_joueurs = $conn->query($sql_joueurs);
$result_championnats = $conn->query($sql_championnats);
$result_pays = $conn->query($sql_pays);
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Résultats pour "<?php echo htmlspecialchars($term); ?>"</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 40px; background: #fafafa; }
        .card { background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1, h2 { text-align: center; }
        ul { list-style: none; padding: 0; }
        li { font-size: 18px; margin: 5px 0; }
        a { text-decoration: none; color: #007bff; }
    </style>
</head>
<body>
    <h1>Résultats pour "<?php echo htmlspecialchars($term); ?>"</h1>

    <div class="card">
        <h2>Équipes</h2>
        <?php if ($result_equipes->num_rows > 0): ?>
            <ul>
                <?php while ($e = $result_equipes->fetch_assoc()): ?>
                    <li>
                        <a href="Equipes/<?php echo sanitize_filename($e['Nom']); ?>.html">
                            <?php echo htmlspecialchars($e['Nom']); ?>
                        </a>
                    </li>
                <?php endwhile; ?>
            </ul>
        <?php else: ?>
            <p>Aucune équipe trouvée.</p>
        <?php endif; ?>
    </div>

    <div class="card">
        <h2>Joueurs</h2>
        <?php if ($result_joueurs->num_rows > 0): ?>
            <ul>
                <?php while ($j = $result_joueurs->fetch_assoc()): ?>
                    <li>
                        <a href="Joueurs/<?php echo sanitize_filename($j['Prenom'] . '_' . $j['Nom']); ?>.html">
                            <?php echo htmlspecialchars($j['Prenom'] . ' ' . $j['Nom']); ?>
                        </a>
                    </li>
                <?php endwhile; ?>
            </ul>
        <?php else: ?>
            <p>Aucun joueur trouvé.</p>
        <?php endif; ?>
    </div>

    <div class="card">
        <h2>Championnats</h2>
        <?php if ($result_championnats->num_rows > 0): ?>
            <ul>
                <?php while ($c = $result_championnats->fetch_assoc()): ?>
                    <li>
                        <a href="Championnats/<?php echo sanitize_filename($c['Nom']); ?>.html">
                            <?php echo htmlspecialchars($c['Nom']); ?>
                        </a>
                    </li>
                <?php endwhile; ?>
            </ul>
        <?php else: ?>
            <p>Aucun championnat trouvé.</p>
        <?php endif; ?>
    </div>

    <div class="card">
        <h2>Pays</h2>
        <?php if ($result_pays->num_rows > 0): ?>
            <ul>
                <?php while ($p = $result_pays->fetch_assoc()): ?>
                    <li>
                        <a href="Pays/<?php echo sanitize_filename($p['Nom']); ?>.html">
                            <?php echo htmlspecialchars($p['Nom']); ?>
                        </a>
                    </li>
                <?php endwhile; ?>
            </ul>
        <?php else: ?>
            <p>Aucun pays trouvé.</p>
        <?php endif; ?>
    </div>
</body>
</html>
