# -*- coding: utf-8 -*-
"""
Bot Discord - Question du jour (version cron)
S'exécute une fois, envoie la question du jour correspondant à la date actuelle.
À lancer via cron : 0 9 * * * /usr/bin/python3 /path/to/bot.py
"""

import asyncio
import json
import os
import logging
from datetime import datetime
from pathlib import Path

import discord
from dotenv import load_dotenv

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Chargement des variables d'environnement
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Validation des variables d'environnement
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN manquant dans le fichier .env")
if not CHANNEL_ID:
    raise ValueError("CHANNEL_ID manquant dans le fichier .env")

CHANNEL_ID = int(CHANNEL_ID)

# Chemin vers le fichier de questions
QUESTIONS_FILE = Path(__file__).parent / "questions.json"

# Mapping des mois en français
MONTHS_FR = {
    1: "janvier",
    2: "fevrier",
    3: "mars",
    4: "avril",
    5: "mai",
    6: "juin",
    7: "juillet",
    8: "aout",
    9: "septembre",
    10: "octobre",
    11: "novembre",
    12: "decembre"
}


def load_questions() -> dict:
    """Charge les questions depuis le fichier JSON."""
    try:
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Fichier {QUESTIONS_FILE} introuvable")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Erreur de parsing JSON: {e}")
        return {}


def get_today_question() -> str | None:
    """Retourne la question correspondant à la date du jour."""
    questions = load_questions()
    if not questions:
        return None
    
    today = datetime.now()
    month_name = MONTHS_FR.get(today.month)
    day_index = today.day - 1  # Les listes commencent à 0
    
    if not month_name or month_name not in questions:
        logger.error(f"Mois introuvable: {month_name}")
        return None
    
    month_questions = questions[month_name]
    
    if day_index >= len(month_questions):
        logger.warning(f"Pas de question pour le jour {today.day}")
        return None
    
    return month_questions[day_index]


def format_message(question: str) -> str:
    """Formate le message de la question du jour avec un style D&D."""
    today = datetime.now()
    day_of_year = today.timetuple().tm_yday
    
    message = (
        f"## 🎲 Question du jour #{day_of_year}\n\n"
        f"*Les astres s'alignent et, sous la lumière des trois lunes, une question se dessine...*\n\n"
        f"> {question}\n\n"
        "🔮 *Que révèle votre personnage ?*"
    )
    
    return message


async def send_daily_question():
    """Se connecte à Discord, envoie la question du jour, puis se déconnecte."""
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        logger.info(f"Connecté en tant que {client.user}")
        
        try:
            channel = client.get_channel(CHANNEL_ID)
            
            # Si get_channel échoue, essayer fetch_channel
            if not channel:
                channel = await client.fetch_channel(CHANNEL_ID)
            
            if not channel:
                logger.error(f"Channel {CHANNEL_ID} introuvable")
                await client.close()
                return
            
            question = get_today_question()
            
            if not question:
                logger.warning("Aucune question disponible pour aujourd'hui")
                await client.close()
                return
            
            message = format_message(question)
            await channel.send(message)
            
            today = datetime.now()
            logger.info(f"Question du {today.day}/{today.month} envoyée: {question[:50]}...")
            
        except discord.DiscordException as e:
            logger.error(f"Erreur Discord: {e}")
        finally:
            await client.close()

    await client.start(DISCORD_TOKEN)


if __name__ == "__main__":
    logger.info("Démarrage du script...")
    asyncio.run(send_daily_question())
    logger.info("Script terminé.")
