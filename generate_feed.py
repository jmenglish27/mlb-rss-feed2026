import requests
from datetime import datetime
from email.utils import formatdate

URL = "https://statsapi.mlb.com/api/v1/standings?leagueId=103,104"

def build_feed():

    try:
        data = requests.get(URL, timeout=10).json()
    except Exception:
        data = {}

    lines = []
    lines.append("MLB Standings — All Divisions")
    lines.append("")

    records = data.get("records", [])

    # Loop through every division in the API
    for record in records:

        division_name = record.get("division", {}).get("name") or "Division"

        lines.append(division_name)
        lines.append("")

        teams = record.get("teamRecords", [])

        if not teams:
            lines.append("No data available")
            lines.append("")
            continue

        leader_wins = max(t.get("wins", 0) for t in teams)

        teams = sorted(
            teams,
            key=lambda x: x.get("wins", 0),
            reverse=True
        )

        for i, team in enumerate(teams, 1):

            name = team.get("team", {}).get("name", "Unknown Team")
            wins = team.get("wins", 0)
            losses = team.get("losses", 0)

            gb = (leader_wins - wins) / 2
            gb_text = "—" if gb == 0 else f"{gb:.1f} GB"

            lines.append(f"{i}. {name} {wins}-{losses} {gb_text}")

        lines.append("")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>MLB Standings Feed</title>
<description>Auto-updating MLB standings (all divisions)</description>

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


if __name__ == "__main__":
    build_feed()
