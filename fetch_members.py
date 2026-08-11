import discord
import json
import asyncio
import os
from datetime import datetime

# ── CONFIG ──────────────────────────────────────────────────────────────────
# Map each rank abbreviation to the EXACT Discord role name in your server.
# If a rank doesn't have a Discord role, remove it from the dict.
RANK_TO_ROLE = {
    # Seamen
    "SR":  "SR | Seaman Recruit",
    "SA":  "SA | Seaman Apprentice",
    "SN":  "SN | Seaman",
    # Petty Officers
    "PO3": "PO3 | Petty Officer Third Class",
    "PO2": "PO2 | Petty Officer Second Class",
    "PO1": "PO1 | Petty Officer First Class",
    # Chief Petty Officers
    "SCPO":"SCPO | Senior Chief Petty Officer",
    "MCPO":"MCPO | Master Chief Petty Officer",
    "CMCPO":"CMCPO | Command Master Chief Petty Officer",
    "MCPCG":"MCPCG | Master Chief Petty Officer Of The Coast Guard",
    # Chief Warrant Officers
    "CW2":  "CW2 | Chief Warrant Officer 2",
    "CW3":  "CW3 | Chief Warrant Officer 3",
    "CW4":  "CW4 | Chief Warrant Officer 4",
    # Junior Officers
    "ENS":  "ENS | Ensign",
    "LTJG":  "LTJG | Lieutenant Junior Grade",
    "LT":  "LT | Lieutenant",
    "LCDR":  "LCDR | Lieutenant Commander",
    # Senior Officers
    "CDR":  "CDR | Commander",
    "CAPT":  "CAPT | Captain",
    # Flag Officers
    "RDML":   "RDML | Rear Admiral Lower Half",
    "RADM":   "RADM | Rear Admiral",
    "VADM":  "VADM | Vice Admiral",
    "ADM":  "ADM | Admiral",
    "FADM":   "FADM | Fleet Admiral (Wartime Only)",
}

# ── NAME OVERRIDES ───────────────────────────────────────────────────────────
# Format: "UserID": "Name to show on website"
NAME_OVERRIDES = {
    "670646167448584192": "GEN | Arrcqne",
    "961265519980335124": "MG | Youknowmeyoukno | CO-G18"
}
# ────────────────────────────────────────────────────────────────────────────

TOKEN     = os.environ["DISCORD_TOKEN"]
GUILD_ID  = int(os.environ["DISCORD_GUILD_ID"])

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        print(f"ERROR: Guild {GUILD_ID} not found.")
        await client.close()
        return

    # Build role-name → role object map
    role_map = {r.name: r for r in guild.roles}

    # DEBUG — prints all roles found in the server and total member count
    print(f"  Connected to: {guild.name}")
    print(f"  Total members visible: {len(guild.members)}")
    print(f"  Roles found in server:")
    for r in sorted(guild.roles, key=lambda x: x.name):
        print(f"     • '{r.name}' ({len(r.members)} members)")
    print("─" * 50)

    result = {}
    for rank, role_name in RANK_TO_ROLE.items():
        role = role_map.get(role_name)
        if role:
            members = [NAME_OVERRIDES.get(str(m.id), m.display_name) for m in guild.members if role in m.roles]
            result[rank] = sorted(members, key=str.lower)
        else:
            result[rank] = []   # role not found – leave empty

    output = {
        "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "members": result
    }

    with open("members.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"  Saved members.json  ({datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')})")
    await client.close()

client.run(TOKEN)
