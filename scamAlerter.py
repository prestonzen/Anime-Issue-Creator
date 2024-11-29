import os
import time
import random
import requests
from dotenv import load_dotenv
from tqdm import tqdm  # For the progress bar

# Load environment variables from .env file
load_dotenv()

# Access the GitHub token from the .env file
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Ensure the token is loaded
if not GITHUB_TOKEN:
    raise ValueError("Missing GITHUB_TOKEN in environment variables. Add it to a .env file.")

# List of GitHub repositories in the format 'owner/repo'
repos = [
    "root-cyborg127/Televiewbooster"
 #   "tmarktg/Calculator-Beta",
 #   "tmarktg/test",
 #   "tmarktg/lesson_03",
 #   "tmarktg/lesson_04",
 #   "tmarktg/lesson_05",
 #   "tmarktg/Lesson_06",
 #   "tmarktg/git_test"
]

# Headers with authorization token
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Mozilla/5.0"
}

# Hardcoded delay for staying below 490 requests/hour
DELAY = 3600 / 490  # ≈ 7.35 seconds

# Fetch random anime title using Jikan API
def get_random_anime_title():
    """Fetch a random anime title using the Jikan API."""
    try:
        page = random.randint(1, 5)  # Limit to the first few pages for efficiency
        response = requests.get(f"https://api.jikan.moe/v4/top/anime?page={page}")
        response.raise_for_status()
        data = response.json()
        anime = random.choice(data["data"])
        return anime["title"]
    except Exception as e:
        print(f"Error fetching anime title: {e}")
        return "Default Issue Title"

# Create GitHub issue
def create_github_issue(repo, title):
    """Create a new issue in the specified GitHub repository."""
    url = f"https://api.github.com/repos/{repo}/issues"
    payload = {
        "title": title,
        "body": "This issue was created automatically with an anime title."
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print(f"Issue created successfully in {repo}: {title}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error creating issue in {repo}: {e}")
        if response is not None:
            print(f"Response: {response.status_code} - {response.text}")
        return False

# Main function to loop through repos
def main():
    issues_created = 0  # Track the total number of issues created
    while True:
        for repo in repos:
            print(f"\nProcessing repository: {repo}")
            title = "This-repo-is-a-scam" #get_random_anime_title()

            # Skip if title is a fallback
            if title == "Default Issue Title":
                print("Skipping issue creation due to fallback title.")
                continue

            success = create_github_issue(repo, title)
            if success:
                issues_created += 1
                print(f"Total Issues Created: {issues_created}")

            # Show progress bar until the next issue
            print(f"Waiting {DELAY:.2f} seconds before the next issue...")
            for _ in tqdm(range(int(DELAY)), desc="Time until next issue", unit="s"):
                time.sleep(1)

# Run the script
if __name__ == "__main__":
    main()
