# Skyroulette

Petit service FastAPI + bot Discord qui propose un "spin" pour ban temporairement un membre.

Installation
- Installer les dépendances :

```bash
pip install -r backend/requirements.txt
```

Configuration
- Créer un fichier `.env` dans `backend/` contenant au minimum :

- `DISCORD_TOKEN` : token du bot Discord
- `GUILD_ID` : identifiant du serveur (entier)
- `ALLOWED_ORIGIN` (optionnel) : origine autorisée pour les requêtes depuis le frontend, par ex. `http://localhost:8000`. Si défini, le serveur refusera les POST vers `/spin` provenant d'une autre origine.

Exécution
- Depuis la racine du projet :

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Le serveur FastAPI sert le frontend (route `/` et `/static`) et démarre le bot Discord en arrière-plan.

Endpoints principaux
- `POST /spin` : lance un spin si possible. Le serveur applique une vérification d'origine si `ALLOWED_ORIGIN` est configuré.
- `GET /status` : informations rapides (online, can_spin, history).
- `GET /history` : historique enrichi des spins.

Notes
- Le frontend est dans le dossier `frontend/` et est monté sur `/static`.
- Pour pinner des versions exactes, exécuter `pip freeze > backend/requirements.txt` dans un environnement contrôlé.
