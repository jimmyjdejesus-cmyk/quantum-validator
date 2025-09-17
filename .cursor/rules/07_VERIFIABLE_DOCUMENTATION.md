# **Protocol 07: Verifiable Documentation**

## **Objective**

To generate technical documentation (e.g., READMEs, API specifications, architectural decision records) that is accurate, clear, up-to-date, and verifiable. This protocol's core purpose is to prevent the spread of misinformation within the team by combating AI hallucination in documentation.

## **Workflow Protocol**

1. **Acknowledge and Announce**: Upon receiving a documentation task, state: "Following Protocol 07: Verifiable Documentation."  
2. **Source Code Analysis**: Ingest the relevant source code (@filename) as the single source of truth for the system's behavior.  
3. **Content Generation**: Generate the documentation content, strictly adhering to the following principles:  
   * **Clarity**: Use simple, unambiguous language. Define all acronyms and technical terms.  
   * **Accuracy**: Ensure all descriptions of functionality, API endpoints, and parameters directly match the source code.  
   * **Completeness**: Cover all public-facing aspects of the code being documented.  
4. **Example Generation**: For all code examples, ensure they are:  
   * Directly extracted or derived from the source code or accompanying tests.  
   * Complete and runnable.  
   * Version-stamped to prevent them from becoming outdated.  
5. **Review and Refine**: Perform a self-review against the TruthGUARD checklist to find and fix any inaccuracies or hallucinations before presenting the final document.

## **TruthGUARD Checklist**

Before presenting the documentation, perform the following internal checks:

* **[ ] Fact Verification**: Is every factual claim made in this document (e.g., "this function returns a Promise<string>," "this endpoint requires a x-api-key header") directly verifiable by inspecting the source code?  
* **[ ] Hallucination Check**: Are all code examples, API endpoints, configuration settings, and library names accurate and not fabricated? Have I cross-referenced them against the actual codebase?  
* **[ ] Context Integrity Check**: Does the documentation accurately reflect the *current* state of the code, or is it based on outdated context from my training data?  
* **[ ] Limitation Acknowledgment**: Have I clearly stated the version of the code that this documentation applies to?

## **Failure Mode Mitigation**

* **Primary Threat**: **AI Hallucination & Reliability**. AI models confidently fabricate facts, references, and technical details. In documentation, this is particularly dangerous as it pollutes the team's knowledge base and leads developers to build against a phantom version of the system.  
* **Mitigation Strategy**: This protocol enforces a strict "source of truth" principle, anchoring all generated documentation directly to the codebase.  
  * **Code as Truth**: The AI is instructed to treat the provided source code as the ultimate authority, overriding any conflicting information from its training data.  
  * **Verifiable Examples**: All code examples must be demonstrably correct. The AI should prefer to extract examples from existing unit tests where possible, as these are by definition verified to work.  
  * **Cautious Phrasing and Versioning**: All claims about system behavior will be anchored to a specific context.  
    * **Example**: Instead of "The API returns user data," the protocol mandates a more precise and verifiable statement: "**As of v1.2.5**, the GET /api/users/{id} endpoint returns a JSON object with the following structure..."

## **Human Empowerment Checkpoint**

"Please review this generated documentation for clarity and accuracy. Your mental model of the system is the final check. Does this document align with how the system actually works in practice? Is there any crucial context or 'gotcha' that is missing?"