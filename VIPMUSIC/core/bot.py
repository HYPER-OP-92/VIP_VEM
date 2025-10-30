#
# Copyright (C) 2024 by VISHAL-PANDEY@Github, < https://github.com/vishalpandeynkp1 >.
#
# This file is part of < https://github.com/vishalpandeynkp1/VIPNOBITAMUSIC_REPO > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/vishalpandeynkp1/VIPNOBITAMUSIC_REPO/blob/master/LICENSE >
#
# All rights reserved.
#

import uvloop

# Install uvloop for faster asyncio event loop
uvloop.install()

import pyrogram
import pyromod.listen  # noqa: F401 # pyromod.listen is imported for side effects (to enable listen method)
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

import config

from ..logging import LOGGER


class VIPBot(Client):
    def __init__(self):
        LOGGER(__name__).info("Initializing VIP Bot Client...")
        super().__init__(
            "VIPMUSIC",  # Session name
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True # Use in_memory session for faster startup if not persisting sessions
        )
        self.one_time_startup_message_sent = False # To prevent sending startup msg multiple times if bot restarts fast

    async def start(self):
        await super().start()
        
        # Fetch bot's own information
        try:
            get_me = await self.get_me()
            self.username = get_me.username
            self.id = get_me.id
            self.name = get_me.first_name + " " + (get_me.last_name or "").strip() # Use get_me, and strip for cleaner name
            self.mention = get_me.mention
            LOGGER(__name__).info(f"Bot connected: @{self.username} (ID: {self.id})")
        except Exception as e:
            LOGGER(__name__).error(f"Failed to fetch bot's own info: {e}")
            # Consider exiting if bot can't even get its own info
            return 


        # --- Send Startup Message to Log Group ---
        # This prevents sending startup message repeatedly on fast restarts
        if not self.one_time_startup_message_sent and config.LOG_GROUP_ID:
            
            button = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        text="๏ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ๏",
                        url=f"https://t.me/{self.username}?startgroup=true",
                    )
                ]]
            )

            caption_template = (
                "╔════❰𝐖𝐄𝐋𝐂𝐎𝐌𝐄❱════❍⊱❁۪۪\n"
                "║\n"
                "║┣⪼🥀𝐁𝐨𝐭 𝐒𝐭𝐚𝐫𝐭𝐞𝐝 𝐁𝐚𝐛𝐲🎉\n"
                "║\n"
                "║┣⪼ {bot_name}\n"
                "║\n"
                "║┣⪼🎈𝐈𝐃:- `{bot_id}` \n"
                "║\n"
                "║┣⪼🎄@{bot_username} \n"
                "║ \n"
                "║┣⪼💖𝐓𝐡𝐚𝐧𝐤𝐬 𝐅𝐨𝐫 𝐔𝐬𝐢𝐧𝐠😍\n"
                "║\n"
                "╚════════════════❍⊱❁"
            )
            
            caption = caption_template.format(
                bot_name=self.name,
                bot_id=self.id,
                bot_username=self.username
            )

            try:
                await self.send_photo(
                    config.LOG_GROUP_ID,
                    photo=config.START_IMG_URL,
                    caption=caption,
                    reply_markup=button,
                )
                self.one_time_startup_message_sent = True
                LOGGER(__name__).info("Startup photo sent to log group.")
            except pyrogram.errors.ChatWriteForbidden as e:
                LOGGER(__name__).warning(
                    f"Bot cannot send photo/message to log group (ChatWriteForbidden): {e}. Trying text message."
                )
                try:
                    # Fallback to text message if photo fails
                    await self.send_message(
                        config.LOG_GROUP_ID,
                        caption, # Using the same caption for consistency
                        reply_markup=button,
                    )
                    self.one_time_startup_message_sent = True
                    LOGGER(__name__).info("Startup text message sent to log group (fallback).")
                except Exception as e_fallback:
                    LOGGER(__name__).error(f"Failed to send any startup message to log group: {e_fallback}")
            except Exception as e:
                LOGGER(__name__).error(f"Unexpected error while sending startup message to log group: {e}")
        elif not config.LOG_GROUP_ID:
            LOGGER(__name__).warning("LOG_GROUP_ID is not set, skipping log group notifications.")
        
        # --- Setting Bot Commands ---
        if config.SET_CMDS:
            LOGGER(__name__).info("Attempting to set bot commands...")
            try:
                # Group all commands for better organization
                private_cmds = [
                    BotCommand("start", "Start the bot"),
                    BotCommand("help", "Get the help menu"),
                    BotCommand("ping", "Check if the bot is alive or dead"),
                ]
                
                group_cmds = [
                    BotCommand("play", "Start playing requested song"),
                    BotCommand("stop", "Stop the current song"),
                    BotCommand("pause", "Pause the current song"),
                    BotCommand("resume", "Resume the paused song"),
                    BotCommand("queue", "Check the queue of songs"),
                    BotCommand("skip", "Skip the current song"),
                    BotCommand("volume", "Adjust the music volume"),
                    BotCommand("lyrics", "Get lyrics of the song"),
                ]
                
                admin_cmds = [
                    BotCommand("start", "❥ Start the bot"),
                    BotCommand("ping", "❥ Check the ping"),
                    BotCommand("help", "❥ Get help"),
                    BotCommand("vctag", "❥ Tag all for voice chat"),
                    BotCommand("stopvctag", "❥ Stop tagging for VC"),
                    BotCommand("tagall", "❥ Tag all members by text"),
                    BotCommand("cancel", "❥ Cancel the tagging"),
                    BotCommand("settings", "❥ Get the settings"),
                    BotCommand("reload", "❥ Reload the bot"),
                    BotCommand("play", "❥ Play the requested song"),
                    BotCommand("vplay", "❥ Play video along with music"),
                    BotCommand("end", "❥ Empty the queue"),
                    BotCommand("playlist", "❥ Get the playlist"),
                    BotCommand("stop", "❥ Stop the song"),
                    BotCommand("lyrics", "❥ Get the song lyrics"),
                    BotCommand("song", "❥ Download the requested song"),
                    BotCommand("video", "❥ Download the requested video song"),
                    BotCommand("gali", "❥ Reply with fun"),
                    BotCommand("shayri", "❥ Get a shayari"),
                    BotCommand("love", "❥ Get a love shayari"),
                    BotCommand("sudolist", "❥ Check the sudo list"),
                    BotCommand("owner", "❥ Check the owner"),
                    BotCommand("update", "❥ Update bot"),
                    BotCommand("gstats", "❥ Get stats of the bot"),
                    BotCommand("repo", "❥ Check the repo"),
                ]
                
                await self.set_bot_commands(private_cmds, scope=BotCommandScopeAllPrivateChats())
                await self.set_bot_commands(group_cmds, scope=BotCommandScopeAllGroupChats())
                await self.set_bot_commands(admin_cmds, scope=BotCommandScopeAllChatAdministrators())
                
                LOGGER(__name__).info("Bot commands set successfully for all scopes.")
            except Exception as e:
                LOGGER(__name__).error(f"Failed to set bot commands: {e}")
        else:
            LOGGER(__name__).info("SET_CMDS is False. Skipping setting bot commands.")

        # --- Check Bot Admin Status in Logger Group ---
        if config.LOG_GROUP_ID:
            LOGGER(__name__).info(f"Checking bot admin status in log group {config.LOG_GROUP_ID}...")
            try:
                chat_member_info = await self.get_chat_member(
                    config.LOG_GROUP_ID, self.id
                )
                if chat_member_info.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                    LOGGER(__name__).error(
                        "Bot is not an administrator in the Logger Group! Please promote Bot as Admin."
                    )
                else:
                    LOGGER(__name__).info("Bot is an administrator in the Logger Group.")
            except pyrogram.errors.PeerIdInvalid:
                LOGGER(__name__).error(f"LOG_GROUP_ID {config.LOG_GROUP_ID} is invalid. Please check the ID.")
            except pyrogram.errors.ChatIdInvalid:
                LOGGER(__name__).error(f"LOG_GROUP_ID {config.LOG_GROUP_ID} is invalid. Please check the ID.")
            except pyrogram.errors.ChannelPrivate:
                 LOGGER(__name__).error(f"LOG_GROUP_ID {config.LOG_GROUP_ID} is a private channel/group. Bot must be invited manually and promoted.")
            except Exception as e:
                LOGGER(__name__).error(f"Error checking bot's admin status in log group: {e}")
        
        LOGGER(__name__).info(f"MusicBot Started as {self.name} (@{self.username}).")
