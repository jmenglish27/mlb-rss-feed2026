import requests
from datetime import datetime
from email.utils import formatdate

URL = "https://statsapi.mlb.com/api/v1/standings?leagueId=103,104"

try:
    data = requests.get(URL, timeout=10).json()
except Exception:
    data = {}

lines = []

for record in data.get("records", []):
    division_name = record.get("division", {}).get("name", "")
    # ONLY keep AL West
    if division_name != "American League West":
        continue

lines = []
lines.append("MLB Standings — AL West")
lines.append("")

for record in data.get("records", []):

    division_name = record.get("division", {}).get("name", "")

    # ONLY AL West
    if division_name != "American League West":
        continue

    lines.append("AL West")
    teams = record.get("teamRecords", [])
    leader = max(t.get("wins", 0) for t in teams)
    teams = sorted(teams, key=lambda x: x.get("wins", 0), reverse=True)

    for i, team in enumerate(teams, 1):
        name = team.get("team", {}).get("name", "Unknown Team")
        wins = team.get("wins", 0)
        losses = team.get("losses", 0)
        gb = (leader - wins) / 2
        gb_text = "—" if gb == 0 else f"{gb:.1f} GB"
        lines.append(f"{i}. {name} {wins}-{losses} {gb_text}")
    lines.append("")

rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>

lines = []
lines.append("MLB Standings — Live Race")
lines.append("")

for record in data.get("records", []):

    division = (
        record.get("division", {}).get("name")
        or record.get("division", {}).get("abbreviation")
        or "Division"
    )

    lines.append(division)   # ✅ ONLY ONCE PER DIVISION

    teams = record.get("teamRecords", [])

    if not teams:
        continue

    leader = max(t.get("wins", 0) for t in teams)

    teams = sorted(teams, key=lambda x: x.get("wins", 0), reverse=True)

    for i, team in enumerate(teams, 1):
        name = team.get("team", {}).get("name", "Unknown Team")
        wins = team.get("wins", 0)
        losses = team.get("losses", 0)

        gb = (leader - wins) / 2
        gb_text = "—" if gb == 0 else f"{gb:.1f} GB"

        lines.append(f"{i}. {name} {wins}-{losses} {gb_text}")

    lines.append("")  # blank line between divisions

</item>

</channel>
</rss>
"""

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss)

print("feed.xml generated successfully")
