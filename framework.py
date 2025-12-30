"""
Structured Hallucinations Framework
Core orchestration for AI-assisted scientific discovery
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from generators import HypothesisGenerator
from validators import AnalyticalValidator
from numerical import NumericalSimulator
from oversight import MetaOversight


@dataclass
class ValidationResult:
    """Result from validation pipeline"""
    hypothesis: str
    hypothesis_data: Dict[str, Any]
    analytical_passed: bool
    analytical_report: Dict[str, Any]
    numerical_passed: bool = None
    numerical_report: Dict[str, Any] = None
    meta_passed: bool = None
    meta_report: Dict[str, Any] = None
    final_status: str = "PENDING"


class StructuredHallucinationFramework:
    """
    Four-loop validation architecture for AI-generated scientific hypotheses.
    
    Loop 1: Divergent Generation - Creative hypothesis generation
    Loop 2: Analytical Validation - Symbolic math and physics constraints
    Loop 3: Numerical Validation - High-fidelity simulation (conceptual)
    Loop 4: Meta-Oversight - Cross-hypothesis consistency (conceptual)
    """
    
    def __init__(self, enable_numerical: bool = False, enable_meta: bool = False):
        """
        Initialize framework components.
        
        Args:
            enable_numerical: Enable Loop 3 (requires external simulation tools)
            enable_meta: Enable Loop 4 (requires LLM API access)
        """
        self.generator = HypothesisGenerator()
        self.analytical = AnalyticalValidator()
        self.numerical = NumericalSimulator() if enable_numerical else None
        self.meta = MetaOversight() if enable_meta else None
        
    def run_full_pipeline(self, 
                         prompt: str, 
                         num_hypotheses: int = 5,
                         analytical_only: bool = True) -> List[ValidationResult]:
        """
        Execute complete validation pipeline.
        
        Args:
            prompt: Scientific question or optimization goal
            num_hypotheses: Number of hypotheses to generate
            analytical_only: Skip numerical validation (faster)
            
        Returns:
            List of ValidationResult objects with validation outcomes
        """
        # Loop 1: Divergent Generation
        hypotheses = self.generator.generate(prompt, num_hypotheses)
        results = []
        
        for hyp_data in hypotheses:
            result = ValidationResult(
                hypothesis=hyp_data['description'],
                hypothesis_data=hyp_data,
                analytical_passed=False,
                analytical_report={}
            )
            
            # Loop 2: Analytical Validation
            analytical_result = self.analytical.validate(hyp_data)
            result.analytical_passed = analytical_result['passed']
            result.analytical_report = analytical_result
            
            if not result.analytical_passed:
                result.final_status = "REJECTED_ANALYTICAL"
                results.append(result)
                continue
                
            # Loop 3: Numerical Validation (if enabled and requested)
            if not analytical_only and self.numerical:
                numerical_result = self.numerical.simulate(hyp_data)
                result.numerical_passed = numerical_result['passed']
                result.numerical_report = numerical_result
                
                if not result.numerical_passed:
                    result.final_status = "REJECTED_NUMERICAL"
                    results.append(result)
                    continue
            
            result.final_status = "PASSED" if analytical_only else "PASSED_ALL"
            results.append(result)
        
        # Loop 4: Meta-Oversight (if enabled)
        if self.meta:
            meta_results = self.meta.analyze_batch(results)
            for i, result in enumerate(results):
                result.meta_passed = meta_results[i]['passed']
                result.meta_report = meta_results[i]
                if not result.meta_passed:
                    result.final_status = "REJECTED_META"
        
        return results
    
    def generate_report(self, results: List[ValidationResult]) -> Dict[str, Any]:
        """
        Generate summary statistics from validation results.
        
        Args:
            results: List of ValidationResult objects
            
        Returns:
            Dictionary with summary statistics
        """
        total = len(results)
        passed_analytical = sum(1 for r in results if r.analytical_passed)
        passed_numerical = sum(1 for r in results if r.numerical_passed)
        passed_meta = sum(1 for r in results if r.meta_passed)
        final_passed = sum(1 for r in results if r.final_status.startswith("PASSED"))
        
        return {
            'total_generated': total,
            'passed_analytical': passed_analytical,
            'passed_numerical': passed_numerical,
            'passed_meta': passed_meta,
            'final_passed': final_passed,
            'analytical_filter_rate': 1 - (passed_analytical / total) if total > 0 else 0,
            'final_acceptance_rate': final_passed / total if total > 0 else 0
        }


if __name__ == "__main__":
    # Example usage
    framework = StructuredHallucinationFramework()
    
    prompt = "Propose design modifications to increase thermal efficiency"
    results = framework.run_full_pipeline(prompt, num_hypotheses=5)
    
    print("\n=== Validation Results ===\n")
    for i, result in enumerate(results, 1):
        print(f"Hypothesis {i}: {result.hypothesis}")
        print(f"  Analytical: {'PASS' if result.analytical_passed else 'FAIL'}")
        print(f"  Status: {result.final_status}")
        if not result.analytical_passed:
            print(f"  Issues: {result.analytical_report.get('violations', [])}")
        print()
    
    report = framework.generate_report(results)
    print("\n=== Summary Statistics ===")
    print(f"Total hypotheses: {report['total_generated']}")
    print(f"Passed analytical: {report['passed_analytical']}")
    print(f"Analytical filter rate: {report['analytical_filter_rate']:.1%}")
    print(f"Final acceptance rate: {report['final_acceptance_rate']:.1%}")
