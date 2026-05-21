// ============================================================
// ALFRED_WEB - Premiere classe Java
// Semaine 4 : POO — Classe, Objet, Constructeur, Getters
// ============================================================

/**
 * LECON 1 : Classe Java
 * Une classe = un modele. Un objet = une instance du modele.
 */
public class Module {

    // LECON 2 : Attributs (variables de la classe)
    // "private" = encapsulation : on ne peut pas y acceder directement
    private int    id;
    private String nom;
    private String description;
    private boolean actif;

    // LECON 3 : Constructeur — initialise l'objet
    // Meme nom que la classe, pas de type de retour
    public Module(int id, String nom, String description) {
        this.id          = id;
        this.nom         = nom;
        this.description = description;
        this.actif       = true;  // actif par defaut
    }

    // LECON 4 : Getters — lire les attributs depuis l'exterieur
    public int     getId()          { return id; }
    public String  getNom()         { return nom; }
    public String  getDescription() { return description; }
    public boolean isActif()        { return actif; }

    // LECON 5 : Setters — modifier les attributs
    public void setNom(String nom)                 { this.nom = nom; }
    public void setDescription(String description) { this.description = description; }
    public void setActif(boolean actif)            { this.actif = actif; }

    // LECON 6 : Methode toString — afficher l'objet facilement
    @Override
    public String toString() {
        return String.format(
            "[Module #%d] %s — %s (actif: %s)",
            id, nom, description, actif ? "oui" : "non"
        );
    }

    // LECON 7 : Methode main — point d'entree du programme
    public static void main(String[] args) {

        System.out.println("=== ALFRED — Modules Java ===\n");

        // Creer des objets (instances de la classe Module)
        Module dashboard = new Module(1, "Dashboard",   "Interface principale ALFRED");
        Module securite  = new Module(2, "Securite",    "Module cybersecurite et logs");
        Module bdd       = new Module(3, "Base de donnees", "Gestion SQL ALFRED");

        // Afficher les modules
        System.out.println(dashboard);
        System.out.println(securite);
        System.out.println(bdd);

        // Modifier un attribut via setter
        bdd.setNom("BDD ALFRED");
        System.out.println("\nApres modification : " + bdd);

        // Acceder a un attribut via getter
        System.out.println("\nNom du module 1 : " + dashboard.getNom());
        System.out.println("Module actif ? " + dashboard.isActif());

        System.out.println("\n[ALFRED] Programme Java termine.");
    }
}

// ============================================================
// Pour compiler et executer (terminal Linux) :
//   javac Module.java
//   java Module
// ============================================================

// EXERCICES a faire (Semaine 4) :
// 1. Creer une classe "User" avec id, nom, email, role
// 2. Ajouter un constructeur avec tous les attributs
// 3. Creer 3 objets User et les afficher
// 4. Ajouter une methode "afficherInfos()" qui affiche tout proprement
