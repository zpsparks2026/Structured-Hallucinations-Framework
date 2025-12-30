"""
Loop 1: Divergent Hypothesis Generation
Generates multiple hypotheses from a scientific prompt
"""

from typing import List, Dict, Any
import random


class HypothesisGenerator:
    """
    Generates scientific hypotheses for validation.
    
    In production, this would interface with an LLM API.
    This implementation uses rule-based generation for demonstration.
    """
    
    def __init__(self):
        """Initialize generator with example hypothesis templates"""
        # Template-based generation for demonstration
        # In production: replace with LLM API calls
        self.thermal_templates = [
            {
                'description': 'Increase surface area by {factor}x through fin addition',
                'equation': 'Q = h * A * ΔT',
                'parameters': {'h': 1.0, 'A': '{area_multiplier}', 'ΔT': 1.0},
                'type': 'geometric'
            },
            {
                'description': 'Modify material thermal conductivity by {percent}%',
                'equation': 'Q = k * A * ΔT / L',
                'parameters': {'k': '{conductivity_factor}', 'A': 1.0, 'ΔT': 1.0, 'L': 1.0},
                'type': 'material'
            },
            {
                'description': 'Alter flow rate to increase convection coefficient',
                'equation': 'h = C * v^n',
                'parameters': {'C': 1.0, 'v': '{velocity_factor}', 'n': 0.8},
                'type': 'fluid'
            },
            {
                'description': 'Add phase change material for latent heat storage',
                'equation': 'Q_total = m * c * ΔT + m * L_f',
                'parameters': {'m': 1.0, 'c': 1.0, 'ΔT': 1.0, 'L_f': '{latent_heat}'},
                'type': 'phase_change'
            },
            {
                'description': 'Implement radiative cooling with emissivity enhancement',
                'equation': 'Q_rad = ε * σ * A * (T^4 - T_surr^4)',
                'parameters': {'ε': '{emissivity}', 'σ': 5.67e-8, 'A': 1.0, 'T': 300, 'T_surr': 250},
                'type': 'radiation'
            }
        ]
        
        self.structural_templates = [
            {
                'description': 'Reduce cross-section by {percent}% for weight savings',
                'equation': 'σ = F / A',
                'parameters': {'F': 1.0, 'A': '{area_factor}'},
                'type': 'geometric',
                'constraint': 'σ < σ_yield'
            },
            {
                'description': 'Add reinforcement ribs at {spacing} mm intervals',
                'equation': 'I = b * h^3 / 12',
                'parameters': {'b': 1.0, 'h': '{height_factor}'},
                'type': 'reinforcement'
            }
        ]
    
    def generate(self, prompt: str, num_hypotheses: int = 5) -> List[Dict[str, Any]]:
        """
        Generate hypotheses based on prompt.
        
        Args:
            prompt: Scientific question or optimization goal
            num_hypotheses: Number of hypotheses to generate
            
        Returns:
            List of hypothesis dictionaries with equations and parameters
        """
        hypotheses = []
        
        # Detect domain from prompt (simple keyword matching)
        domain = self._detect_domain(prompt)
        
        if domain == 'thermal':
            templates = self.thermal_templates
        elif domain == 'structural':
            templates = self.structural_templates
        else:
            templates = self.thermal_templates  # Default
        
        # Generate hypotheses from templates with randomization
        for i in range(min(num_hypotheses, len(templates))):
            template = templates[i]
            hypothesis = self._instantiate_template(template, i)
            hypotheses.append(hypothesis)
        
        return hypotheses
    
    def _detect_domain(self, prompt: str) -> str:
        """Detect scientific domain from prompt keywords"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['thermal', 'heat', 'temperature', 'cooling']):
            return 'thermal'
        elif any(word in prompt_lower for word in ['structural', 'stress', 'strength', 'load']):
            return 'structural'
        else:
            return 'general'
    
    def _instantiate_template(self, template: Dict[str, Any], seed: int) -> Dict[str, Any]:
        """
        Create specific hypothesis from template with randomized parameters.
        
        Args:
            template: Hypothesis template
            seed: Random seed for reproducibility
            
        Returns:
            Instantiated hypothesis dictionary
        """
        random.seed(seed)
        
        # Copy template
        hypothesis = template.copy()
        
        # Randomize parameters
        if 'factor' in hypothesis['description']:
            factor = random.uniform(1.5, 3.0)
            hypothesis['description'] = hypothesis['description'].format(factor=f"{factor:.1f}")
            
            # Update parameters
            params = hypothesis['parameters'].copy()
            for key, value in params.items():
                if isinstance(value, str) and '{' in value:
                    params[key] = factor
            hypothesis['parameters'] = params
        
        if 'percent' in hypothesis['description']:
            percent = random.randint(10, 50)
            hypothesis['description'] = hypothesis['description'].format(percent=percent)
            
            # Update parameters
            params = hypothesis['parameters'].copy()
            for key, value in params.items():
                if isinstance(value, str) and '{' in value:
                    params[key] = 1 + (percent / 100)
            hypothesis['parameters'] = params
        
        if 'spacing' in hypothesis['description']:
            spacing = random.choice([50, 100, 150, 200])
            hypothesis['description'] = hypothesis['description'].format(spacing=spacing)
        
        # Add metadata
        hypothesis['id'] = f"hyp_{seed}"
        hypothesis['domain'] = template.get('type', 'unknown')
        
        return hypothesis
    
    def generate_with_constraints(self, 
                                  prompt: str, 
                                  constraints: Dict[str, Any],
                                  num_hypotheses: int = 5) -> List[Dict[str, Any]]:
        """
        Generate hypotheses respecting specified constraints.
        
        Args:
            prompt: Scientific question
            constraints: Dictionary of constraint conditions
            num_hypotheses: Number to generate
            
        Returns:
            List of hypothesis dictionaries
        """
        # Generate base hypotheses
        hypotheses = self.generate(prompt, num_hypotheses * 2)
        
        # Filter by constraints
        valid_hypotheses = []
        for hyp in hypotheses:
            if self._check_constraints(hyp, constraints):
                valid_hypotheses.append(hyp)
            if len(valid_hypotheses) >= num_hypotheses:
                break
        
        return valid_hypotheses
    
    def _check_constraints(self, hypothesis: Dict[str, Any], constraints: Dict[str, Any]) -> bool:
        """Check if hypothesis satisfies constraints"""
        # Simple constraint checking
        # In production: more sophisticated constraint evaluation
        
        if 'max_complexity' in constraints:
            param_count = len(hypothesis.get('parameters', {}))
            if param_count > constraints['max_complexity']:
                return False
        
        if 'allowed_types' in constraints:
            if hypothesis.get('type') not in constraints['allowed_types']:
                return False
        
        return True


if __name__ == "__main__":
    # Example usage
    generator = HypothesisGenerator()
    
    prompt = "How can we increase heat transfer efficiency?"
    hypotheses = generator.generate(prompt, num_hypotheses=5)
    
    print("\n=== Generated Hypotheses ===\n")
    for i, hyp in enumerate(hypotheses, 1):
        print(f"{i}. {hyp['description']}")
        print(f"   Equation: {hyp['equation']}")
        print(f"   Type: {hyp['type']}")
        print()
