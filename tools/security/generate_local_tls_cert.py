"""
PROJECT      : ALFRED
BLOCK        : B24 — ALFRED Android / Compagnon mobile natif (durcissement API)
FUNCTION     : 24.03 — Certificat TLS local pour interface/companion_api.py
FILE         : tools/security/generate_local_tls_cert.py
ROLE         : Génère un certificat auto-signé (clé privée + certificat public)
               pour servir l'API compagnon en HTTPS sur le réseau local, sans
               dépendance externe (mkcert) ni domaine public (Let's Encrypt) —
               cohérent avec le principe local-first du projet.

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-14
VERSION      : V1.0
STATUS       : CODÉ — À TESTER (exécution manuelle + tests/b24_tests/test_companion_api_tls.py)

DESCRIPTION :
Certificat auto-signé RSA 2048 bits, validité 10 ans. Limitation assumée et
documentée : pas de rotation automatique (usage local personnel, pas un
service exposé publiquement) — cf. docs/mobilite/vision_mobilite_v2.md.
SAN couvre l'IP fixe du PC ALFRED sur VLAN 10 (192.168.10.100,
docs/smsi/vlan_config.md) + 127.0.0.1/localhost (usage direct sur le PC) +
10.0.2.2 (alias hôte pour l'émulateur Android).

Sortie : data/security/certs/companion_api/server.key (privé, JAMAIS commité,
cf. .gitignore) et server.crt (public — safe à committer, aussi copié tel
quel dans ALFRED_ANDROID/app/src/main/res/raw/alfred_pc_cert.pem comme ancre
de confiance côté client).

USAGE :
    python tools/security/generate_local_tls_cert.py
    (relancer uniquement si l'IP fixe du PC change, ou si la clé doit être
    régénérée — dans ce cas, republier aussi le .pem côté ALFRED_ANDROID et
    reconstruire l'app, sinon la confiance TLS échouera côté client)
"""

from __future__ import annotations

import datetime
import ipaddress
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "data" / "security" / "certs" / "companion_api"
KEY_PATH = CERT_DIR / "server.key"
CERT_PATH = CERT_DIR / "server.crt"

# IP fixe ALFRED_PC sur VLAN 10 (docs/smsi/vlan_config.md) + loopback +
# alias hôte émulateur Android (10.0.2.2 -> 127.0.0.1 du poste hôte).
SAN_IPS = ["192.168.10.100", "127.0.0.1", "10.0.2.2"]
SAN_DNS = ["localhost"]
VALIDITY_DAYS = 365 * 10


def generate(force: bool = False) -> tuple[Path, Path]:
    if CERT_PATH.exists() and KEY_PATH.exists() and not force:
        print(f"[ALFRED] Certificat déjà présent : {CERT_PATH} — rien à faire (force=True pour régénérer).")
        return CERT_PATH, KEY_PATH

    CERT_DIR.mkdir(parents=True, exist_ok=True)

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Cognitive Products Lab"),
            x509.NameAttribute(NameOID.COMMON_NAME, "ALFRED Companion API (local)"),
        ]
    )

    san_entries: list[x509.GeneralName] = [
        x509.IPAddress(ipaddress.ip_address(ip)) for ip in SAN_IPS
    ] + [x509.DNSName(dns) for dns in SAN_DNS]

    now = datetime.datetime.now(datetime.timezone.utc)
    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(days=1))
        .not_valid_after(now + datetime.timedelta(days=VALIDITY_DAYS))
        .add_extension(x509.SubjectAlternativeName(san_entries), critical=False)
        .add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_encipherment=True,
                content_commitment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .sign(private_key, hashes.SHA256())
    )

    KEY_PATH.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    CERT_PATH.write_bytes(certificate.public_bytes(serialization.Encoding.PEM))

    print(f"[ALFRED] Certificat généré : {CERT_PATH}")
    print(f"[ALFRED] Clé privée générée : {KEY_PATH} (ne jamais committer)")
    print(f"[ALFRED] SAN : {SAN_IPS + SAN_DNS}, validité {VALIDITY_DAYS} jours")
    return CERT_PATH, KEY_PATH


if __name__ == "__main__":
    import sys

    generate(force="--force" in sys.argv)
