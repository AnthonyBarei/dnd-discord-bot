# -*- coding: utf-8 -*-
"""
Bot Discord - Question du jour (version cron)
S'exécute une fois, envoie une question aléatoire, puis quitte.
À lancer via cron : 0 9 * * * /usr/bin/python3 /path/to/bot.py
"""

import asyncio
import json
import os
import random
import logging
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


def load_questions() -> list[str]:
    """Charge les questions depuis le fichier JSON."""
    try:
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("questions", [])
    except FileNotFoundError:
        logger.error(f"Fichier {QUESTIONS_FILE} introuvable")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Erreur de parsing JSON: {e}")
        return []


def get_random_question() -> str | None:
    """Retourne une question aléatoire."""
    questions = load_questions()
    if not questions:
        return None
    return random.choice(questions)


def format_message(question: str) -> str:
    """Formate le message de la question du jour."""
    return f"🧠 **Question du jour**\n\n{question}"


async def send_daily_question():
    """Se connecte à Discord, envoie la question, puis se déconnecte."""
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
            
            question = get_random_question()
            
            if not question:
                logger.warning("Aucune question disponible")
                await client.close()
                return
            
            message = format_message(question)
            await channel.send(message)
            logger.info(f"Question envoyée: {question[:50]}...")
            
        except discord.DiscordException as e:
            logger.error(f"Erreur Discord: {e}")
        finally:
            await client.close()

    await client.start(DISCORD_TOKEN)


if __name__ == "__main__":
    logger.info("Démarrage du script...")
    asyncio.run(send_daily_question())
    logger.info("Script terminé.")
