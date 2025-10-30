#
# Copyright (C) 2024 by THE-VIP-BOY-OP@Github, < https://github.com/THE-VIP-BOY-OP >.
#
# This file is part of < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC > project,
# and is released under the MIT License.
# Please see < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC/blob/master/LICENSE >
#
# All rights reserved.

# Core Bot Components Imports
from VIPMUSIC.core.bot import VIPBot
from VIPMUSIC.core.dir import dirr
from VIPMUSIC.core.git import git
from VIPMUSIC.core.userbot import Userbot
from VIPMUSIC.misc import dbb, heroku, sudo

# Logging Setup
from .logging import LOGGER

# --- Initializing Core Bot Setup ---
LOGGER(__name__).info("Starting VIPMUSIC package core setup...")

# Directories Setup
dirr()
LOGGER(__name__).info("Project directories ensured.")

# Check for Git Updates
git()
LOGGER(__name__).info("Git updates checked.")

# Initialize Memory Database
dbb()
LOGGER(__name__).info("Memory database initialized.")

# Heroku APP Configuration
heroku()
LOGGER(__name__).info("Heroku configuration loaded (if applicable).")

# Load Sudo Users from Database
sudo()
LOGGER(__name__).info("Sudo users loaded.")

# --- Client Instantiation ---

# Main Bot Client
app = VIPBot()
LOGGER(__name__).info("Main Bot Client 'app' instantiated.")

# Assistant Client
userbot = Userbot()
LOGGER(__name__).info("Assistant Client 'userbot' instantiated.")

# --- Music Platform API Setup ---
# Explicitly importing individual APIs for clarity
from .platforms import (
    AppleAPI,
    CarbonAPI,
    YouTubeAPI,
    SpotifyAPI,
    RessoAPI,
    SoundAPI,
    TeleAPI,
)

YouTube = YouTubeAPI()
Carbon = CarbonAPI()
Spotify = SpotifyAPI()
Apple = AppleAPI()
Resso = RessoAPI()
SoundCloud = SoundAPI()
Telegram = TeleAPI()
LOGGER(__name__).info("All music platform APIs initialized.")

# Dictionary to hold help modules (will be populated by main init.py)
HELPABLE = {}

LOGGER(__name__).info("VIPMUSIC package core setup completed successfully.")
