# D&D Discord Bot - Question du Jour

Bot Discord qui publie chaque jour une question pour aider les joueurs à développer leurs personnages de jeu de rôle. Contient 365 questions uniques couvrant la personnalité, l'histoire, les relations et les préférences des personnages.

## Exemple de message

```
🎲 Question du jour #36

Les astres s'alignent et, sous la lumière des trois lunes, une question se dessine...

> Ton personnage a-t-il des phobies ? Lesquelles et quelle est leur intensité ?

🔮 Que révèle votre personnage ?
```

## Prérequis

- Python 3.10+
- Un bot Discord
- Un serveur Discord avec un channel dédié

## Installation

```bash
git clone <repo-url>
cd dnd-discord-bot
pip install -r requirements.txt
```

## Configuration

Copier `.env.example` vers `.env` et remplir les valeurs :

```
DISCORD_TOKEN=votre_token_ici
CHANNEL_ID=123456789012345678
```

### Créer le bot Discord

1. Aller sur https://discord.com/developers/applications
2. Créer une application > Bot > Reset Token > Copier le token
3. OAuth2 > URL Generator > Cocher `bot` et `Send Messages`
4. Inviter le bot avec l'URL générée

### Récupérer l'ID du channel

1. Discord > Paramètres > Avancés > Mode développeur
2. Clic droit sur le channel > Copier l'identifiant

## Utilisation

### Exécution manuelle

```bash
python bot.py
```

### Automatisation (cron)

Le bot est conçu pour s'exécuter une fois par jour via cron :

```
0 9 * * * /usr/bin/python3 /chemin/vers/bot.py
```

Le bot se connecte, envoie la question du jour, puis se déconnecte.

## Structure des questions

`questions.json` contient 365 questions organisées par mois :

```json
{
  "janvier": ["Question 1", "Question 2", ...],
  "fevrier": [...],
  ...
  "decembre": [...]
}
```

La question est sélectionnée automatiquement selon la date du jour.

## Fichiers

| Fichier | Description |
|---------|-------------|
| `bot.py` | Code du bot |
| `questions.json` | 365 questions / 1 question par jour |
| `requirements.txt` | Dépendances Python |
| `.env.example` | Template de configuration |
| `.env` | Configuration (à créer) |
