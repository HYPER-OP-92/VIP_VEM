#
# Copyright (C) 2024 by THE-VIP-BOY-OP@Github, < https://github.com/THE-VIP-BOY-OP >.
#
# This file is part of < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC > project,
# and is released under the MIT License.
# Please see < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC/blob/master/LICENSE >
#
# All rights reserved.

# Core Bot Components
from VIPMUSIC.core.bot import VIPBot
from VIPMUSIC.core.dir import dirr
from VIPMUSIC.core.git import git
from VIPMUSIC.core.userbot import Userbot
from VIPMUSIC.misc import dbb, heroku, sudo

# Logging
from .logging import LOGGER

# Initialize directories, check git, database, heroku, and sudo users
LOGGER(__name__).info("Initializing core components...") # Added log for clarity
dirr()
git()
dbb()
heroku()
sudo()

# Bot Client
app = VIPBot()
LOGGER(__name__).info("Main Bot Client Initialized.") # Added log

# Assistant Client
userbot = Userbot()
LOGGER(__name__).info("Assistant Client Initialized.") # Added log

# Platform APIs
# It's generally good practice to explicitly import what you need
# rather than using a wildcard import if possible, for clarity.
from .platforms import ( # Grouped for better readability
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

LOGGER(__name__).info("Music Platform APIs Initialized.") # Added log

# Dictionary to hold help modules (populated later)
HELPABLE = {}

# End of __init__.py setup
LOGGER(__name__).info("VIPMUSIC package core setup complete.") # Added final log
