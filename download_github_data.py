import os
import pathlib


GITUB_TOKEN = os.getenv("GITHUB_TOKEN")
KNOWLEDGE_DIR = "knowledge"
GITHUB_DIR = "github"
GITHUB_DATA_DIR = os.path.join(KNOWLEDGE_DIR, GITHUB_DIR)

if not GITUB_TOKEN:
    try:
        import dotenv
        dotenv.load_dotenv()
        print("Found GITHUB_TOKEN")
        GITUB_TOKEN = os.getenv("GITHUB_TOKEN")
    except ImportError:
        raise Exception("Could not find GITHUB_TOKEN! If you have a .env file run pip install python-dotenv to automatically detect it")


# Check if data root folder exists
if not os.path.isdir(GITHUB_DATA_DIR):
    print(f"{GITHUB_DATA_DIR} not found")
    pathlib.Path(GITHUB_DATA_DIR).mkdir(parents=True, exist_ok=True)
    print("Created Github data directory")