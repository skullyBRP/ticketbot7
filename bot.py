import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Emoji mapping voor ticket types
ticket_types = {
    "hulpticket": {"emoji": "🟢", "staff_only": False},
    "refundticket": {"emoji": "🔵", "staff_only": False},
    "unbanticket": {"emoji": "🔴", "staff_only": False},
    "overstap": {"emoji": "✈️", "staff_only": False},
    "klacht": {"emoji": "🟤", "staff_only": True}
}

# Staff role ID (vervang dit door je eigen staff role)
STAFF_ROLE_ID = 1454817763033088202  # <-- Vul hier je echte staff role ID in

# Category IDs gekoppeld aan ticket types
CATEGORY_TICKET_IDS = {
    1454188736995659876: "hulpticket",
    1454188738698543125: "refundticket",
    1454188740099575849: "unbanticket",
    1454197352272236584: "overstap",
    1454214259905921044: "klacht"
}

@bot.event
async def on_ready():
    print(f'Bot is online als {bot.user}')

@bot.event
async def on_guild_channel_create(channel):
    # Controleer of het kanaal een tekstkanaal is en in een ticketcategorie zit
    if isinstance(channel, discord.TextChannel):
        cat_id = channel.category.id if channel.category else None
        if cat_id in CATEGORY_TICKET_IDS:
            type_ticket = CATEGORY_TICKET_IDS[cat_id]
            data = ticket_types[type_ticket]
            emoji = data["emoji"]
            staff_only = data["staff_only"]

            # Kanaalnaam samenstellen
            new_name = f"{emoji}-{type_ticket}"

            # Basis permissies
            overwrites = {
                channel.guild.default_role: discord.PermissionOverwrite(read_messages=not staff_only),
                channel.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }

            # Staff role toevoegen bij staff-only tickets
            if staff_only:
                staff_role = channel.guild.get_role(STAFF_ROLE_ID)
                if staff_role:
                    overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
                else:
                    print("⚠️ Staff role niet gevonden, check STAFF_ROLE_ID")
                    return

            try:
                await channel.edit(name=new_name, overwrites=overwrites)
                print(f"✅ Kanaal {channel.name} automatisch hernoemd naar {new_name}")
            except Exception as e:
                print(f"❌ Kon kanaal niet hernoemen: {e}")

import os

bot.run(os.getenv("DISCORD_TOKEN"))