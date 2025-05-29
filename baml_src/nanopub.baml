// Defining a data model.

// need enums for predicates   ref:  https://docs.boundaryml.com/ref/baml/enum    

class Nanograph {
    triples Nanopub[]
}

class Nanopub {
    subject string  // @description("The main research question or proposed explanation the paper tests (e.g., Does X affect Y?).")
    predicate  string // @description("Evidence or reasoning backing the hypothesis, such as experimental data or cited studies.")
    object string // @description("Evidence or reasoning backing the hypothesis, such as experimental data or cited studies.")
}


// Create a function to extract the idea from a string.
function ExtractNanopubs(idea: string) -> Nanograph {
  // Specify a client as provider/model-name
  // you can use custom LLM params with a custom client name from clients.baml like "client CustomHaiku"
  client "openai/gpt-4o" // Set OPENAI_API_KEY to use this client.
  //client "XAI"                  // use xai
  prompt #"

You are an expert in semantic web technologies and nanopublications. Your task is to analyze a given scientific text and extract the components of a nanopublication assertion, specifically the subject, predicate, and object, to form a structured assertion in the format of a subject-predicate-object triple. 

**Instructions:**
1. Read the provided text carefully.
2. Identify the core scientific claim or relationship described in the text.
3. Extract:
   - **Subject**: The entity or concept that the claim is about (e.g., a gene, drug, or disease).
   - **Predicate**: The relationship or action connecting the subject and object (e.g., "is associated with," "inhibits," "causes").
   - **Object**: The entity or concept that the subject is related to (e.g., another gene, disease, or outcome).
4. Present the assertion as a clear subject-predicate-object triple.
5. If the text is ambiguous or lacks a clear claim, state that no assertion could be formed and explain why.
6. Do not include provenance or publication info unless explicitly requested.


There may be more than one assertion (set of triples) or none, in the provided text.

If the text has no assertions that can be found return the requested format with
empty elements.

**Example:**
**Input Text**: "The study found that Drug X effectively reduces symptoms of Disease Y."
**Output**:
- **Assertion**: Drug X - reduces symptoms of - Disease Y
- **Explanation**: The subject is "Drug X" (the entity the claim is about), the predicate is "reduces symptoms of" (the relationship), and the object is "Disease Y" (the entity affected).

    {{ idea }}

    {{ ctx.output_format }}
  "#
}

// Test the function Open the VSCode playground to run this.
test vaibhav_idea {
  functions [ExtractNanopubs]
  args {
    idea #"
    Our work uses CNNs trained with magnetic field vectors from analytical flux rope data.
    The simulated flux ropes span many possible spacecraft trajectories and flux rope orientations.
    The circular-cylindrical flux rope model of Nieves-Chinchilla et al. [19] (N-C model) is used to simulate the magnetic field signature of flux ropes.
    The process of casting the physics problem as a machine learning problem is discussed.
    Various physics-based flux rope models exist (for examples Lepping et al. [9]and Nieves-Chinchilla et al. [10]) that can be used to reconstruct the internal ICME magnetic configuration.
    The neural network is trained using simulated magnetic field measurements over a range of spacecraft trajectories and flux rope orientations.
    The final segment of this work is to evaluate the trained CNNs on flux ropes observed by the Wind spacecraft.
    Figure 3. The parameter prediction error for the synthetic test set of full duration flux rope crossings
    "#
  }
}
