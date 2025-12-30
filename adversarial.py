"""
Adversarial Tournament System

Implements the tournament scoring and validation logic for the adversarial-augmented
architecture. Two LLMs (Challenger and Defender) compete to identify and fix errors,
with a Judge scoring their performance.

Key Features:
- Tournament scoring system (+10 valid flaws, -8 fabrication penalty)
- Feedback routing based on error type
- Transcript generation for research documentation
- No API keys stored - user provides via environment variables

Usage:
    from adversarial import AdversarialTournament
    
    tournament = AdversarialTournament(
        challenger_key=os.environ['OPENAI_API_KEY'],
        defender_key=os.environ['ANTHROPIC_API_KEY']
    )
    
    results = tournament.run(hypothesis, rounds=10)
"""

import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class CritiqueType(Enum):
    """Types of critiques that can be generated"""
    DIMENSIONAL_ERROR = "dimensional_error"
    CONSERVATION_VIOLATION = "conservation_violation"
    FABRICATED_PARAMETER = "fabricated_parameter"
    NUMERICAL_HALLUCINATION = "numerical_hallucination"
    LOGICAL_CONFABULATION = "logical_confabulation"
    SCOPE_VIOLATION = "scope_violation"
    FALSE_ALARM = "false_alarm"


class Decision(Enum):
    """Possible outcomes from adversarial checkpoint"""
    PASS = "pass"
    PASS_WITH_REPAIR = "pass_with_repair"
    REJECT = "reject"
    ESCALATE = "escalate"


@dataclass
class Critique:
    """Structured critique from Challenger"""
    type: CritiqueType
    description: str
    severity: str  # "minor", "moderate", "major"
    specific_claim: str
    evidence: str


@dataclass
class Defense:
    """Structured response from Defender"""
    addresses_critique: bool
    refutation: Optional[str]
    repair: Optional[str]
    preserves_consistency: bool


@dataclass
class Scoring:
    """Tournament round scoring"""
    challenger_points: int
    defender_points: int
    rationale: str
    decision: Decision


class AdversarialTournament:
    """
    Manages adversarial tournament between Challenger and Defender LLMs.
    
    This class coordinates the tournament, tracks scores, and generates
    transcripts. It does NOT store API keys - user must provide them.
    
    Args:
        challenger_key: API key for Challenger LLM (e.g., OpenAI)
        defender_key: API key for Defender LLM (e.g., Anthropic)
        judge_key: Optional separate API key for Judge
    """
    
    def __init__(
        self,
        challenger_key: Optional[str] = None,
        defender_key: Optional[str] = None,
        judge_key: Optional[str] = None
    ):
        # Validate that keys are provided
        if not challenger_key:
            challenger_key = os.environ.get('OPENAI_API_KEY')
        if not defender_key:
            defender_key = os.environ.get('ANTHROPIC_API_KEY')
        if not judge_key:
            judge_key = os.environ.get('GOOGLE_API_KEY')
            
        if not challenger_key or not defender_key:
            raise ValueError(
                "API keys required. Set environment variables:\n"
                "  OPENAI_API_KEY (Challenger)\n"
                "  ANTHROPIC_API_KEY (Defender)\n"
                "Or pass directly to __init__()"
            )
        
        self.challenger_key = challenger_key
        self.defender_key = defender_key
        self.judge_key = judge_key or defender_key  # Fallback to defender
        
        self.scores = {
            'challenger': 0,
            'defender': 0
        }
        
        self.transcript = []
        self.round_results = []
    
    def run(
        self,
        hypothesis: str,
        rounds: int = 10
    ) -> Dict:
        """
        Run complete tournament for given hypothesis.
        
        Args:
            hypothesis: The hypothesis to validate
            rounds: Number of tournament rounds
            
        Returns:
            Dictionary containing:
                - final_scores: Dict with challenger/defender totals
                - round_results: List of per-round outcomes
                - transcript: Full conversation history
                - precision: Error detection precision
        """
        print(f"Starting {rounds}-round tournament...")
        print(f"Hypothesis: {hypothesis}\n")
        
        self.add_to_transcript("HYPOTHESIS", hypothesis)
        
        for round_num in range(1, rounds + 1):
            print(f"\n{'='*60}")
            print(f"ROUND {round_num}")
            print(f"{'='*60}\n")
            
            result = self.run_round(hypothesis, round_num)
            self.round_results.append(result)
            
            print(f"\nRound {round_num} Complete")
            print(f"  Challenger: {result.challenger_points:+d} points")
            print(f"  Defender: {result.defender_points:+d} points")
            print(f"  Decision: {result.decision.value}")
        
        return self.generate_results()
    
    def run_round(
        self,
        hypothesis: str,
        round_num: int
    ) -> Scoring:
        """
        Execute single tournament round.
        
        Args:
            hypothesis: Hypothesis being validated
            round_num: Current round number
            
        Returns:
            Scoring object with points and decision
        """
        # Step 1: Challenger generates critique
        critique = self.challenger_critique(hypothesis, round_num)
        self.add_to_transcript(f"CHALLENGER (Round {round_num})", critique)
        
        # Step 2: Defender responds
        defense = self.defender_response(hypothesis, critique, round_num)
        self.add_to_transcript(f"DEFENDER (Round {round_num})", defense)
        
        # Step 3: Judge scores the exchange
        scoring = self.judge_round(critique, defense, round_num)
        self.add_to_transcript(f"JUDGE (Round {round_num})", scoring)
        
        # Update cumulative scores
        self.scores['challenger'] += scoring.challenger_points
        self.scores['defender'] += scoring.defender_points
        
        return scoring
    
    def challenger_critique(
        self,
        hypothesis: str,
        round_num: int
    ) -> str:
        """
        Generate critique from Challenger LLM.
        
        NOTE: This is a template method. In production, this would call
        the actual LLM API. For now, returns template critique.
        
        For real implementation, see arena/discord_challenger_bot.py
        """
        # Template critique for demonstration
        # In production, replace with actual API call:
        #   response = openai.ChatCompletion.create(...)
        
        return f"""[CHALLENGER - Round {round_num}]

I identify the following issues with the hypothesis:

1. **Dimensional consistency check needed**
   Verify that all equations have consistent units across terms.

2. **Conservation law compliance**  
   Ensure energy-momentum conservation is satisfied.

3. **Parameter justification**
   Verify all parameters have derivational or empirical support.

Awaiting validation against analytical checks.
"""
    
    def defender_response(
        self,
        hypothesis: str,
        critique: str,
        round_num: int
    ) -> str:
        """
        Generate defense from Defender LLM.
        
        NOTE: Template method. In production, calls actual LLM API.
        For real implementation, see arena/discord_defender_bot.py
        """
        return f"""[DEFENDER - Round {round_num}]

Addressing the Challenger's critiques:

1. **Dimensional consistency:** VERIFIED
   All terms in equations have consistent units.
   
2. **Conservation laws:** CONFIRMED
   Energy-momentum conservation satisfied via Klein-Gordon structure.
   
3. **Parameters:** ACKNOWLEDGED AS LIMITATION
   Hypothesis explicitly states phenomenological approach.

The critiques are either false alarms (#1, #2) or acknowledged 
limitations (#3). No repairs needed.
"""
    
    def judge_round(
        self,
        critique: str,
        defense: str,
        round_num: int
    ) -> Scoring:
        """
        Judge scores the Challenger-Defender exchange.
        
        NOTE: Template method. In production, calls actual LLM API.
        For real implementation, see arena/discord_judge_bot.py
        """
        # Simplified scoring for demonstration
        # In production, Judge LLM analyzes full exchange and assigns points
        
        return Scoring(
            challenger_points=2,  # Some valid observations
            defender_points=12,   # Mostly false alarms caught
            rationale=(
                "Challenger raised reasonable questions but most were "
                "false alarms. Defender provided thorough refutations."
            ),
            decision=Decision.PASS
        )
    
    def add_to_transcript(
        self,
        role: str,
        content: str
    ):
        """Add entry to tournament transcript"""
        self.transcript.append({
            'role': role,
            'content': content
        })
    
    def generate_results(self) -> Dict:
        """
        Generate final tournament results.
        
        Returns:
            Complete results including scores, precision, transcript
        """
        # Calculate precision
        valid_detections = sum(
            1 for r in self.round_results 
            if r.challenger_points > 0
        )
        false_alarms = sum(
            1 for r in self.round_results 
            if r.challenger_points < 0
        )
        
        total_critiques = valid_detections + false_alarms
        precision = valid_detections / total_critiques if total_critiques > 0 else 0
        
        return {
            'final_scores': self.scores,
            'round_results': self.round_results,
            'transcript': self.transcript,
            'precision': precision,
            'valid_detections': valid_detections,
            'false_alarms': false_alarms
        }
    
    def export_transcript(self, filename: str):
        """
        Export full tournament transcript to Markdown file.
        
        Args:
            filename: Path to output file (e.g., 'tournament_results.md')
        """
        with open(filename, 'w') as f:
            f.write("# Tournament Transcript\n\n")
            f.write(f"**Final Scores:**\n")
            f.write(f"- Challenger: {self.scores['challenger']}\n")
            f.write(f"- Defender: {self.scores['defender']}\n\n")
            
            f.write("---\n\n")
            
            for entry in self.transcript:
                f.write(f"## {entry['role']}\n\n")
                f.write(f"{entry['content']}\n\n")
                f.write("---\n\n")
        
        print(f"Transcript exported to: {filename}")


class FeedbackRouter:
    """
    Routes rejected hypotheses to appropriate loop based on error type.
    
    Implements formal decision logic from ARCHITECTURE.md:
    - Adversarial feedback (local): Returns to previous loop
    - Human routing (global): Can return to any loop
    """
    
    @staticmethod
    def route_adversarial(
        hypothesis: Dict,
        critique: Critique,
        current_loop: int
    ) -> Tuple[Decision, Optional[int]]:
        """
        Adversarial checkpoint routing (local feedback).
        
        Args:
            hypothesis: The hypothesis being validated
            critique: Challenger's critique
            current_loop: Current loop number (1-4)
            
        Returns:
            Tuple of (decision, target_loop)
        """
        if critique.type == CritiqueType.FALSE_ALARM:
            return (Decision.PASS, None)
        
        if critique.type == CritiqueType.SCOPE_VIOLATION:
            return (Decision.ESCALATE, None)
        
        # Check if repair is possible
        if FeedbackRouter._can_repair(hypothesis, critique):
            repair = FeedbackRouter._propose_repair(hypothesis, critique)
            if repair['preserves_consistency']:
                return (Decision.PASS_WITH_REPAIR, None)
        
        # Cannot repair - return to previous loop
        target_loop = max(1, current_loop - 1)
        return (Decision.REJECT, target_loop)
    
    @staticmethod
    def route_human(
        hypothesis: Dict,
        root_cause: str
    ) -> Optional[int]:
        """
        Human routing (global feedback).
        
        Args:
            hypothesis: The hypothesis being validated
            root_cause: Identified root cause of failure
            
        Returns:
            Target loop number (1-4) or None for terminal rejection
        """
        routing_map = {
            'flawed_hypothesis_generation': 1,
            'missed_analytical_constraint': 2,
            'simulation_setup_error': 3,
            'not_novel': None,
            'unsafe': None,
            'infeasible': None
        }
        
        return routing_map.get(root_cause, 1)  # Default to regeneration
    
    @staticmethod
    def _can_repair(hypothesis: Dict, critique: Critique) -> bool:
        """Check if hypothesis can be repaired given critique"""
        # Simplified check - in production, would involve deeper analysis
        repairable_types = {
            CritiqueType.DIMENSIONAL_ERROR,
            CritiqueType.NUMERICAL_HALLUCINATION
        }
        return critique.type in repairable_types
    
    @staticmethod
    def _propose_repair(hypothesis: Dict, critique: Critique) -> Dict:
        """Propose repair for hypothesis given critique"""
        # Simplified repair - in production, would call Defender LLM
        return {
            'repaired_hypothesis': hypothesis,
            'preserves_consistency': True,
            'changes': [f"Fixed {critique.type.value}"]
        }


# Example usage
if __name__ == "__main__":
    # This is a demonstration - actual implementation requires API keys
    
    print("Adversarial Tournament System")
    print("="*60)
    print("\nNOTE: This is a template demonstration.")
    print("For real tournaments, set environment variables:")
    print("  export OPENAI_API_KEY='your-key'")
    print("  export ANTHROPIC_API_KEY='your-key'")
    print("\nOr use the Discord/Slack bot implementations in arena/")
    print("="*60)
    
    # Template demonstration
    hypothesis = "Gravitational screening R(k) = 1/(1 + λ²k²) with λ ~ 5 Mpc"
    
    print(f"\nHypothesis: {hypothesis}")
    print("\nTo run actual tournament:")
    print("  from adversarial import AdversarialTournament")
    print("  tournament = AdversarialTournament()")
    print("  results = tournament.run(hypothesis, rounds=10)")
