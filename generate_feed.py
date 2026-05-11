import requests
from datetime import datetime
from email.utils import formatdate

URL = "https://statsapi.mlb.com/api/v1/standings?leagueId=103,104"

AL_WEST_TEAMS = {"HOU", "TEX", "SEA", "LAA", "OAK", "ATH"}

def build_feed():

    try:
        data = requests.get(URL, timeout=10).json()
    except Exception:
        data = {}

    lines = []
    lines.append("MLB Standings — AL West")
    lines.append("")

    records = data.get("records", [])

    team_rows = []

    # 🔥 collect AL West teams from ALL divisions
    for record in records:
        teams = record.get("teamRecords", [])

        for t in teams:
            team_info = t.get("team", {})
            abbr = team_info.get("abbreviation")

            if abbr in AL_WEST_TEAMS:
                team_rows.append(t)

    if not team_rows:
        lines.append("AL West data not found")
    else:

        leader_wins = max(t.get("wins", 0) for t in team_rows)

        team_rows = sorted(
            team_rows,
            key=lambda x: x.get("wins", 0),
            reverse=True
        )

        lines.append("AL West")
        lines.append("")

        for i, team in enumerate(team_rows, 1):

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
