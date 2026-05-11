import requests
from datetime import datetime
from email.utils import formatdate

url = "https://statsapi.mlb.com/api/v1/standings?leagueId=103,104"

data = requests.get(url).json()

content = []

for record in data["records"]:
    division = record["division"]["name"]

    content.append(f"{division}")
    content.append("")

    teams = sorted(
        record["teamRecords"],
        key=lambda x: int(x["divisionRank"])
    )

    for team in teams:
        name = team["team"]["name"]
        wins = team["wins"]
        losses = team["losses"]

        content.append(f"{name}: {wins}-{losses}")

    content.append("")
    content.append("")

standings_text = "\n".join(content)

rss = f'''<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>

<title>MLB Standings Feed</title>
<link>https://github.com</link>
<description>Auto-updating MLB standings</description>

<item>
<title>MLB Standings Update</title>

<description><![CDATA[
<pre>
{standings_text}
</pre>
]]></description>

<pubDate>{formatdate()}</pubDate>
<guid>{datetime.utcnow().isoformat()}</guid>

</item>

</channel>
</rss>
'''

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss)

print("feed.xml generated")
