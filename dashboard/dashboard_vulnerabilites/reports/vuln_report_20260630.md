# Rapport Vulnérabilités ALFRED — 2026-06-30

**Total** : 15 | Élevées : 2 | Modérées : 6 | Ouvertes : 2

- 🟡 `VULN-001` **Dépendances Python potentiellement obsolètes** — contrôlé
  _Packages Python susceptibles de contenir des CVE. Audit pip-audit configuré hebdomadairement._
  → Remédiation : pip-audit --fix automatique + gel requirements.txt versionné

- 🟡 `VULN-002` **Rate limiting insuffisant — formulaire contact** — en cours
  _Le formulaire de contact ne dispose pas de rate limiting strict. Risque de spam ou de bruteforce._
  → Remédiation : Implémenter Flask-Limiter — règle 5 req/min par IP

- 🟡 `VULN-003` **Content-Security-Policy — directive incomplète** — en cours
  _CSP partiellement configurée. Risque XSS résiduel si assets tiers chargés sans nonce._
  → Remédiation : Flask-Talisman : default-src 'self', script-src 'nonce-{random}', style-src 'self'

- 🟡 `VULN-004` **JWT — expiration et rotation des tokens** — contrôlé
  _JWT configurés avec expiration 24h. Rotation des refresh tokens implémentée. Blacklist active._
  → Remédiation : Maintenir expiration ≤24h, blacklist tokens révoqués en base, audit périodique

- 🟢 `VULN-005` **ChromaDB — accès local sans authentification** — accepté
  _ChromaDB accessible sur localhost:8000 uniquement. Pas d'exposition réseau. Risque limité à accès physique machine._
  → Remédiation : Risque résiduel acceptable — bind localhost + pare-feu OS + contrôle accès physique

- 🟢 `VULN-006` **Ollama API locale — port 11434 non authentifié** — contrôlé
  _Ollama écoute sur localhost:11434 sans token d'accès. Isolation réseau assurée par Zero Trust._
  → Remédiation : Bind localhost + règle iptables. Évolution : reverse proxy auth si exposition réseau future

- 🟠 `VULN-007` **Clés Fernet — absence de rotation automatique** — en cours
  _Les clés Fernet AES-256 ne font pas l'objet d'une rotation automatique programmée. Risque en cas de compromission silencieuse._
  → Remédiation : Script de rotation trimestrielle : génération nouvelle clé, re-chiffrement données, archivage ancienne clé

- 🟠 `VULN-008` **Backup — chiffrement et test de restauration** — contrôlé
  _Backups Fernet chiffrés sur disque F. Vérification intégrité hebdomadaire. Test restauration à planifier mensuellement._
  → Remédiation : Automatiser test restauration 1×/mois. Ajouter backup hors-site chiffré.

- 🟢 `VULN-009` **CSRF — protection formulaires Flask** — contrôlé
  _Flask-WTF CSRF tokens actifs sur tous les formulaires POST. Cookie SameSite=Lax configuré._
  → Remédiation : Upgrader SameSite=Strict si compatibilité confirmée. Maintenir Flask-WTF.

- 🟢 `VULN-010` **XSS — injection dans templates Jinja2** — contrôlé
  _Jinja2 auto-escaping actif par défaut. Variables utilisateur systématiquement échappées. |safe banni sur entrées utilisateur._
  → Remédiation : Maintenir auto-escape, revue de code interdisant |safe sur données non maîtrisées

- 🟢 `VULN-011` **Injection SQL — requêtes SQLite** — contrôlé
  _Toutes les requêtes SQLite utilisent des placeholders paramétrés. Aucune concaténation de chaîne SQL._
  → Remédiation : Maintenir usage des placeholders, ajouter sqlmap scan automatisé en CI/CD

- 🟢 `VULN-012` **TLS/HTTPS — certificat Let's Encrypt Render.com** — résolu
  _TLS géré automatiquement par Render.com (Let's Encrypt). Renouvellement auto. Score SSL Labs : A+._
  → Remédiation : Surveillance via Render dashboard. HSTS activé. Aucune action manuelle requise.

- 🟢 `VULN-013` **Variables d'environnement — exposition accidentelle** — contrôlé
  _ALFRED_SECRET_KEY, SMTP credentials, API keys stockées en .env — hors VCS (.gitignore). Render.com env panel sécurisé._
  → Remédiation : .gitignore actif, scan git-secrets en pré-commit hook, rotation clés si suspicion

- 🟡 `VULN-014` **Logs applicatifs — rétention et données personnelles** — ouvert
  _Les logs Flask contiennent des adresses IP et fragments de formulaire. Politique de rétention non formalisée. Risque RGPD Art. 5(1)(e)._
  → Remédiation : Anonymisation IP (masquage dernier octet), rétention max 90 jours, rotation log automatique

- 🟡 `VULN-015` **Pentest tiers qualifié PASSI — non réalisé** — ouvert
  _Aucun audit de sécurité externe qualifié PASSI n'a été réalisé. Démo pentest interne disponible sur le site, mais sans valeur de certification._
  → Remédiation : Budgéter audit PASSI (estimé 5-15K€). Cible : Q4 2026. Pré-requis : déploiement Docker ZAP Q3.

