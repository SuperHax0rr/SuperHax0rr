from datetime import date
from calendar import monthrange
import requests

USERNAME = "SuperHax0rr"
BIRTHDAY = date(2005, 8, 24)

# -------------------------
# Calculate age
# -------------------------

today = date.today()

years = today.year - BIRTHDAY.year
months = today.month - BIRTHDAY.month
days = today.day - BIRTHDAY.day

if days < 0:
    prev_month = today.month - 1 or 12
    prev_year = today.year if today.month != 1 else today.year - 1
    days += monthrange(prev_year, prev_month)[1]
    months -= 1

if months < 0:
    months += 12
    years -= 1

uptime = f"{years} years, {months} months, {days} days"

# -------------------------
# GitHub stats
# -------------------------

headers = {
    "Accept": "application/vnd.github+json"
}

user = requests.get(
    f"https://api.github.com/users/{USERNAME}",
    headers=headers
).json()

repos = user["public_repos"]
followers = user["followers"]

repo_list = requests.get(
    f"https://api.github.com/users/{USERNAME}/repos?per_page=100",
    headers=headers
).json()

stars = 0
commits = 0

for repo in repo_list:

    stars += repo["stargazers_count"]

    contributors = requests.get(
        f"https://api.github.com/repos/{USERNAME}/{repo['name']}/contributors",
        headers=headers
    ).json()

    if isinstance(contributors, list):
        for contributor in contributors:
            if contributor["login"].lower() == USERNAME.lower():
                commits += contributor["contributions"]

# -------------------------
# Replace placeholders
# -------------------------

with open("terminal_template.svg", "r", encoding="utf-8") as f:
    svg = f.read()

svg = svg.replace("{{UPTIME}}", uptime)
svg = svg.replace("{{REPOS}}", str(repos))
svg = svg.replace("{{COMMITS}}", str(commits))
svg = svg.replace("{{STARS}}", str(stars))
svg = svg.replace("{{FOLLOWERS}}", str(followers))

with open("terminal.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("terminal.svg updated successfully.")
