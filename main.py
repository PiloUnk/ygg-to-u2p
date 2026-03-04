import os
import sys
import qbittorrentapi
from dotenv import load_dotenv

load_dotenv()

QB_HOST           = os.getenv("QB_HOST", "http://localhost:8080")
QB_USERNAME       = os.getenv("QB_USERNAME", "admin")
QB_PASSWORD       = os.getenv("QB_PASSWORD", "adminadmin")
TRACKERS_FILE     = os.getenv("TRACKERS_FILE", "trackers.txt")
TARGET_DOMAIN     = "p2p-world.net"


def load_trackers(filepath: str) -> list[str]:
    if not os.path.exists(filepath):
        print(f"[ERREUR] Fichier introuvable : {filepath}")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        trackers = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

    if not trackers:
        print("[ERREUR] Le fichier de trackers est vide.")
        sys.exit(1)

    print(f"[INFO] {len(trackers)} tracker(s) chargé(s) depuis '{filepath}'")
    return trackers


def main():
    new_trackers = load_trackers(TRACKERS_FILE)

    client = qbittorrentapi.Client(
        host=QB_HOST,
        username=QB_USERNAME,
        password=QB_PASSWORD,
    )

    try:
        client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(f"[ERREUR] Connexion échouée : {e}")
        sys.exit(1)

    print(f"[INFO] Connecté à qBittorrent ({QB_HOST})")

    torrents = client.torrents_info()
    print(f"[INFO] {len(torrents)} torrent(s) trouvé(s)\n")

    updated   = 0
    skipped   = 0
    no_target = 0

    for torrent in torrents:
        # Récupère les URLs des trackers (on filtre les entrées internes **)
        tracker_urls = [
            t.url for t in torrent.trackers
            if t.url and not t.url.startswith("**")
        ]

        # Est-ce que ce torrent a un tracker p2p-world.net ?
        if not any(TARGET_DOMAIN in url for url in tracker_urls):
            print(f"[IGNORÉ]  {torrent.name} — pas de tracker {TARGET_DOMAIN}")
            no_target += 1
            continue

        # Trackers manquants uniquement
        current_set = set(tracker_urls)
        missing = [t for t in new_trackers if t not in current_set]

        if not missing:
            print(f"[OK]      {torrent.name} — déjà à jour")
            skipped += 1
            continue

        torrent.add_trackers(urls=missing)
        print(f"[MODIFIÉ] {torrent.name} — {len(missing)} tracker(s) ajouté(s)")
        updated += 1

    client.auth_log_out()

    print(f"\n--- Résumé ---")
    print(f"  Mis à jour          : {updated}")
    print(f"  Déjà à jour         : {skipped}")
    print(f"  Sans p2p-world.net  : {no_target}")


if __name__ == "__main__":
    main()