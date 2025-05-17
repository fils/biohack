// Defining a data model.
class Idea {
    hypothesis string[] @description("The main research question or proposed explanation the paper tests (e.g., Does X affect Y?).")
    supportingArguments  string[] @description("Evidence or reasoning backing the hypothesis, such as experimental data or cited studies.")
    researchOpportunities string[] @description("Areas for future research or gaps in knowledge suggested by the paper.")
    methodology string[] @description("How the research was conducted, including experimental design and techniques.")
    results string[] @description("The key outcomes or findings from the study.")
    conclusions string[] @description("The paper’s final interpretations or decisions based on the results.")
    limitations string[] @description("Weaknesses or constraints in the study that might impact the findings.")
    futureDirections string[] @description("Specific suggestions for next steps in research, slightly distinct from research opportunities by being more actionable.")
    keyFindings string[] @description("The most significant or impactful results highlighted in the paper.")
    references string[] @description("Cited works that provide context or support for the study.")
}

// Create a function to extract the idea from a string.
function ExtractIdea(idea: string) -> Idea {
  // Specify a client as provider/model-name
  // you can use custom LLM params with a custom client name from clients.baml like "client CustomHaiku"
  client "openai/gpt-4o" // Set OPENAI_API_KEY to use this client.
  //client "XAI"                  // use xai
  prompt #"

    Instructions:
    Analyze the provided text from a biosciences research paper and extract the
    following elements. For each element, provide a concise summary or direct quote from the
    text where possible. If an element is not explicitly stated,
    indicate "Not explicitly mentioned" or infer it from the context if reasonable.
    Organize your output with clear headings for each element.

    Hypothesis
    Identify the main hypothesis or research question the paper addresses. Look for statements like "We hypothesize that..." or "This study aims to determine..." in the introduction or abstract.

    Supporting Argument
    Extract key evidence or reasoning supporting the hypothesis, such as experimental data, observations, or references to prior studies. Check the results, discussion, or literature review sections.

    Research Opportunities
    Highlight areas suggested for further research or gaps in knowledge. Look for phrases like "Future studies could explore..." or "This raises questions about..." in the discussion or conclusion.

    Methodology
    Summarize the methods or techniques used to test the hypothesis, including experimental design, data collection, and analysis. Typically found in the "Methods" or "Materials and Methods" section.

    Results
    Describe the main findings or outcomes of the study, including quantitative data (e.g., measurements, statistics) or qualitative observations. Look in the "Results" section, tables, or figures.

    Conclusions
    Extract the final interpretations or decisions drawn from the research, such as whether the hypothesis was supported. Found in the "Conclusion" or "Discussion" section.

    Limitations
    Note any constraints, weaknesses, or biases mentioned that might affect the results. Look for phrases like "A limitation of this study is..." in the discussion.

    Future Directions
    Identify specific suggestions for future research based on the findings. Look for actionable recommendations like "Future work should investigate..." in the conclusion.

    Key Findings
    Highlight the most significant or impactful results emphasized by the authors. Check the abstract, conclusion, or discussion for standout points.

    References
    List key studies or papers cited in the text that provide context or support. Found in in-text citations or the reference list.


    {{ idea }}

    {{ ctx.output_format }}
  "#
}

// Test the function Open the VSCode playground to run this.
test vaibhav_idea {
  functions [ExtractIdea]
  args {
    idea #"
      Vaibhav Gupta
      vbv@boundaryml.com

      Experience:
      - Founder at BoundaryML
      - CV Engineer at Google
      - CV Engineer at Microsoft

      Skills:
      - Rust
      - C++
    "#
  }
}
