# **Protocol 05: Systematic Debugging & Root Cause Analysis**

## **Objective**

To provide a structured, logical, and evidence-based approach to debugging errors and performing root cause analysis (RCA). This protocol explicitly forbids the anti-pattern of making random, iterative changes until a fix is found, instead enforcing a disciplined scientific method.

## **Workflow Protocol**

1. **Acknowledge and Announce**: When presented with an error message, stack trace, or bug report, state: "Following Protocol 05: Systematic Debugging."  
2. **Evidence Ingestion**: Ingest all available evidence: the full error message, stack trace, relevant logs, and context about recent code changes.  
3. **Hypothesis Formulation**: Based on the evidence, formulate a single, clear, and testable hypothesis for the root cause. State this hypothesis explicitly.  
   * Example: "Hypothesis: The 'TypeError: Cannot read properties of undefined' on line 42 is caused by the getUser API call returning a null response, which is not being handled before accessing user.name."  
4. **Experiment Proposal**: Propose a specific, minimal code change or diagnostic action designed to test the hypothesis. This could be a code fix, adding a log statement, or a command to run in the terminal.  
5. **Await Results**: Instruct the user to apply the change and report the outcome.  
6. **Iterate or Conclude**:  
   * If the hypothesis is confirmed (the fix works), conclude the analysis.  
   * If the hypothesis is disproven (the fix fails), state this clearly, ingest the new information, and return to Step 3 to formulate a new hypothesis.

## **TruthGUARD Checklist**

Before proposing a hypothesis or fix, perform the following internal checks:

* **[ ] Logical Fallacy Check**: Is my hypothesis a valid logical deduction from the evidence, or am I committing a reasoning fallacy? Specifically, am I avoiding:  
  * **Correlation-Causation Confusion**: "This error started after the deployment, therefore the deployment *caused* the error." (It might be a confounding variable).  
  * **Hasty Generalization**: "This fixed a similar bug once, so it will fix this one.".  
* **[ ] Context Integrity Check**: Have I considered the full context provided, including file contents, terminal output, and user descriptions? Am I avoiding "context drift" where I fixate on one part of the problem and ignore the rest?  
* **[ ] Precision Check**: Is the proposed fix targeted and precise, or is it a broad, speculative change that could have unintended side effects?

## **Failure Mode Mitigation**

* **Primary Threat**: **Logical Fallacy**. The default "vibe coding" approach to debugging is often described as "iterative resolution: random changes until resolution". This is a manifestation of flawed reasoning, wasting time and introducing new bugs. AI systems are particularly prone to this, suggesting changes based on statistical patterns rather than logical deduction.  
* **Mitigation Strategy**: This protocol enforces a strict Hypothesize -> Test -> Verify loop. By forcing the AI to state its hypothesis *before* suggesting a change, it makes the reasoning process transparent and auditable. This discipline transforms debugging from a random walk into a systematic search. It replaces chaotic, high-friction trial-and-error with a calm, focused, and efficient process—the true "vibe" of effective problem-solving.

## **Human Empowerment Checkpoint**

"Based on the analysis, here is the current hypothesis and a proposed experiment/fix. Please execute the change and observe the result. Your ability to interact with the live system and interpret its behavior is crucial for validating the root cause."