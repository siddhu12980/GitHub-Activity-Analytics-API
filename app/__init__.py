import os
from dotenv import load_dotenv

load_dotenv()


print("GITHUB_CLIENT_ID:", os.getenv("GITHUB_CLIENT_ID"))


