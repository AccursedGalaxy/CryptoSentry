import os
from dotenv import load_dotenv

load_dotenv()

# import TOKEN
TOKEN = os.getenv("TOKEN")
CMC_API_KEY = os.getenv("CMC_API_KEY")
TEST_GUILD_IDS = [int(os.getenv("TEST_GUILD_IDS"))]
SIGNAL_CHANNEL_ID = os.getenv("SIGNAL_CHANNEL_ID")
X_RAPIDAPI_KEY = os.getenv("X_RAPIDAPI_KEY")
