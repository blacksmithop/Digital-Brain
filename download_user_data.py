import os
import pathlib
import click


@click.command()
@click.option("--username", prompt="Github usernamw", help="Your Github username")
def download_github_data(username: str):
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    KNOWLEDGE_DIR = "knowledge"
    GITHUB_DIR = "github"
    GITHUB_DATA_DIR = os.path.join(KNOWLEDGE_DIR, GITHUB_DIR)
    
    if not GITHUB_TOKEN:
        try:
            import dotenv
            dotenv.load_dotenv()
            click.echo(click.style("Found GITHUB_TOKEN", fg="green"))
            GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
        except ImportError:
            click.echo(click.style("Could not find GITHUB_TOKEN! If you have a .env file run pip install python-dotenv to automatically load it", fg="red"))
            exit(0)
            
    # # Check if data root folder exists
    if not os.path.isdir(GITHUB_DATA_DIR):
        click.echo(click.style(f"{GITHUB_DATA_DIR} not found", fg="red"))
        pathlib.Path(GITHUB_DATA_DIR).mkdir(parents=True, exist_ok=True)
        click.echo(click.style("Created Github data directory", fg="green"))
    
if __name__ == "__main__":
    download_github_data()