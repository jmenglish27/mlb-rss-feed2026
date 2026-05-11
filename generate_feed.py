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
    division = (
        record.get("division", {}).get("name")
        or record.get("division", {}).get("abbreviation")
        or "Division"
    )

    lines.append(division)

    for team in record.get("teamRecords", []):
        name = team.get("team", {}).get("name", "Unknown")
        wins = team.get("wins", "?")
        losses = team.get("losses", "?")

        lines.append(f"{name}: {wins}-{losses}")

    lines.append("")

rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>

<title>MLB Standings Feed</title>
<description>Auto-updating MLB standings</description>

<item>
<title>MLB Standings Update</title>

<description><![CDATA[
{chr(10).join(lines)}
]]></description>

<pubDate>{formatdate()}</pubDate>
<guid>{datetime.utcnow().isoformat()}</guid>

</item>

</channel>
</rss>
"""

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss)

print("feed.xml generated successfully")
