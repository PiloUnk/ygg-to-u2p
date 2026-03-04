# YGG to U2P

Script Python pour ajouter automatiquement une liste de trackers publics à certains torrents dans qBittorrent.

## Pourquoi ce projet

Ce projet a été créé dans le contexte de la migration post-hack de l'écosystème Ygg, afin d'aider à maintenir les torrents disponibles via des trackers publics.

L'idée : ajouter une liste de trackers publics à vos torrents pour réduire la dépendance à un tracker unique.

## Ce que fait le script

Le script :

1. Charge une liste de trackers depuis `trackers.txt`
2. Se connecte à l'API Web de qBittorrent
3. Parcourt tous les torrents
4. Ne traite **que** les torrents qui possèdent déjà un tracker contenant `p2p-world.net` ou `maxp2p.org`
5. Ajoute uniquement les trackers manquants (pas de doublons)
6. Affiche un résumé final

## Prérequis

- Python 3.10+
- qBittorrent avec l'interface Web activée
- Accès API Web (hôte, login, mot de passe)

## Installation

1. Cloner / copier le projet
2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

Le fichier `requirements.txt` contient :

- `qbittorrent-api`
- `python-dotenv`

## Configuration

Le script lit des variables d'environnement (via `.env` si présent).

Créer un fichier `.env` à la racine :

```env
QB_HOST=http://localhost:8080
QB_USERNAME=admin
QB_PASSWORD=adminadmin
TRACKERS_FILE=trackers.txt
```

### Variables disponibles

- `QB_HOST` : URL de l'interface Web qBittorrent
- `QB_USERNAME` : utilisateur qBittorrent
- `QB_PASSWORD` : mot de passe qBittorrent
- `TRACKERS_FILE` : chemin du fichier de trackers

Si une variable est absente, le script utilise les valeurs par défaut montrées ci-dessus.

## Liste de trackers

La liste des trackers publics se trouve dans `trackers.txt`.

Règles de lecture :

- lignes vides ignorées
- lignes commençant par `#` ignorées

## Exécution

```bash
python main.py
```

Sortie attendue :

- connexion à qBittorrent
- nombre de torrents trouvés
- statut par torrent (`[MODIFIÉ]`, `[OK]`, `[IGNORÉ]`)
- résumé final

## Important

Le filtrage des torrents est actuellement basé sur les domaines :

- `p2p-world.net`
- `maxp2p.org`

Ces domaines sont définis en dur dans `main.py` via `TARGET_DOMAINS`.

Si vous voulez cibler d'autres domaines/anciens trackers, modifiez cette liste.

## Dépannage rapide

- **Erreur de connexion qBittorrent** : vérifier `QB_HOST`, `QB_USERNAME`, `QB_PASSWORD` et l'activation WebUI.
- **Fichier trackers introuvable** : vérifier `TRACKERS_FILE` et l'emplacement de `trackers.txt`.
- **Aucun tracker ajouté** : possible si les torrents ne contiennent ni `p2p-world.net` ni `maxp2p.org`, ou s'ils sont déjà à jour.
