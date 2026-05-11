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
    lines.append("MLB Standings — AL West")
    lines.append("")

    records = data.get("records", [])

    alwest_teams = []

    # 🔥 STEP 1: find AL West properly from API structure
    for record in records:

        division = record.get("division", {}).get("name", "")

        # flexible match (API naming varies)
        if "West" in division and "American League" in division:

            teams = record.get("teamRecords", [])

            for t in teams:
                alwest_teams.append(t)

    # fallback safety
    if not alwest_teams:
        lines.append("AL West data not found")
    else:

        leader_wins = max(t.get("wins", 0) for t in alwest_teams)

        alwest_teams = sorted(
            alwest_teams,
            key=lambda x: x.get("wins", 0),
            reverse=True
        )

        lines.append("AL West")
        lines.append("")

        for i, team in enumerate(alwest_teams, 1):

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
<description>Auto-updating AL West standings</description>

<item>
<title>AL West Standings Update</title>
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
