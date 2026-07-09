# -*- coding: utf-8 -*-
"""
PROJECT      : ALFRED
BLOCK        : B29
FUNCTION     : XX.XX
FILE         : scripts/run_hadoop_poc.py
ROLE         : Orchestre le job MapReduce du PoC Hadoop (upload HDFS, run, résultats)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-09
UPDATED      : 2026-07-09
VERSION      : V1.0
STATUS       : VALIDATED — exécuté avec succès le 09/07/2026

DESCRIPTION :
Prérequis : cluster démarré (`docker compose -f docker-compose.hadoop.yml
up -d`) et data/hadoop_poc/input/ peuplé (`python
scripts/anonymize_logs_for_hadoop.py`). Copie les fichiers anonymisés +
mapper/reducer dans le conteneur namenode, les charge dans HDFS, lance le
job Hadoop Streaming, puis rapatrie le résultat dans
data/hadoop_poc/output/result.tsv.

Usage :
    python scripts/run_hadoop_poc.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = ROOT / "data" / "hadoop_poc" / "input"
OUTPUT_DIR = ROOT / "data" / "hadoop_poc" / "output"
HADOOP_POC_DIR = ROOT / "hadoop_poc"
NAMENODE = "alfred_hadoop_namenode"

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        if check:
            sys.exit(result.returncode)
    return result


def main() -> None:
    if not any(INPUT_DIR.glob("*.jsonl")):
        print("Aucune donnée anonymisée trouvée — lance d'abord "
              "scripts/anonymize_logs_for_hadoop.py.")
        sys.exit(1)

    print("== 1. Copie des données et scripts dans le conteneur namenode ==")
    run(["docker", "exec", NAMENODE, "rm", "-rf", "/tmp/poc"])
    run(["docker", "exec", NAMENODE, "mkdir", "-p", "/tmp/poc/input"])
    run(["docker", "cp", str(INPUT_DIR) + "/.", f"{NAMENODE}:/tmp/poc/input"])
    run(["docker", "cp", str(HADOOP_POC_DIR / "mapper.py"), f"{NAMENODE}:/tmp/poc/mapper.py"])
    run(["docker", "cp", str(HADOOP_POC_DIR / "reducer.py"), f"{NAMENODE}:/tmp/poc/reducer.py"])

    print("\n== 2. Chargement dans HDFS ==")
    run(["docker", "exec", NAMENODE, "hdfs", "dfs", "-mkdir", "-p", "/poc/input"], check=False)
    run(["docker", "exec", NAMENODE, "hdfs", "dfs", "-rm", "-r", "-f", "/poc/output"], check=False)
    run([
        "docker", "exec", NAMENODE, "sh", "-c",
        "hdfs dfs -put -f /tmp/poc/input/*.jsonl /poc/input/",
    ])

    print("\n== 3. Job Hadoop Streaming (mapper.py | reducer.py) ==")
    streaming_jar_glob = (
        "$(find $HADOOP_HOME/share/hadoop/tools/lib -name 'hadoop-streaming*.jar' | head -1)"
    )
    run([
        "docker", "exec", NAMENODE, "sh", "-c",
        f"hadoop jar {streaming_jar_glob} "
        "-input /poc/input -output /poc/output "
        "-mapper 'python3 mapper.py' -reducer 'python3 reducer.py' "
        "-file /tmp/poc/mapper.py -file /tmp/poc/reducer.py",
    ])

    print("\n== 4. Rapatriement du résultat ==")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    run(["docker", "exec", NAMENODE, "sh", "-c", "hdfs dfs -cat /poc/output/part-* > /tmp/poc/result.tsv"])
    run(["docker", "cp", f"{NAMENODE}:/tmp/poc/result.tsv", str(OUTPUT_DIR / "result.tsv")])

    print(f"\nRésultat -> {OUTPUT_DIR / 'result.tsv'}")


if __name__ == "__main__":
    main()
