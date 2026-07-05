# Architecture Documentation

Place simplified ALFRED architecture diagrams here.

## Réseau

[reseau_alfred.svg](reseau_alfred.svg) — Architecture réseau domestique ALFRED :
Internet → Bbox Must → ER605 (segmentation VLAN 10/PC_ALFRED, 20/ADMIN,
30/IOT) → switch TL-SG108E → postes finaux. État au 2026-07-05 : DMZ et
pare-feu WAN réalisés et testés, ACL inter-VLAN restantes. Détails et
procédures : `../smsi/vlan_config.md`, `../smsi/acces_distant_durcissement_wan.md`.

Confidentiel interne (IP et topologie détaillées) — ne pas publier tel quel.
