"""
Discord Challenger Bot Template

This bot plays the "Challenger" role in adversarial tournaments, generating
critiques of hypotheses posted in the shared arena.

SECURITY: This template requires YOU to provide API keys via environment variables.
The framework NEVER stores your keys.

Setup:
1. Create Discord bot at https://discord.com/developers/applications
2. Copy bot token
3. Set environment variables:
     export DISCORD_BOT_TOKEN="your-discord-token"
     export OPENAI_API_KEY="your-openai-key"
4. Run: python arena/discord_challenger_bot.py

API Keys Required:
- DISCORD_BOT_TOKEN: From Discord Developer Portal
- OPENAI_API_KEY: From https://platform.openai.com/api-keys

Cost: ~$0.006 per critique (200 tokens at GPT-4 rates)
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Validate required environment variables
DISCORD_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

if not DISCORD_TOKEN:
    print("❌ ERROR: DISCORD_BOT_TOKEN not set")
    print("\nGet token from: https://discord.com/developers/applications")
    print("Set with: export DISCORD_BOT_TOKEN='your-token-here'")
    exit(1)

if not OPENAI_API_KEY:
    print("❌ ERROR: OPENAI_API_KEY not set")
    print("\nGet key from: https://platform.openai.com/api-keys")
    print("Set with: export OPENAI_API_KEY='sk-your-key-here'")
    exit(1)

# Initialize Discord bot
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Challenger system prompt
CHALLENGER_PROMPT = """You are a rigorous scientific critic in an adversarial tournament.

Your role: Identify GENUINE errors in hypotheses. Be precise and evidence-based.

Look for:
- Dimensional inconsistencies (unit mismatches)
- Conservation law violations (energy, momentum, charge)
- Fabricated parameters (invented without support)
- Numerical hallucinations (factor-of-10+ errors)
- Logical confabulations (circular reasoning)

Scoring:
- Valid major flaw: +10 points
- False alarm: -4 points (you lose if wrong!)
- Reward hacking: -8 points (fabricating issues)

Be accurate. False alarms cost you points and give opponent +6.

Output format:
1. List specific errors with evidence
2. Classify severity (minor/moderate/major)
3. Cite equations/claims being questioned

Do NOT:
- Manufacture issues to sound smart
- Question things already acknowledged as limitations
- Nitpick stylistic choices
- Repeat critiques from earlier rounds
"""

@bot.event
async def on_ready():
    """Called when bot successfully connects to Discord"""
    print(f'✅ {bot.user} is now online!')
    print(f'📊 Connected to {len(bot.guilds)} servers')
    print(f'🔍 Challenger mode: Ready to critique hypotheses')
    print(f'\nWaiting for !challenge command...')

@bot.command(name='challenge')
async def challenge(ctx, hypothesis_id: str = None):
    """
    Generate critique of hypothesis.
    
    Usage:
        !challenge HT-0042
    
    The bot will:
    1. Read recent channel history (gets hypothesis context)
    2. Generate critique via OpenAI API
    3. Post critique in channel
    """
    if not hypothesis_id:
        await ctx.send("❌ Usage: `!challenge HT-0042`")
        return
    
    # Read channel history to get context
    messages = []
    async for message in ctx.channel.history(limit=50):
        messages.append(f"{message.author.name}: {message.content}")
    
    # Reverse to get chronological order
    context = "\n".join(reversed(messages))
    
    # Generate critique
    await ctx.send(f"🔍 **[CHALLENGER - GPT-4]** analyzing {hypothesis_id}...")
    
    try:
        # NOTE: In production, this would call OpenAI API:
        #
        # import openai
        # openai.api_key = OPENAI_API_KEY
        # response = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     messages=[
        #         {"role": "system", "content": CHALLENGER_PROMPT},
        #         {"role": "user", "content": f"Context:\n{context}\n\nCritique {hypothesis_id}"}
        #     ],
        #     temperature=0.7,
        #     max_tokens=500
        # )
        # critique = response.choices[0].message.content
        
        # For this template, we show what the structure would be:
        critique = f"""**[CHALLENGER CRITIQUE - {hypothesis_id}]**

⚠️ **TEMPLATE MODE** - This is demonstration output.
For real critiques, uncomment the OpenAI API call in code.

I would identify:
1. **Dimensional Consistency:** Check all equations for unit consistency
2. **Conservation Laws:** Verify energy-momentum conservation
3. **Parameter Support:** Validate all parameters have justification

To enable real API calls:
- Uncomment lines 98-112 in discord_challenger_bot.py
- Ensure OPENAI_API_KEY is set correctly
"""
        
        await ctx.send(critique)
        
    except Exception as e:
        await ctx.send(f"❌ Error generating critique: {e}")
        print(f"Error: {e}")

@bot.command(name='status')
async def status(ctx):
    """Check bot status and configuration"""
    status_msg = f"""**Challenger Bot Status**

✅ Bot: Online
✅ OpenAI API: {"Configured" if OPENAI_API_KEY else "❌ Not Set"}
✅ Server: {ctx.guild.name}
✅ Channel: {ctx.channel.name}

Ready to challenge hypotheses!
"""
    await ctx.send(status_msg)

@bot.command(name='help_challenger')
async def help_challenger(ctx):
    """Show bot commands and usage"""
    help_msg = """**Challenger Bot Commands**

`!challenge HT-0042` - Critique hypothesis HT-0042
`!status` - Check bot configuration
`!help_challenger` - Show this message

**Tournament Flow:**
1. Human posts hypothesis
2. `!challenge` - Challenger critiques
3. `!defend` - Defender responds (different bot)
4. `!judge` - Judge scores (different bot)

**Scoring:**
- Valid major flaw: +10 points
- False alarm: -4 points
- Reward hacking: -8 points
"""
    await ctx.send(help_msg)

# Error handlers
@bot.event
async def on_command_error(ctx, error):
    """Handle command errors gracefully"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ Unknown command. Use `!help_challenger` for commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing argument. Use `!help_challenger` for usage.")
    else:
        await ctx.send(f"❌ Error: {error}")
        print(f"Error: {error}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("CHALLENGER BOT - Starting...")
    print("="*60)
    print(f"\nBot Token: {'✅ Set' if DISCORD_TOKEN else '❌ Missing'}")
    print(f"OpenAI Key: {'✅ Set' if OPENAI_API_KEY else '❌ Missing'}")
    print("\nTo enable REAL critiques:")
    print("  1. Uncomment lines 98-112 (OpenAI API call)")
    print("  2. Install openai: pip install openai")
    print("  3. Bot will then generate actual critiques")
    print("\n" + "="*60 + "\n")
    
    try:
        bot.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        print("\n❌ ERROR: Invalid Discord bot token")
        print("Verify token at: https://discord.com/developers/applications")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
