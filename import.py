import discord
from discord.ext import commands, tasks
import requests

# ==== CONFIG ====
# Replace this with your actual Bot Token
TOKEN = "MTQzOTU4NjQ2OTY1MTE1MjkyNg.G0d2cP.q8CupYxF44XC3UqkmEZyG7u-SeguIN-P_o7e4E" 
# CORRECTED: Includes the /api/botdata path
WEB_ENDPOINT = "https://receiver-th57.onrender.com/api/botdata" 

DEVELOPER_ROLE_NAME = "Developer"
MODERATOR_ROLE_NAME = "Moderator"

# NOTE: You MUST enable the Server Members and Presence Intents in the Discord Developer Portal
intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ----------------------------
# Function: Send data to website
# ----------------------------
def send_to_website(data: dict):
    """Sends the collected server data as a JSON POST request to your web server API."""
    try:
        # Use the WEB_ENDPOINT for the POST request
        response = requests.post(WEB_ENDPOINT, json=data, timeout=5)
        print(f"✓ Sent to website (Status: {response.status_code})")
        # Print the response content for debugging your web server
        print(f"Server Response: {response.text[:100]}...") 
    except Exception as e:
        print("✗ ERROR sending to website:", e)


# ----------------------------
# Auto-update task: runs every 15 seconds
# ----------------------------
@tasks.loop(seconds=15)
async def update_status():
    print("Updating server status...")

    # We assume the bot is only in one primary server for this simple loop.
    if not bot.guilds:
        print("Bot is not in any guild.")
        return

    # Using the first guild the bot is connected to
    guild = bot.guilds[0]
    members = guild.members

    total_members = len(members)
    # Counts users that are not 'offline' (online, idle, dnd, streaming)
    active_users = sum(1 for m in members if m.status != discord.Status.offline)

    moderator_count = 0
    developer_count = 0

    for member in members:
        # Getting role names is better for comparison
        role_names = [r.name for r in member.roles]
        if MODERATOR_ROLE_NAME in role_names:
            moderator_count += 1
        if DEVELOPER_ROLE_NAME in role_names:
            developer_count += 1

    # Data package to send
    data = {
        "server_id": guild.id,
        "server_name": guild.name,
        "total_members": total_members,
        "active_users": active_users,
        "moderators": moderator_count,
        "developers": developer_count
    }

    send_to_website(data)


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    update_status.start()  # start 15-sec auto update


# ----------------------------
# Manual command version (for testing)
# ----------------------------
@bot.command()
async def report(ctx):
    guild = ctx.guild
    members = guild.members

    # Recalculating stats for the command
    total_members = len(members)
    active_users = sum(1 for m in members if m.status != discord.Status.offline)

    moderator_count = 0
    developer_count = 0

    for member in members:
        role_names = [r.name for r in member.roles]
        if MODERATOR_ROLE_NAME in role_names:
            moderator_count += 1
        if DEVELOPER_ROLE_NAME in role_names:
            developer_count += 1

    embed = discord.Embed(title="📊 Server Report", color=discord.Color.blue())
    embed.add_field(name="👥 Total Members", value=total_members)
    embed.add_field(name="🟢 Active Users", value=active_users)
    embed.add_field(name="🛡️ Moderators", value=moderator_count)
    embed.add_field(name="💻 Developers", value=developer_count)

    await ctx.send(embed=embed)


bot.run(TOKEN)