#
# Copyright (C) 2024 by THE-VIP-BOY-OP@Github, < https://github.com/THE-VIP-BOY-OP >.
#
# This file is part of < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC > project, 
# and is released under the MIT License.
# Please see < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC/blob/master/LICENSE >
#
# All rights reserved.
import asyncio
import importlib
import sys # Added for more robust error handling

from pyrogram import idle

import config
from config import BANNED_USERS
from VIPMUSIC import HELPABLE, LOGGER, app, userbot
from VIPMUSIC.core.call import VIP
from VIPMUSIC.plugins import ALL_MODULES
from VIPMUSIC.utils.database import get_banned_users, get_gbanned


async def init():
    # Assistant client vars check
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER("VIPMUSIC").error(
            "No Assistant Clients Vars Defined! Exiting Process."
        )
        sys.exit(1) # Exit with an error code

    # Spotify vars check
    if not config.SPOTIFY_CLIENT_ID or not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("VIPMUSIC").warning(
            "No Spotify Vars defined. Your bot won't be able to play Spotify queries."
        )

    # Load banned users
    try:
        gbanned_users = await get_gbanned()
        for user_id in gbanned_users:
            BANNED_USERS.add(user_id)
        
        banned_users = await get_banned_users()
        for user_id in banned_users:
            BANNED_USERS.add(user_id)
        LOGGER("VIPMUSIC").info("Successfully loaded banned users from database.")
    except Exception as e:
        LOGGER("VIPMUSIC").error(f"Error loading banned users: {e}")
        # Agar banned users load nahi ho paate hain toh bot ko rokna hai ya aage chalana hai,
        # yeh aapke project ke hisaab se decide karein. Abhi yeh sirf error log karega.

    # Start main Pyrogram app
    await app.start()
    LOGGER("VIPMUSIC").info("Main Pyrogram app started successfully.")

    # Import and register modules
    for all_module in ALL_MODULES:
        try:
            imported_module = importlib.import_module(all_module)
            if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
                if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                    HELPABLE[imported_module.__MODULE__.lower()] = imported_module
        except Exception as e:
            LOGGER("VIPMUSIC").error(f"Failed to import module {all_module}: {e}")
    LOGGER("VIPMUSIC.plugins").info("All modules imported and registered successfully.")

    # Start userbot and VIP music core
    await userbot.start()
    LOGGER("VIPMUSIC").info("Assistant Userbot started.")
    await VIP.start()
    await VIP.decorators()
    LOGGER("VIPMUSIC").info("VIP Music Core components initialized.")
    
    LOGGER("VIPMUSIC").info("NOBITAMUSIC STARTED SUCCESSFULLY 🕊️ - Waiting for commands...")
    
    # Keep the bot running and listening for updates
    await idle()
    LOGGER("VIPMUSIC").info("Bot idle completed. Initiating graceful shutdown.")


if __name__ == "__main__":
    try:
        # Modern way to run an async main function (Python 3.7+)
        asyncio.run(init())
    except KeyboardInterrupt:
        LOGGER("VIPMUSIC").info("Bot shutdown initiated by user (KeyboardInterrupt).")
    except Exception as e:
        LOGGER("VIPMUSIC").error(f"An unhandled error occurred during bot execution: {e}")
    finally:
        LOGGER("VIPMUSIC").info("Stopping VIPMUSIC! CHAL NIKAL LAUDE")
