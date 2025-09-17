# **Protocol 02: System Design & Architecture**

## **Objective**

To generate and evaluate system designs and architectural plans that are robust, scalable, verifiable, and logically sound. This protocol ensures that all recommendations are based on existing, well-understood technologies and patterns, actively preventing the hallucination of non-existent tools or the misapplication of architectural principles.

## **Workflow Protocol**

1. **Acknowledge and Announce**: Upon receiving a design task, state: "Following Protocol 02: System Design & Architecture."  
2. **Model Selection**: For complex architectural decisions, the user will enable "Max Mode" to leverage the most capable reasoning model (e.g., Claude 3.7 Sonnet).  
3. **Option Generation**: Based on the verified requirements from Protocol 01, generate at least two viable architectural options. For each option, provide:  
   * A high-level description of the approach (e.g., Monolith, Microservices, Serverless).  
   * A list of key technologies involved.  
   * A summary of the primary trade-offs (e.g., development velocity vs. operational complexity, cost vs. scalability).  
4. **Diagramming**: For the recommended option, generate a system diagram using Mermaid syntax (e.g., sequence diagrams, C4 models).  
5. **Data Modeling**: Propose a preliminary data model, including key entities, attributes, and relationships.

## **TruthGUARD Checklist**

Before presenting the design options, perform the following internal checks:

* **[ ] Fact Verification**: For every recommended technology, framework, or library, can I confirm its existence, current maintenance status, and suitability for this specific use case with an authoritative source (e.g., official documentation, GitHub repository, reputable benchmark)?  
* **[ ] Hallucination Check**: Have I ensured that all recommended components, API endpoints, and configuration examples are real and not fabricated? This is a critical check against the 20% rate of false package recommendations by AI models.  
* **[ ] Logical Coherence Check**: Does the proposed design logically follow from the requirements? Have I avoided "Pattern Recognition Masquerading as Logic," where a familiar pattern is applied without justification?  
* **[ ] Alignment Check**: Does this design genuinely serve the user's stated requirements, or is it overly complex ("resume-driven development") or based on optimizing for a proxy metric (e.g., using a technology simply because it's popular)?

## **Failure Mode Mitigation**

* **Primary Threats**: **AI Hallucination** and **Logical Fallacy**. Hallucinations lead to designs based on non-existent tools, wasting significant time. Logical fallacies lead to architectures that are internally inconsistent or poorly suited to the problem domain.  
* **Mitigation Strategy**: This protocol mandates radical source attribution and transparent reasoning.  
  * **Source Attribution**: Every technology recommendation must be accompanied by a direct link to its official documentation or a primary source. (e.g., "For the caching layer, I recommend Redis [https://redis.io/docs/]. Its in-memory data structures are well-suited for this use case.").  
  * **Transparent Reasoning**: Every significant design choice must be explicitly justified by linking it back to a specific requirement from Protocol 01. (e.g., "A microservices architecture is recommended *because* Requirement F-5 specifies that the billing and shipping components must be independently deployable.").

## **Human Empowerment Checkpoint**

"Please review the proposed architectural options and their trade-offs. Your domain expertise and understanding of the long-term business strategy are essential to validate these technical decisions. Which approach best aligns with our project's goals?"