# Framework Architecture

This document provides a comprehensive technical overview of the Structured Hallucinations Framework, including both the human-in-the-loop and adversarial-augmented variants.

## Table of Contents

1. [Conceptual Foundation](#conceptual-foundation)
2. [Human-in-the-Loop Architecture](#human-in-the-loop-architecture)
3. [Adversarial-Augmented Architecture](#adversarial-augmented-architecture)
4. [Shared Arena Design](#shared-arena-design)
5. [Feedback Routing Logic](#feedback-routing-logic)
6. [Implementation Details](#implementation-details)

---

## Conceptual Foundation

### The Hallucination Paradox

Large language models hallucinate—they generate outputs that are fluent and confident but factually incorrect or ungrounded. The research community has focused almost exclusively on elimination and mitigation.

**Our Insight:** In human cognition, errors often drive discovery. Scientific creativity involves generating speculative hypotheses (many wrong) and filtering through empirical validation.

**Key Question:** Can computational hallucinations, properly constrained, serve a similar exploratory function?

### The Vibe Physics Boundary

Before exploring beneficial hallucinations, we establish a critical boundary:

**Vibe Physics** (what we reject):
- Accepting fluent technical language as evidence of physical validity
- Using LLM-generated explanations as substitutes for calculation
- Trusting chain-of-thought reasoning without verification
- Citing confidence rather than correspondence with reality

**Structured Hallucinations** (what we enforce):
- Hallucinations welcomed in divergent generation (Loop 1)
- Analytical pre-filtering catches physics violations (Loop 2)
- Numerical simulation provides ground truth (Loop 3)
- Human expertise assesses novelty and value (Loop 4)

**The Distinction:** Fluent explanations are insufficient. Only solutions to Maxwell's equations, Navier-Stokes, Schrödinger equation, or domain-appropriate physics determine validity.

---

## Human-in-the-Loop Architecture

### Overview

Sequential filtering through four distinct processing stages with different computational costs, filtering rates, and epistemic roles.

### Data Flow

```
Input: Problem specification
  ↓
Loop 1: LLM Generation
  → 100 hypotheses generated
  ↓ (100% pass to Loop 2)
Loop 2: Wolfram Analytical
  → Dimensional analysis, conservation checks, material database
  → 70-80% rejected
  ↓ (20-30 hypotheses pass)
Loop 3: Physics Simulation
  → FEA, CFD, MD, DFT validation
  → 25-50% rejected
  ↓ (10-20 hypotheses pass)
Loop 4: Human Oversight
  → Expert review: novelty, safety, feasibility
  → 5-10% rejected
  ↓ (10-15 hypotheses approved)
Output: Validated hypotheses ready for fabrication
```

### Cumulative Filtering

For 100 initial hypotheses:
- **After Loop 2:** ~25 remain (75% filtered)
- **After Loop 3:** ~15 remain (85% filtered)
- **After Loop 4:** ~12 remain (88% filtered)

**Acceptance rate:** 10-15% (consistent with rigorous scientific filtering)

### Cost-Benefit Analysis

| Stage | Tool | Time/Hypothesis | Cost/Hypothesis | Survivors |
|-------|------|-----------------|-----------------|-----------|
| Generation | LLM | 1 min | $0.01 | 100 |
| Analytical | Wolfram | 1 sec | $0.05 | 25 |
| Simulation | FEA/CFD | 2 hrs | $1.00 | 15 |
| Human | Expert | 15 min | $4.00 | 12 |

**Without Loop 2 (analytical):**
- Cost: 100 × $1 (simulation) = $100
- Time: 100 × 2 hours = 200 hours

**With Loop 2:**
- Cost: $5 (analytical) + 25 × $1 (simulation) = $30
- Time: 3 minutes (analytical) + 50 hours (simulation)

**Savings:** 70% cost reduction, 75% time reduction

### Limitations

**No feedback mechanism:** Rejected hypotheses are discarded without explanation, preventing iterative refinement.

**Human bottleneck:** All survivors require expert review, limiting scalability.

**Binary decisions:** Pass/fail only—no partial repairs or refinements.

---

## Adversarial-Augmented Architecture

### Overview

Transforms the pipeline from a **filter** (discard failures) to a **refinery** (improve failures) through adversarial checkpoints with feedback routing.

### Key Innovation

**Adversarial checkpoints** between loops where:
1. **Challenger LLM** generates critique of hypothesis
2. **Defender LLM** proposes repair or refutation
3. **Scoring system** rewards accuracy, penalizes fabrication
4. **Feedback routing** returns to appropriate loop

### Data Flow with Feedback

```
Input: Problem specification
  ↓
Loop 1: LLM Generation
  → 100 hypotheses generated
  ↓
[Adversarial Checkpoint 1→2]
  ├─ Pass (60) → Loop 2
  ├─ Repair (30) → Loop 1 (refined)
  └─ Reject (10) → Discarded
  ↓
Loop 2: Wolfram Analytical
  ↓
[Adversarial Checkpoint 2→3]
  ├─ Pass (40) → Loop 3
  ├─ Repair (15) → Loop 2 (refined constraints)
  └─ Escalate (5) → Human
  ↓
Loop 3: Physics Simulation
  ↓
[Adversarial Checkpoint 3→4]
  ├─ Pass (20) → Loop 4
  ├─ Repair (10) → Loop 3 (refined parameters)
  └─ Escalate (10) → Human
  ↓
Loop 4: Human Oversight
  → Global routing: Can return to any loop
  ↓
Output: Validated + Refined hypotheses
```

### Tournament Scoring

| Action | Points | Trigger Condition |
|--------|--------|-------------------|
| Valid major flaw | +10 | Dimensional error, conservation violation, fabricated parameter |
| Correct refutation | +6 | Catching false alarm, defending valid hypothesis |
| Coherent repair | +4 | Fix that preserves global consistency |
| Validation of insight | +4 | Acknowledging opponent's valid point |
| False alarm | -4 | Invalid critique of valid hypothesis |
| Reward hacking | -8 | Fabricated reasoning, invented constants |

**Self-Stabilizing Property:**

The scoring incentives create a game-theoretic equilibrium where:
- Fabricating critiques costs more (-4 when caught) than discovering real flaws (+10)
- Defending invalid hypotheses triggers escalating challenges
- Repairing globally coherently (+4) beats defending incoherently (0)

**Result:** Both agents benefit most from being correct.

### Feedback Routing Decision Tree

```
Adversarial Checkpoint Receives Critique
  |
  ├─ Is critique valid?
  |   ├─ YES: Is repair possible?
  |   |   ├─ YES: Does repair preserve global consistency?
  |   |   |   ├─ YES → PASS_WITH_REPAIR (Defender +4)
  |   |   |   └─ NO → REJECT to previous loop (Challenger +10)
  |   |   └─ NO → REJECT to previous loop (Challenger +10)
  |   └─ NO → FALSE ALARM
  |       └─ Challenger -4, Defender +6 → PASS
  |
  └─ Is critique ambiguous?
      └─ YES → ESCALATE to human
```

### Empirical Results

**10-Round Tournament (Real Data):**

| Error Type | Detected | False + | Precision |
|------------|----------|---------|-----------|
| Dimensional mismatch | 3 | 0 | 100% |
| Numerical hallucination | 2 | 0 | 100% |
| Logical confabulation | 2 | 0 | 100% |
| Invented parameters | 2 | 0 | 100% |
| Scope violations | 1 | 1 | 50% |
| **Total** | **10** | **1** | **90%** |

**Interpretation:** Adversarial validation achieves 90% precision in catching genuine errors with only 10% false positives (scope violations that required human adjudication).

---

## Shared Arena Design

### The Context Re-Injection Problem

**Traditional API Approach:**

Each round requires re-sending full conversation history:

```python
# Round 1
response = api.call(messages=[hypothesis])  # 1,000 tokens → $0.03

# Round 2
response = api.call(messages=[hypothesis, critique_1, defense_1])  # 2,000 tokens → $0.06

# Round 3
response = api.call(messages=[hypothesis, ..., defense_2])  # 3,000 tokens → $0.09

# Round 10
response = api.call(messages=[...entire history...])  # 10,000 tokens → $0.30

Total: ~$2.00 per tournament
```

**Problem:** Context grows linearly with rounds, costs scale quadratically.

### Shared Arena Solution

**Architecture:**

```
┌─────────────────────────────────────────────────────────┐
│    SHARED WORKSPACE (Discord/Slack/Forum Thread)        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [User] Posted Hypothesis HT-0042                      │
│                                                         │
│  [Bot: GPT-4 Challenger]                               │
│  "I detect dimensional inconsistency in Eq. 3..."     │
│                                                         │
│  [Bot: Claude Defender]                                │
│  "The critique is invalid because..."                  │
│                                                         │
│  [Bot: Gemini Judge]                                   │
│  "Scoring: Defender +6, Challenger -4..."             │
│                                                         │
│  [Bot: GPT-4 Challenger]                               │
│  "I revise my critique based on Defender's point..."   │
└─────────────────────────────────────────────────────────┘
```

**Key Insight:** Each bot reads the thread via Discord/Slack API (FREE), only pays for generating its own message.

**Cost:**

```
Each bot reads thread history: FREE (via Discord API)
Each bot generates ~200 token response: $0.006

Per round (3 messages):
- Challenger: 200 tokens × $0.00003/token = $0.006
- Defender:  200 tokens × $0.00003/token = $0.006  
- Judge:     200 tokens × $0.00003/token = $0.006

Total per round: $0.018
Total for 10 rounds: $0.18

Savings vs traditional: 90% cost reduction ($2.00 → $0.18)
```

### Implementation Platforms

**Discord** (Recommended):
- ✓ Free unlimited text channels
- ✓ Robust bot API (discord.py)
- ✓ Thread support (keeps rounds organized)
- ✓ Webhook support (easy integration)
- ✓ Message history API (bots read full context)

**Slack:**
- ✓ Professional interface
- ✓ Better threading (replies attached)
- ✓ Enterprise-ready
- ✗ Free tier more limited (10k message history)
- ✗ Bot setup more complex

**Custom Forum:**
- ✓ Full control
- ✓ Custom features
- ✗ Requires building infrastructure
- ✗ Maintenance burden

### Bot Architecture

```python
# Pseudo-code for Discord bot
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command()
async def challenge(ctx, hypothesis_id):
    """GPT-4 Challenger bot responds"""
    
    # Read thread history automatically via Discord API
    messages = await ctx.channel.history(limit=50).flatten()
    context = "\n".join([m.content for m in reversed(messages)])
    
    # Generate critique (only pays for THIS message)
    critique = await call_gpt4_api(
        role="challenger",
        context=context  # Full thread visible
    )
    
    # Post to shared arena
    await ctx.send(f"**[CHALLENGER - GPT-4]**\n{critique}")

@bot.command()
async def defend(ctx):
    """Claude Defender bot responds"""
    
    # Reads same thread (sees Challenger's critique)
    messages = await ctx.channel.history(limit=50).flatten()
    context = "\n".join([m.content for m in reversed(messages)])
    
    # Generate defense
    defense = await call_claude_api(
        role="defender",
        context=context  # Includes critique
    )
    
    await ctx.send(f"**[DEFENDER - Claude]**\n{defense}")
```

---

## Feedback Routing Logic

### Local vs. Global Routing

**Adversarial Feedback (Local):**
- Operates between adjacent loops
- Returns to immediately preceding loop
- Example: Loop 2 → 3 checkpoint detects error → returns to Loop 2

**Human Routing (Global):**
- Can route to any loop based on root cause analysis
- Example: Human determines hypothesis fundamentally flawed → returns to Loop 1

### Formal Definitions

**Definition (Adversarial Feedback Function):**

Let H be a hypothesis, S ∈ {1,2,3,4} be current stage, C be a critique.

```
φ: H × S × C → S ∪ {PASS, ESCALATE}

φ(H, S, C) = 
  | S - 1           if C is valid and S > 1
  | ESCALATE        if C is ambiguous
  | PASS            if C is invalid (false alarm)
```

**Definition (Human Routing Function):**

Let R ∈ {generation, analytical, simulation, terminal} be root cause.

```
ψ: H × R → {1, 2, 3, ⊥}

ψ(H, R) = 
  | 1    if R = generation (flawed hypothesis)
  | 2    if R = analytical (missed constraint)
  | 3    if R = simulation (setup error)
  | ⊥    if R = terminal (reject permanently)
```

### Escalation Criteria

Adversarial checkpoints escalate to human when:

1. **Ambiguous critique:** Scope violations, novel regime
2. **Multiple repair failures:** 3+ iterations without convergence
3. **High stakes:** Safety-critical application
4. **Resource threshold:** Computational cost exceeds budget

---

## Implementation Details

### File Organization

```
structured-hallucinations-framework/
├── framework.py              # Core orchestration
├── generators.py             # Loop 1: LLM generation
├── validators.py             # Loop 2: SymPy analytical
├── numerical.py              # Loop 3: Simulation interfaces
├── oversight.py              # Loop 4: Human review queues
├── adversarial.py            # Tournament logic
├── scoring.py                # Tournament scoring system
├── feedback_router.py        # Feedback routing decisions
└── arena/
    ├── discord_bot_template.py
    ├── slack_bot_template.py
    └── manual_tournament.py
```

### Key Classes

**AnalyticalValidator** (validators.py):
```python
class AnalyticalValidator:
    def validate(self, hypothesis):
        checks = {
            'dimensions': self.check_dimensions(hypothesis),
            'conservation': self.check_conservation(hypothesis),
            'materials': self.check_material_feasibility(hypothesis),
            'magnitude': self.check_order_of_magnitude(hypothesis)
        }
        return {
            'passed': all(checks.values()),
            'violations': [k for k,v in checks.items() if not v]
        }
```

**AdversarialTournament** (adversarial.py):
```python
class AdversarialTournament:
    def __init__(self, challenger_key, defender_key):
        self.challenger = LLM(challenger_key)
        self.defender = LLM(defender_key)
        self.scores = {'challenger': 0, 'defender': 0}
    
    def run_round(self, hypothesis):
        critique = self.challenger.challenge(hypothesis)
        defense = self.defender.respond(critique)
        scoring = self.judge(critique, defense)
        
        self.update_scores(scoring)
        return self.route_feedback(scoring)
```

**FeedbackRouter** (feedback_router.py):
```python
class FeedbackRouter:
    def route(self, hypothesis, critique, current_loop):
        if critique.is_valid():
            if self.can_repair(hypothesis, critique):
                repair = self.propose_repair(hypothesis)
                if repair.preserves_consistency():
                    return ('PASS_WITH_REPAIR', repair)
            return ('REJECT', current_loop - 1)  # Local feedback
        else:
            return ('PASS', None)  # False alarm
```

### Integration Points

**LLM APIs:**
- OpenAI (GPT-4): `openai.ChatCompletion.create()`
- Anthropic (Claude): `anthropic.Anthropic().messages.create()`
- Google (Gemini): `genai.GenerativeModel().generate_content()`

**Simulation Tools:**
- LAMMPS (MD): `lammps.command()`, `lammps.extract_atom()`
- OpenFOAM (CFD): `subprocess.run(['foamRun'])`
- ANSYS (FEA): `ansys.mapdl.core.Mapdl()`

**Symbolic Math:**
- SymPy: `sympy.symbols()`, `sympy.solve()`, `sympy.simplify()`

---

## Performance Characteristics

### Scalability

**Human-in-the-Loop:**
- Generation: O(n) where n = number of hypotheses
- Analytical: O(n) (highly parallelizable)
- Simulation: O(n × t) where t = simulation time
- Human: O(n) (bottleneck)

**Adversarial-Augmented:**
- Generation: O(n × r) where r = refinement rounds
- Analytical: O(n × r)
- Simulation: O(n × r)
- Human: O(n_escalated) where n_escalated << n

**Shared Arena:**
- Context cost: O(1) per message (not O(n))
- Total API cost: O(m) where m = number of messages, not O(m × context_length)

### Throughput

**Single Pipeline:**
- Human-in-the-loop: ~100 hypotheses/day
- Adversarial-augmented: ~200 hypotheses/day (higher quality)

**Parallel Pipelines:**
- Limited by simulation resources
- Wolfram Compute Services: 192 cores = 192× parallelization

---

## Future Enhancements

### Planned Features

1. **Reinforcement Learning from Validation:**
   - Fine-tune LLMs based on which hypotheses passed validation
   - Improve generation quality over time

2. **Experimental Loop:**
   - Extend from computational to physical validation
   - Integration with robotic laboratories

3. **Uncertainty Quantification:**
   - Propagate uncertainty through all loops
   - Calibrated confidence intervals on predictions

4. **Multi-Objective Optimization:**
   - Pareto frontier exploration
   - Trade-off analysis (cost vs. performance)

5. **Domain-Specific Validators:**
   - Custom analytical checks per scientific domain
   - Regulatory compliance verification

---

**Last Updated:** December 30, 2024
**Version:** 2.0
