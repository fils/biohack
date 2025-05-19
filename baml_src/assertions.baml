// Defining a data model.
class Assertion {
    Cardinal string[] @description("The main research question or proposed explanation the paper tests (e.g., Does X affect Y?).")
    Supporting  string[] @description("Evidence or reasoning backing the hypothesis, such as experimental data or cited studies.")
}

// Create a function to extract the idea from a string.
function ExtractAssertion(idea: string) -> Assertion {
  // Specify a client as provider/model-name
  // you can use custom LLM params with a custom client name from clients.baml like "client CustomHaiku"
  client "openai/gpt-4o" // Set OPENAI_API_KEY to use this client.
  //client "XAI"                  // use xai
  prompt #"

Extract the most significant Cardinal Assertions from the research paper.
 Cardinal Assertions are the novel, significant, or central claims that
 represent the core contribution of the research. These are often found
 in the abstract, introduction, results, and discussion sections and may
 use language such as "we found that," "our results show," or "this study demonstrates."
 For example, a Cardinal Assertion might be: "This study demonstrates that X leads to Y,
 challenging the previous understanding that Z is the primary factor."

For each Cardinal Assertion, list the corresponding Supporting Assertions that provide
context, methodology, provenance, or evidence. Supporting Assertions are typically
found in the methods and introduction sections and may include phrases like "using the method of,"
"based on data from," or "as defined by." For example, a Supporting Assertion might
be: "The data was collected from a sample of 100 participants using a randomized controlled trial design."

Ensure that all extracted assertions are directly supported by the text and do not
infer or generate information not explicitly stated in the research paper. If you do not find anything simply
    do not repot for that elements, do not state that nothing is found.


    {{ idea }}

    {{ ctx.output_format }}
  "#
}

// Test the function Open the VSCode playground to run this.
test vaibhav_idea {
  functions [ExtractAssertion]
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
