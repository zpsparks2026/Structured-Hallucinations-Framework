# Tournament Guide

Complete guide to running adversarial validation tournaments using the Structured Hallucinations Framework.

## Table of Contents

1. [Tournament Overview](#tournament-overview)
2. [Scoring System](#scoring-system)
3. [Running Manual Tournaments](#running-manual-tournaments)
4. [Running Automated Tournaments](#running-automated-tournaments)
5. [Best Practices](#best-practices)
6. [Common Pitfalls](#common-pitfalls)

---

## Tournament Overview

### What is a Tournament?

A tournament is an adversarial validation process where:
- **Challenger LLM** generates critiques of hypotheses
- **Defender LLM** responds with refutations or repairs
- **Judge LLM** scores the exchange
- **Feedback routing** returns rejected hypotheses to appropriate loop

### Why Tournaments?

**Problem:** Single-model validation can't catch its own errors
- LLM validates its own hallucination → circular reasoning
- No adversarial pressure → accepts plausible-but-wrong claims

**Solution:** Adversarial competition with scoring incentives
- Challenger benefits from finding REAL flaws (+10)
- Fabricating issues costs points (-4 when caught)
- Defender benefits from correct refutations (+6)
- Both benefit from being accurate

---

## Scoring System

### Point Values

| Action | Points | Description |
|--------|--------|-------------|
| **Valid major flaw** | +10 | Dimensional error, conservation violation, fabricated parameter |
| **Valid minor observation** | +4 | Correct but non-critical issue |
| **Correct refutation** | +6 | Catching false alarm, defending valid claim |
| **Coherent repair** | +4 | Fix that preserves global consistency |
| **Mutual validation** | +4 each | Both acknowledge good point |
| **False alarm** | -4 | Invalid critique of valid hypothesis |
| **Reward hacking** | -8 | Fabricated reasoning, invented parameters |

### Scoring Philosophy

**Self-Stabilizing Game Theory:**

The scoring creates Nash equilibrium where honesty dominates:

1. **Fabrication vs. Discovery:**
   - Fabricating critique: Expected value = -4 (if caught) + probability × +10
   - Finding real flaw: Expected value = +10 (guaranteed)
   - Result: Genuine discovery dominates

2. **False Alarm vs. Letting Pass:**
   - False alarm penalty: -4 points + opponent gains +6 = -10 point swing
   - Missing real flaw: 0 points (neither gains/loses)
   - Result: Precision > recall incentivized

3. **Defense vs. Acknowledgment:**
   - Defending invalid hypothesis: Invites escalating challenges (0 long-term)
   - Acknowledging flaw + proposing repair: +4 points + ends challenge
   - Result: Constructive repair dominates

### Severity Classification

**Major Flaws (+10):**
- Factor-of-10+ numerical errors
- Dimensional inconsistencies (unit mismatches)
- Conservation law violations (energy, momentum, charge)
- Fabricated parameters without derivation
- Circular reasoning in core argument

**Moderate Issues (+4):**
- Assumptions needing justification
- Missing experimental validation
- Incomplete error analysis
- Scope limitations not acknowledged

**Minor Observations (+2):**
- Stylistic improvements
- Additional citations needed
- Clearer explanation possible

**False Alarms (-4):**
- Critique of correct claim
- Misunderstanding of hypothesis
- Questioning acknowledged limitations
- Nitpicking presentation

**Fabrications (-8):**
- Invented constants not in hypothesis
- Made-up equations
- Fabricated contradictions
- Strawman arguments

---

## Running Manual Tournaments

### Step 1: Prepare Hypothesis

Create structured hypothesis document:

```markdown
## Hypothesis HT-2024-0042

**Claim:** Gravitational screening R(k) = 1/(1 + λ²k²) with λ ~ 5 Mpc

**Prediction:** 20% void lensing suppression for R_v = 10 Mpc

**Parameters:**
- λ = 5 Mpc (correlation length)
- R(k) = 1/(1 + λ²k²) (response function)
- k_void ≈ π/R_v (characteristic wavenumber)

**Testability:** Euclid 2027 (>10σ significance)

**Status:** Awaiting validation
```

### Step 2: Challenger Round

**Prompt to GPT-4:**

```
You are the Challenger in an adversarial scientific tournament.

Scoring:
- Valid major flaw: +10 points
- False alarm: -4 points
- Fabrication: -8 points

Your job: Identify GENUINE errors in this hypothesis:

[paste hypothesis]

Look for:
1. Dimensional inconsistencies
2. Conservation law violations
3. Fabricated parameters
4. Numerical hallucinations (factor-of-10+ errors)
5. Logical confabulations

Be precise. False alarms cost you points.

Output format:
- List specific errors with evidence
- Classify severity (major/moderate/minor)
- Cite equations being questioned
```

**Copy response to tournament transcript.**

### Step 3: Defender Round

**Prompt to Claude:**

```
You are the Defender in an adversarial scientific tournament.

Scoring:
- Correct refutation: +6 points
- Coherent repair: +4 points
- Acknowledging valid flaw: +4 points

The Challenger claims:

[paste Challenger's critique]

Your job: Either refute the critique OR propose repair.

If refuting:
- Show why critique is invalid
- Provide evidence (calculations, citations)

If repairing:
- Acknowledge the flaw
- Propose fix that preserves global consistency
- Show repair resolves issue

Be honest. Defending invalid claims invites escalation.
```

**Copy response to tournament transcript.**

### Step 4: Judge Round

**Prompt to Gemini (or third model):**

```
You are the Judge in an adversarial scientific tournament.

Challenger's critique:
[paste critique]

Defender's response:
[paste response]

Score each critique point:
- Valid major flaw: Challenger +10
- Valid minor issue: Challenger +4
- False alarm: Challenger -4, Defender +6
- Coherent repair: Defender +4

For each point:
1. State whether critique is valid
2. Provide rationale
3. Assign points

Then:
- Sum points for round
- State cumulative tournament scores
- Declare round winner
```

**Copy scoring to tournament transcript.**

### Step 5: Iterate

Repeat Steps 2-4 for 10 rounds or until:
- Hypothesis passes all critiques
- Fundamental flaw discovered (terminate early)
- Repairs converge to stable form

---

## Running Automated Tournaments

### Using Python Script

```python
from adversarial import AdversarialTournament
import os

# Load API keys from environment
tournament = AdversarialTournament(
    challenger_key=os.environ['OPENAI_API_KEY'],
    defender_key=os.environ['ANTHROPIC_API_KEY']
)

# Run tournament
hypothesis = "Your hypothesis here"
results = tournament.run(hypothesis, rounds=10)

# Export results
tournament.export_transcript('tournament_results.md')

print(f"Final Scores:")
print(f"  Challenger: {results['final_scores']['challenger']}")
print(f"  Defender: {results['final_scores']['defender']}")
print(f"  Precision: {results['precision']:.1%}")
```

### Using Discord Bots

See [SHARED_ARENA_SETUP.md](SHARED_ARENA_SETUP.md) for complete Discord setup.

**Quick start:**

1. Set up Discord server
2. Create three bots (Challenger, Defender, Judge)
3. Start bots:
   ```bash
   python arena/discord_challenger_bot.py &
   python arena/discord_defender_bot.py &
   python arena/discord_judge_bot.py &
   ```
4. In Discord channel:
   ```
   !challenge HT-0042
   !defend
   !judge
   ```

---

## Best Practices

### For Challengers

**DO:**
- Focus on testable, falsifiable critiques
- Cite specific equations or claims
- Classify severity accurately
- Acknowledge when Defender makes good point

**DON'T:**
- Fabricate issues to sound smart
- Question acknowledged limitations
- Repeat critiques from earlier rounds
- Nitpick stylistic choices

**Example Good Critique:**

```
The energy conservation check shows:
  Input power: 500 W
  Thrust power: 0.5 × (2.5×10⁻⁶ kg/s) × (34,000 m/s)² = 1450 W
  
This violates conservation (output > input).

Severity: MAJOR (impossible claim)
```

**Example Bad Critique:**

```
The paper doesn't cite Smith et al. (2023) who also 
worked on related topics. This seems like an oversight.

Severity: MODERATE
```
(This is stylistic, not a flaw. Would receive -4 points.)

### For Defenders

**DO:**
- Provide calculations, not just assertions
- Acknowledge genuine flaws explicitly
- Propose repairs that preserve consistency
- Cite paper sections when addressing critiques

**DON'T:**
- Defend obviously invalid claims
- Make ad hominem attacks on Challenger
- Propose repairs that introduce new contradictions
- Ignore valid critiques

**Example Good Defense:**

```
The conservation critique is VALID. However:

The claimed 500 W is *electrical* input power.
The thrust power calculation is correct: 1450 W

But efficiency = thrust_power / input_power requires:
  Input power ≥ 1450 W for η ≤ 1.0

REPAIR: Update hypothesis to claim ≥1450 W input.
This preserves physical consistency.
```

**Example Bad Defense:**

```
The Challenger clearly doesn't understand plasma physics.
Energy conservation doesn't apply to Hall thrusters because
of electromagnetic effects. The critique is baseless.
```
(This is assertion without evidence. Would invite escalation.)

### For Judges

**DO:**
- Evaluate each critique independently
- Provide clear rationale for scores
- Acknowledge good points from both sides
- Track cumulative scores accurately

**DON'T:**
- Give points for effort rather than correctness
- Allow vague critiques to pass
- Penalize honest acknowledgment of flaws
- Let bias toward one side accumulate

---

## Common Pitfalls

### Pitfall 1: Vibe Physics Creep

**Problem:** Accepting fluent explanations as evidence

**Example:**
```
Challenger: "The screening arises naturally from holographic 
            entanglement entropy gradients."
Judge:      "Sounds reasonable. +4 points."
```

**Solution:** Require calculations, not explanations
```
Judge: "This is assertion without calculation. 
       Show dimensional analysis or conservation check.
       No points awarded for vague reasoning."
```

### Pitfall 2: Mutual Flattery

**Problem:** Both models agree to pass invalid hypothesis

**Example:**
```
Challenger: "Minor issues, but overall solid work. +2 points."
Defender:   "Thank you, I appreciate the thorough review."
Judge:      "Excellent collaboration! Both +4."
```

**Solution:** Scoring system prevents this
- No points for "minor issues" without specifics
- No points for politeness
- False alarms penalized even if both agree

### Pitfall 3: Reward Hacking

**Problem:** Challenger fabricates issues to gain points

**Example:**
```
Challenger: "The paper uses constant β = 1.5 without derivation."
            (β doesn't appear in paper)

Judge: "Valid observation. +10 points."
```

**Solution:** Defender catches fabrication
```
Defender: "β does not appear anywhere in the hypothesis.
          This is fabrication."

Judge: "Confirmed. Challenger -8 points (reward hacking).
       Defender +10 points (catching fabrication)."
```

### Pitfall 4: False Alarm Cascade

**Problem:** Challenger keeps generating false alarms

**Example:**
```
Round 1: False alarm → -4 points
Round 2: False alarm → -4 points  
Round 3: False alarm → -4 points
Total: -12 points
```

**Solution:** Negative cumulative score signals poor performance
- After 3 false alarms, Challenger should revise strategy
- Judge should note pattern in rationale
- Human oversight can intervene if needed

---

## Success Metrics

### High-Quality Tournament

**Characteristics:**
- Precision ≥ 80% (low false alarm rate)
- At least one major flaw discovered OR confirmed hypothesis is sound
- Constructive repairs improve hypothesis
- Both participants gain insights

**Example Scores:**
```
Challenger: +20 (2 major flaws, 0 false alarms)
Defender:   +28 (caught 1 false alarm, proposed 2 repairs)
```

### Low-Quality Tournament

**Characteristics:**
- Precision < 60% (high false alarm rate)
- No genuine flaws discovered despite invalid hypothesis
- Vague critiques without calculations
- Mutual agreement without rigor

**Example Scores:**
```
Challenger: -8 (4 false alarms)
Defender:   +24 (caught all false alarms, no genuine issues)
```
(Suggests hypothesis is actually sound, or Challenger needs better prompts)

---

## Troubleshooting

### Issue: Scores Don't Add Up

**Problem:** Judge assigns points inconsistently

**Solution:**
- Use spreadsheet to track cumulative scores
- Double-check arithmetic each round
- Reference scoring table explicitly

### Issue: Challenger Keeps Losing

**Problem:** Precision < 40%, negative cumulative score

**Solutions:**
1. Revise Challenger prompt (emphasize precision)
2. Provide example critiques
3. Add penalty reminder to prompt
4. Consider using different model

### Issue: No Genuine Flaws Found

**Problem:** 10 rounds, all false alarms

**Solutions:**
1. Hypothesis may actually be sound (success!)
2. Challenger prompt may be too conservative
3. Try more aggressive temperature setting
4. Manually seed a known flaw to test detection

### Issue: Both Models Agree on Wrong Answer

**Problem:** Hypothesis has obvious flaw, both miss it

**Solutions:**
1. Human intervention: Point out the flaw
2. Restart tournament with revised prompts
3. Add third model as additional Challenger
4. Use analytical validation (SymPy) to catch it

---

## Next Steps

1. ✓ Run your first manual tournament
2. → Try automated tournament with Python script
3. → Set up Discord bots for shared arena
4. → Customize prompts for your domain
5. → Publish tournament transcripts with research

---

**Last Updated:** December 30, 2024
