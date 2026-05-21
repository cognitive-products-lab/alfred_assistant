-- ============================================================
-- ALFRED_WEB - Base de données principale
-- Semaine 1 : SQL Fondamental - CREATE TABLE + INSERT + SELECT
-- ============================================================

-- LECON 1 : Créer une table
-- Syntaxe : CREATE TABLE nom_table (colonne TYPE, ...)
CREATE TABLE IF NOT EXISTS users (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    nom       VARCHAR(100) NOT NULL,
    prenom    VARCHAR(100) NOT NULL,
    email     VARCHAR(200) NOT NULL UNIQUE,
    role      VARCHAR(50)  DEFAULT 'utilisateur',
    actif     BOOLEAN      DEFAULT 1,
    created_at DATETIME    DEFAULT CURRENT_TIMESTAMP
);

-- LECON 2 : Insérer des données
-- Syntaxe : INSERT INTO table (colonnes) VALUES (valeurs)
INSERT INTO users (nom, prenom, email, role) VALUES
    ('ALFRED', 'Admin', 'admin@alfred.local', 'administrateur'),
    ('Dupont', 'Marie', 'marie.dupont@alfred.local', 'utilisateur'),
    ('Martin', 'Lucas', 'lucas.martin@alfred.local', 'utilisateur');

-- LECON 3 : Lire les données
-- Syntaxe : SELECT colonnes FROM table WHERE condition
SELECT * FROM users;
SELECT nom, prenom, email FROM users WHERE role = 'administrateur';
SELECT COUNT(*) AS total_users FROM users;

-- ============================================================
-- TABLE DES MODULES (pour la suite du projet)
-- ============================================================
CREATE TABLE IF NOT EXISTS modules (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nom         VARCHAR(100) NOT NULL,
    description TEXT,
    actif       BOOLEAN DEFAULT 1,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO modules (nom, description) VALUES
    ('Dashboard', 'Interface principale ALFRED'),
    ('Sécurité', 'Module cybersécurité et logs'),
    ('Base de données', 'Gestion des données SQL');

-- ============================================================
-- EXERCICES A FAIRE (Semaine 1)
-- ============================================================
-- 1. Ajouter un utilisateur avec ton vrai prénom
-- 2. Afficher tous les utilisateurs actifs
-- 3. Mettre à jour un email : UPDATE users SET email='...' WHERE id=1;
-- 4. Supprimer un utilisateur : DELETE FROM users WHERE id=3;
