# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import os
from dotenv import load_dotenv

load_dotenv()

# VPS --- FILL COOKIES 🍪 in """ ... """ 

INST_COOKIES = """
# wtite up here insta cookies
"""

YTUB_COOKIES = """
# write here yt cookies
"""

API_ID = os.getenv("API_ID", "")
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_DB = os.getenv("MONGO_DB", "")
OWNER_ID = list(map(int, os.getenv("OWNER_ID", "").split())) # list seperated via space
DB_NAME = os.getenv("DB_NAME", "SuperBot")
STRING = os.getenv("STRING", None) # optional
LOG_GROUP = int(os.getenv("LOG_GROUP", "-1002421334463")) # optional with -100
FORCE_SUB = int(os.getenv("FORCE_SUB", "-1002304047320")) # optional with -100
MASTER_KEY = os.getenv("MASTER_KEY", "023e9fe1f5c1cfec923eb61216ccaf72") # for session encryption
IV_KEY = os.getenv("IV_KEY", "75d69d46ffba") # for decryption
YT_COOKIES = os.getenv("YT_COOKIES", YTUB_COOKIES)
INSTA_COOKIES = os.getenv("INSTA_COOKIES", INST_COOKIES)
FREEMIUM_LIMIT = int(os.getenv("FREEMIUM_LIMIT", "20"))
PREMIUM_LIMIT = int(os.getenv("PREMIUM_LIMIT", "500"))
JOIN_LINK = os.getenv("JOIN_LINK", "https://t.me/testdownv3") # this link for start command message
ADMIN_CONTACT = os.getenv("ADMIN_CONTACT", "https://t.me/Ultimatesmmhelp")
