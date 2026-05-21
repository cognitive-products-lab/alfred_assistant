<?php
// ============================================================
// ALFRED_WEB - Premier fichier PHP
// Semaine 6 : API REST + CRUD
// ============================================================

// LECON 1 : Variables en PHP (commence par $)
$nom_projet = "ALFRED";
$version    = "1.0";
$annee      = 2026;

// LECON 2 : echo = afficher du texte
echo "Bienvenue dans $nom_projet version $version\n";

// LECON 3 : Tableau (array)
$langages = ["Python", "SQL", "Java", "PHP", "HTML"];
echo "Langages : " . implode(", ", $langages) . "\n";

// LECON 4 : Condition if/else
$heure = date("H");
if ($heure < 12) {
    echo "Bonjour ! Bonne matinee.\n";
} elseif ($heure < 18) {
    echo "Bon apres-midi !\n";
} else {
    echo "Bonsoir !\n";
}

// LECON 5 : Fonction PHP
function bienvenue($nom) {
    return "Bonjour $nom, ALFRED est pret !";
}
echo bienvenue("Utilisateur") . "\n";

// ============================================================
// LECON 6 : API REST - retourner du JSON
// (Ce code simule un endpoint /api/users)
// ============================================================
header("Content-Type: application/json");

// Simulation de donnees (en vrai on ferait une requete SQL)
$users = [
    ["id" => 1, "nom" => "ALFRED",  "role" => "administrateur"],
    ["id" => 2, "nom" => "Dupont",  "role" => "utilisateur"],
    ["id" => 3, "nom" => "Martin",  "role" => "utilisateur"],
];

// Retourner les donnees en JSON
$reponse = [
    "status"  => "success",
    "total"   => count($users),
    "data"    => $users
];

echo json_encode($reponse, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);

// ============================================================
// LECON 7 : Connexion base de donnees MySQL (modele)
// ============================================================
/*
$pdo = new PDO(
    "mysql:host=localhost;dbname=alfred_db;charset=utf8",
    "alfred_user",
    "mot_de_passe_secret"
);

// Requete preparee (protection injection SQL)
$stmt = $pdo->prepare("SELECT * FROM users WHERE role = ?");
$stmt->execute(["utilisateur"]);
$users = $stmt->fetchAll(PDO::FETCH_ASSOC);
*/

// ============================================================
// EXERCICES a faire (Semaine 6)
// ============================================================
// 1. Creer une fonction qui retourne le carre d'un nombre
// 2. Creer un tableau de tes films preferes
// 3. Ajouter un parametre GET : $_GET['id'] pour filtrer un user
// 4. Creer un formulaire HTML qui envoie des donnees ici
?>
