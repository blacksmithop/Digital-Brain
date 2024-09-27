import os
import pathlib
import click
import requests
from git import Repo


@click.command()
@click.option("--username", prompt="Github username", help="Your Github username")
def download_github_data(username: str):
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    KNOWLEDGE_DIR = "./knowledge"
    GITHUB_DIR = "github"
    GITHUB_DATA_DIR = os.path.join(KNOWLEDGE_DIR, GITHUB_DIR)

    if not GITHUB_TOKEN:
        try:
            import dotenv
            dotenv.load_dotenv()
            click.echo(click.style("Found GITHUB_TOKEN", fg="green"))
            GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
        except ImportError:
            click.echo(click.style(
                "Could not find GITHUB_TOKEN! If you have a .env file run pip install python-dotenv to automatically load it", fg="red"))
            exit(0)

    # # Check if data root folder exists
    if not os.path.isdir(GITHUB_DATA_DIR):
        click.echo(click.style(f"{GITHUB_DATA_DIR} not found", fg="red"))
        pathlib.Path(GITHUB_DATA_DIR).mkdir(parents=True, exist_ok=True)
        click.echo(click.style("Created Github data directory", fg="green"))

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    click.echo(click.style(f"GitHub username {username}", fg="cyan"))

    results = []
    per_page = 100
    try:
        for i in range(1, 100):
            try:
                response = requests.get(
                    f"https://api.github.com/users/{username}/repos?page={i}&per_page={per_page}", headers=headers)
                json_data = response.json()
                results.extend(json_data)
                fetch_len = len(json_data)
                click.echo(click.style(
                    f"Page{i} ({fetch_len}/{per_page})", fg="white"))
                if fetch_len == 0:
                    break
            except Exception as e:
                print(response.status_code)
                break

        click.echo(click.style(
            f"Found {len(results)} repositories for user {username}", fg="green"))
    except Exception as e:
        click.echo(click.style(
            f"Could not find repositories for user {username} due to {e}", fg="red"))
        exit(0)

    click.echo(click.style("Download data?", fg="cyan"))
    download = input("yes/no >>")
    download = download.lower()
    if download == "no":
        exit(0)
    elif download == "yes":
        click.echo(click.style(
            f"Downloading repositories for user {username}...", fg="green"))

    os.chdir(GITHUB_DATA_DIR)
    # Git clone shallow
    for repo in results:
        repo_name = repo['name']
        clone_url = repo['clone_url']
        click.echo(click.style(
            f"Cloning repository: {repo_name}", fg="yellow"))
        click.echo(click.style(
            f"URL {clone_url}", fg="bright_magenta"))
        os.mkdir(repo_name)
        Repo.clone_from(url=clone_url, to_path=repo_name, depth=1)

if __name__ == "__main__":
    download_github_data()
