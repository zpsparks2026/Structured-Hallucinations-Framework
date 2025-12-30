# Shared Arena Setup Guide

This guide walks you through setting up a Discord or Slack workspace where multiple AI models can collaborate in a shared conversation thread, dramatically reducing API costs while enabling true adversarial validation.

## Table of Contents

1. [Why Shared Arena?](#why-shared-arena)
2. [Discord Setup (Recommended)](#discord-setup-recommended)
3. [Slack Setup (Alternative)](#slack-setup-alternative)
4. [Bot Configuration](#bot-configuration)
5. [Running Your First Tournament](#running-your-first-tournament)
6. [Troubleshooting](#troubleshooting)

---

## Why Shared Arena?

### The Problem with Traditional APIs

When running tournaments via direct API calls, you must re-send the entire conversation history with each request:

```
Round 1:  Send 1,000 tokens  → Cost: $0.03
Round 2:  Send 2,000 tokens  → Cost: $0.06
Round 3:  Send 3,000 tokens  → Cost: $0.09
...
Round 10: Send 10,000 tokens → Cost: $0.30

Total: $2.00 per tournament
```

### The Shared Arena Solution

All models read the same Discord/Slack thread:

```
Round 1:  Bot generates 200 tokens  → Cost: $0.006
Round 2:  Bot generates 200 tokens  → Cost: $0.006
...
Round 10: Bot generates 200 tokens  → Cost: $0.006

Total: $0.18 per tournament (90% savings!)
```

**Plus:**
- ✓ Real-time visibility (you watch the debate)
- ✓ Full audit trail (export transcript for paper)
- ✓ Human oversight (pause/intervene anytime)
- ✓ Transparent process (community can observe)

---

## Discord Setup (Recommended)

### Step 1: Create Discord Server

1. **Open Discord** (desktop app or web: https://discord.com)

2. **Create Server:**
   - Click the "+" icon on left sidebar
   - Choose "Create My Own"
   - Select "For me and my friends"
   - Name: "Structured Hallucinations Lab"

3. **Create Channels:**
   ```
   📁 TOURNAMENT
      #tournament-arena     ← Main discussion
      #hypothesis-queue     ← Pending validation
      #validation-results   ← Approved hypotheses
   
   📁 ADMINISTRATION
      #meta-oversight       ← Human review
      #bot-commands         ← Control bots
   ```

### Step 2: Create Discord Bots

You'll create **three separate bots** (Challenger, Defender, Judge).

**For each bot:**

1. **Go to Discord Developer Portal:**
   - Visit: https://discord.com/developers/applications
   - Log in with your Discord account

2. **Create New Application:**
   - Click "New Application"
   - Name it: "GPT-4 Challenger" (or "Claude Defender", "Gemini Judge")
   - Click "Create"

3. **Create Bot User:**
   - Click "Bot" in left sidebar
   - Click "Add Bot"
   - Confirm "Yes, do it!"

4. **Copy Bot Token:**
   - Under "TOKEN" section, click "Reset Token"
   - Click "Copy"
   - **SAVE THIS TOKEN SECURELY** (you'll need it later)
   - This is like a password for your bot

5. **Set Bot Permissions:**
   - Scroll to "Privileged Gateway Intents"
   - Enable: "MESSAGE CONTENT INTENT"
   - Enable: "SERVER MEMBERS INTENT"

6. **Invite Bot to Server:**
   - Click "OAuth2" → "URL Generator" in left sidebar
   - **Scopes:** Check "bot"
   - **Bot Permissions:** Check:
     - Read Messages/View Channels
     - Send Messages
     - Read Message History
     - Mention Everyone
   - Copy the generated URL at bottom
   - Paste URL in browser, select your server, click "Authorize"

**Repeat for all three bots:**
- Bot 1: GPT-4 Challenger
- Bot 2: Claude Defender  
- Bot 3: Gemini Judge

### Step 3: Get API Keys

You'll need API keys for the AI models:

**OpenAI (GPT-4):**
1. Go to: https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy and save securely
5. Note: $5 free credit for new accounts

**Anthropic (Claude):**
1. Go to: https://console.anthropic.com/
2. Sign up or log in
3. Click "API Keys" → "Create Key"
4. Copy and save securely

**Google (Gemini):**
1. Go to: https://ai.google.dev/
2. Click "Get API Key"
3. Create project if needed
4. Copy and save securely

### Step 4: Configure Environment Variables

**Create a file called `.env` in your framework directory:**

```bash
# Discord Bot Tokens (from Step 2)
DISCORD_CHALLENGER_TOKEN=your-challenger-bot-token-here
DISCORD_DEFENDER_TOKEN=your-defender-bot-token-here
DISCORD_JUDGE_TOKEN=your-judge-bot-token-here

# AI API Keys (from Step 3)
OPENAI_API_KEY=sk-proj-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
GOOGLE_API_KEY=your-google-key-here

# Channel IDs (find these in Step 5)
TOURNAMENT_CHANNEL_ID=your-channel-id-here
```

**Important:** Add `.env` to your `.gitignore` so keys never get committed!

### Step 5: Find Channel IDs

1. **Enable Developer Mode in Discord:**
   - User Settings → Advanced → Enable "Developer Mode"

2. **Get Channel ID:**
   - Right-click on `#tournament-arena` channel
   - Click "Copy Channel ID"
   - Paste into `.env` file as `TOURNAMENT_CHANNEL_ID`

### Step 6: Run the Bots

```bash
# Install dependencies
pip install discord.py python-dotenv openai anthropic google-generativeai

# Start each bot in separate terminals
python arena/discord_challenger_bot.py
python arena/discord_defender_bot.py  
python arena/discord_judge_bot.py
```

**You should see:**
```
Challenger bot logged in as GPT-4 Challenger#1234
Ready to validate hypotheses!
```

---

## Slack Setup (Alternative)

### Step 1: Create Slack Workspace

1. Go to: https://slack.com/create
2. Enter email, verify
3. Name workspace: "Structured Hallucinations Lab"
4. Create channels:
   - `#tournament-arena`
   - `#hypothesis-queue`
   - `#validation-results`

### Step 2: Create Slack Apps

1. Go to: https://api.slack.com/apps
2. Click "Create New App" → "From scratch"
3. Name: "GPT-4 Challenger"
4. Select your workspace

**Bot Token Scopes:**
- `channels:history` (read channel messages)
- `channels:read` (view channel info)
- `chat:write` (post messages)
- `chat:write.public` (post in any channel)

**Install to Workspace:**
- Click "Install to Workspace"
- Copy "Bot User OAuth Token"

**Repeat for Defender and Judge bots.**

### Step 3: Configure Slack Bots

Create `.env` file:

```bash
SLACK_CHALLENGER_TOKEN=xoxb-your-token-here
SLACK_DEFENDER_TOKEN=xoxb-your-token-here
SLACK_JUDGE_TOKEN=xoxb-your-token-here

OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GOOGLE_API_KEY=your-google-key
```

### Step 4: Run Slack Bots

```bash
pip install slack-sdk slack-bolt python-dotenv

python arena/slack_challenger_bot.py
python arena/slack_defender_bot.py
python arena/slack_judge_bot.py
```

---

## Bot Configuration

### Customizing Bot Behavior

Edit `arena/discord_challenger_bot.py`:

```python
# Adjust critique aggressiveness
CRITIQUE_TEMPERATURE = 0.7  # Higher = more creative critiques

# Set scoring thresholds
MAJOR_FLAW_THRESHOLD = 10  # Factor-of-10 errors
FALSE_ALARM_PENALTY = -4

# Define role-specific prompts
CHALLENGER_SYSTEM_PROMPT = """
You are a rigorous scientific critic. Your job is to identify 
genuine errors in hypotheses:
- Dimensional inconsistencies
- Conservation law violations
- Fabricated parameters
- Numerical hallucinations

Be precise. False alarms cost you points.
"""
```

### Monitoring Bot Activity

**Discord:**
- Bots appear as online users
- Messages show bot badge
- Right-click bot → "View Profile" to see status

**Slack:**
- Apps section shows bot status
- Messages tagged with [APP] badge

### Bot Commands

Once bots are running, use these commands in Discord/Slack:

**Start Tournament:**
```
!start_tournament hypothesis_id=HT-0042
```

**Manual Round:**
```
!challenge HT-0042
!defend
!judge
```

**Check Scores:**
```
!scores
```

**Export Transcript:**
```
!export tournament_HT-0042.md
```

---

## Running Your First Tournament

### Step 1: Post Hypothesis

In `#tournament-arena` channel:

```
@Tournament-Manager start HT-0042

**Hypothesis:** Gravitational screening R(k) = 1/(1 + λ²k²) with λ ~ 5 Mpc

**Prediction:** 20% void lensing suppression for R_v = 10 Mpc voids

**Parameters:**
- λ = 5 Mpc (correlation length)
- k_void ≈ 0.1 Mpc⁻¹
- R(k_void) ≈ 0.80

**Testability:** Euclid 2027, >10σ significance
```

### Step 2: Challenger Responds

Bot automatically or you trigger:
```
!challenge HT-0042
```

GPT-4 Challenger bot posts:
```
[CHALLENGER - GPT-4]

I identify three potential issues:

1. **Dimensional consistency:** Equation R(k) = 1/(1 + λ²k²) requires 
   λ and k to have inverse dimensions. Verify λ is length scale.

2. **Scale justification:** λ ~ 5 Mpc lacks derivational support. Why 
   not λ ~ 1 Mpc or λ ~ 50 Mpc?

3. **Numerical validation:** Claimed R(k_void) ≈ 0.80 assumes single-
   mode approximation. Full Fourier profile integration needed.

Severity: Minor (issues 1,3) to Moderate (issue 2)
```

### Step 3: Defender Responds

```
!defend
```

Claude Defender bot posts:
```
[DEFENDER - Claude]

Addressing critiques:

1. **Dimensional consistency:** CONFIRMED VALID
   - λ has dimensions [length] (Mpc)
   - k has dimensions [length]⁻¹ (Mpc⁻¹)
   - λ²k² is dimensionless ✓
   - R(k) is dimensionless ✓

2. **Scale justification:** ACKNOWLEDGED AS LIMITATION
   - Paper explicitly states λ ~ 5 Mpc from phenomenological fit
   - Section 7.1 acknowledges this as "most severe weakness"
   - Observable window: 10⁻² Mpc < λ < 100 Mpc
   - λ ~ 5 Mpc chosen for detectability with Euclid

3. **Numerical validation:** VALID CONCERN, ALREADY ADDRESSED
   - Paper Section 5.4 discusses extended Fourier content
   - Effective k_eff ≈ 0.1 Mpc⁻¹ after profile integration
   - Shifts from naive 0.29 to observed 0.80

**Verdict:** Critique #1 is false alarm (dimensional analysis passes).
Critiques #2 and #3 are valid observations already acknowledged in paper.
```

### Step 4: Judge Scores

```
!judge
```

Gemini Judge bot posts:
```
[JUDGE - Gemini]

**Scoring Round 1:**

Critique #1 (Dimensional consistency):
- FALSE ALARM: Dimensions are correct (λ in Mpc, k in Mpc⁻¹)
- Challenger: -4 points
- Defender: +6 points (correct refutation)

Critique #2 (Scale justification):
- VALID OBSERVATION: Paper acknowledges lack of derivation
- However, not a "major flaw" (paper is explicit about limitation)
- Challenger: +4 points (valid but minor)
- Defender: +4 points (appropriate acknowledgment)

Critique #3 (Numerical validation):
- VALID CONCERN, ALREADY ADDRESSED: Paper includes full analysis
- Challenger: +2 points (reasonable question)
- Defender: +6 points (thorough response with citations)

**Round 1 Totals:**
- Challenger: -4 + 4 + 2 = +2
- Defender: +6 + 4 + 6 = +16

**Defender wins Round 1.**
```

### Step 5: Continue Tournament

Repeat for 10 rounds or until convergence.

---

## Troubleshooting

### Bot Won't Start

**Error:** `discord.LoginFailure: Improper token has been passed`

**Solution:** 
- Check token in `.env` file
- Regenerate token in Discord Developer Portal
- Ensure no extra spaces in `.env`

**Error:** `Missing required intents`

**Solution:**
- Go to Discord Developer Portal
- Enable "MESSAGE CONTENT INTENT"
- Save changes, restart bot

### Bot Can't Read Messages

**Error:** Bot online but doesn't respond to commands

**Solution:**
- Check bot has "Read Message History" permission
- Invite bot to channel: type `/invite @BotName`
- Verify channel ID in `.env` is correct

### API Rate Limits

**Error:** `Rate limit exceeded`

**Solutions:**
- Add delays between API calls: `await asyncio.sleep(1)`
- Upgrade API tier (OpenAI, Anthropic offer higher limits)
- Use separate API keys for each bot

### Bot Responds Out of Order

**Issue:** Defender responds before reading Challenger's message

**Solution:**
- Add explicit wait in bot code:
  ```python
  await asyncio.sleep(2)  # Wait for message to propagate
  ```
- Refresh message history:
  ```python
  await ctx.channel.fetch_message(message_id)
  ```

### Export Transcript Fails

**Error:** `Permission denied` when exporting

**Solution:**
- Ensure bot has "Manage Messages" permission
- Check file write permissions in output directory
- Use `!export` command with valid filename

---

## Security Best Practices

### Protecting API Keys

1. **Never commit `.env` to Git:**
   ```bash
   echo ".env" >> .gitignore
   git rm --cached .env  # Remove if already committed
   ```

2. **Use environment variables in production:**
   ```bash
   export OPENAI_API_KEY="your-key"  # Set in shell, not in code
   ```

3. **Rotate keys regularly:**
   - Generate new API keys monthly
   - Revoke old keys after rotation

4. **Monitor usage:**
   - Check API dashboards for unexpected usage
   - Set spending limits in API platforms

### Discord Server Security

1. **Private server:**
   - Don't share invite links publicly
   - Set server to "Private"

2. **Role permissions:**
   - Create "Researcher" role with limited permissions
   - Create "Admin" role with full control
   - Assign bots to "Bot" role with minimal necessary permissions

3. **Audit logs:**
   - Server Settings → Audit Log
   - Review bot actions regularly

---

## Cost Estimation

### API Costs

**GPT-4:**
- Input: $0.00003/token
- Output: $0.00006/token
- Per message: ~200 tokens = $0.012

**Claude Sonnet:**
- Input: $0.000003/token
- Output: $0.000015/token
- Per message: ~200 tokens = $0.003

**Gemini Pro:**
- Input: $0.000000125/token
- Output: $0.0000005/token
- Per message: ~200 tokens = $0.0001

**10-Round Tournament:**
- Challenger (GPT-4): 10 × $0.012 = $0.12
- Defender (Claude): 10 × $0.003 = $0.03
- Judge (Gemini): 10 × $0.0001 = $0.001
- **Total: ~$0.15**

### Monthly Estimates

**Active research (5 tournaments/week):**
- 20 tournaments/month × $0.15 = $3.00/month

**Production scale (100 hypotheses/month):**
- 100 tournaments/month × $0.15 = $15.00/month

---

## Next Steps

1. ✓ Set up Discord server
2. ✓ Create and configure bots
3. ✓ Run first tournament
4. → Review [TOURNAMENT_GUIDE.md](TOURNAMENT_GUIDE.md) for advanced strategies
5. → Customize bot prompts for your domain
6. → Export transcripts for research papers

---

**Questions?** 
- GitHub Issues: https://github.com/zpsparks2026/Structured-Hallucinations-Framework/issues
- Email: zpsparks@asu.edu

**Last Updated:** December 30, 2024
