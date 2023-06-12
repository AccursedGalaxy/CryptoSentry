import os
from dotenv import load_dotenv

load_dotenv()

# import TOKEN
TOKEN = os.getenv("TOKEN")
CMC_API_KEY = os.getenv("CMC_API_KEY")
TEST_GUILD_IDS = [int(os.getenv("TEST_GUILD_IDS"))]
