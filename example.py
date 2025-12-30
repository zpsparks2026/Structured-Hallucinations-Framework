"""
Example: Complete workflow demonstration
Shows all four loops of the Structured Hallucinations Framework
"""

from framework import StructuredHallucinationFramework


def main():
    """Run complete example workflow"""
    
    print("=" * 70)
    print("STRUCTURED HALLUCINATIONS FRAMEWORK")
    print("Four-Loop Validation for AI-Assisted Scientific Discovery")
    print("=" * 70)
    
    # Initialize framework (analytical validation only for demo)
    framework = StructuredHallucinationFramework(
        enable_numerical=False,  # Set True if simulation tools available
        enable_meta=False        # Set True if LLM API available
    )
    
    # Scientific prompt
    prompt = "Propose design modifications to increase thermal efficiency"
    num_hypotheses = 5
    
    print(f"\nPrompt: {prompt}")
    print(f"Generating {num_hypotheses} hypotheses...\n")
    
    # Run validation pipeline
    results = framework.run_full_pipeline(prompt, num_hypotheses=num_hypotheses)
    
    # Display results
    print("\n" + "=" * 70)
    print("VALIDATION RESULTS")
    print("=" * 70 + "\n")
    
    for i, result in enumerate(results, 1):
        print(f"Hypothesis {i}:")
        print(f"  Description: {result.hypothesis}")
        print(f"  Analytical Validation: {'✓ PASS' if result.analytical_passed else '✗ FAIL'}")
        
        if not result.analytical_passed:
            print(f"  Issues:")
            for violation in result.analytical_report.get('violations', []):
                print(f"    - {violation}")
        
        print(f"  Final Status: {result.final_status}")
        print()
    
    # Generate summary report
    report = framework.generate_report(results)
    
    print("\n" + "=" * 70)
    print("SUMMARY STATISTICS")
    print("=" * 70 + "\n")
    
    print(f"Total hypotheses generated: {report['total_generated']}")
    print(f"Passed analytical validation: {report['passed_analytical']}")
    print(f"Analytical filter rate: {report['analytical_filter_rate']:.1%}")
    print(f"Final acceptance rate: {report['final_acceptance_rate']:.1%}")
    
    print("\n" + "=" * 70)
    print("KEY INSIGHT")
    print("=" * 70 + "\n")
    
    if report['analytical_filter_rate'] > 0:
        print(f"Analytical pre-filtering eliminated {report['analytical_filter_rate']:.1%}")
        print("of hypotheses BEFORE expensive numerical simulation.")
        print("\nEstimated computational savings: 50-70% of simulation costs")
        print("by catching physics violations using symbolic math.")
    else:
        print("All generated hypotheses passed analytical validation.")
        print("These would proceed to numerical simulation for verification.")
    
    print("\n" + "=" * 70)
    print("FRAMEWORK ARCHITECTURE")
    print("=" * 70 + "\n")
    
    print("Loop 1: Divergent Generation")
    print("  → Creative hypothesis generation from LLM")
    print(f"  → Generated {report['total_generated']} candidate hypotheses")
    print()
    
    print("Loop 2: Analytical Validation")
    print("  → Symbolic mathematics (SymPy)")
    print("  → Physics constraints and conservation laws")
    print(f"  → Filtered {report['total_generated'] - report['passed_analytical']} invalid hypotheses")
    print()
    
    print("Loop 3: Numerical Validation (Conceptual)")
    print("  → FEA/CFD/Molecular Dynamics simulation")
    print("  → High-fidelity physics testing")
    print("  → Only run on analytically-validated hypotheses")
    print()
    
    print("Loop 4: Meta-Oversight (Conceptual)")
    print("  → Cross-hypothesis consistency")
    print("  → Systematic error detection")
    print("  → Final validation quality check")
    print()
    
    print("=" * 70)
    print("NEXT STEPS")
    print("=" * 70 + "\n")
    
    passed_hypotheses = [r for r in results if r.analytical_passed]
    
    if passed_hypotheses:
        print(f"{len(passed_hypotheses)} hypotheses ready for numerical validation:")
        for i, result in enumerate(passed_hypotheses, 1):
            print(f"  {i}. {result.hypothesis}")
        print("\nThese would be submitted to FEA/CFD simulation for verification.")
    else:
        print("No hypotheses passed analytical validation.")
        print("Consider refining the generation prompt or relaxing constraints.")
    
    print()


if __name__ == "__main__":
    main()
