// Defining a data model.

// need enums for predicates   ref:  https://docs.boundaryml.com/ref/baml/enum    

enum NanoPred {
    HAS_DIGITAL_OBJECT_TYPE @alias("has_digital_object_type") @description("Indicates the type of digital object, e.g., dataset, software, or document.")
    HAS_MEDIA_TYPE @alias("has_media_type") @description("Specifies the media type of the resource, such as application/pdf or text/csv.")
    HAS_ACCESS_URI @alias("has_access_uri") @description("Provides the URI where the resource can be accessed.")
    HAS_PUBLISHER @alias("has_publisher") @description("Identifies the entity responsible for publishing the resource.")
    HAS_PUBLICATION_DATE @alias("has_publication_date") @description("Records the date when the resource was published.")
    HAS_VERSION @alias("has_version") @description("Indicates the version number or identifier of the resource.")
    USES_FIP @alias("uses_fip") @description("Denotes that the resource adheres to FAIR Interoperability Principles.")
    HAS_LICENSE @alias("has_license") @description("Specifies the license under which the resource is distributed.")
    HAS_LANGUAGE @alias("has_language") @description("Indicates the primary language(s) of the resource.")
    HAS_DOMAIN @alias("has_domain") @description("Describes the subject domain or discipline of the resource.")
    HAS_TITLE @alias("has_title") @description("The title or name of the resource.")
    HAS_DESCRIPTION @alias("has_description") @description("A brief summary or abstract of the resource content.")
    HAS_FUNDER @alias("has_funder") @description("Identifies the funding agency or entity supporting the resource.")
    HAS_PROJECT_ID @alias("has_project_id") @description("Unique identifier for the project associated with the resource.")
    CREATOR @alias("creator") @description("The individual or entity that created the resource.")
    CONTRIBUTOR @alias("contributor") @description("Additional individuals or entities that contributed to the resource.")
    HAS_CONTACT_POINT @alias("has_contact_point") @description("Contact information for the resource's responsible party.")
    HAS_WEBSITE @alias("has_website") @description("URL of a website related to the resource or project.")
    HAS_START_DATE @alias("has_start_date") @description("The start date of the project or resource creation.")
    HAS_END_DATE @alias("has_end_date") @description("The end date of the project or resource validity.")
    IS_PART_OF @alias("is_part_of") @description("Indicates the larger entity or collection the resource belongs to.")
    IS_IN_RESPONSE_TO @alias("is_in_response_to") @description("References a request or event that prompted the resource creation.")
    HAS_PROJECT_PRE_REGISTRATION @alias("has_project_pre_registration") @description("Details of the project's pre-registration, if applicable.")
    HAS_PROJECT_PROPOSAL @alias("has_project_proposal") @description("Information about the project proposal related to the resource.")
    HAS_MEMBERS @alias("has_members") @description("Lists the members or participants involved in the project.")
    HAD_BUDGET @alias("had_budget") @description("Financial budget details allocated for the project or resource.")
    HAS_ETHICS_CLEARANCE @alias("has_ethics_clearance") @description("Indicates if the project has ethics approval.")
    HAS_CONSORTIUM_AGREEMENT @alias("has_consortium_agreement") @description("Details of any consortium agreement for the project.")
    IS_OUTPUT_OF_PROJECT @alias("is_output_of_project") @description("Confirms the resource is a direct output of a specific project.")
    HAS_BEEN_REPOSED @alias("has_been_reposed") @description("Indicates if the resource has been deposited in a repository.")
    HAS_REPOSITORY_PID @alias("has_repository_pid") @description("Persistent identifier for the resource in a repository.")
    GENERATED_FROM_SAMPLE @alias("generated_from_sample") @description("Indicates the resource was derived from a specific sample.")
    HAS_DATASET @alias("has_dataset") @description("References a dataset associated with the resource.")
    HAS_METHOD @alias("has_method") @description("Describes the methodology used to create or analyze the resource.")
    HAS_IMAGE @alias("has_image") @description("References an image or visual associated with the resource.")
    HAS_CODE @alias("has_code") @description("References source code or scripts related to the resource.")
    HAS_DMP @alias("has_dmp") @description("Refers to the Data Management Plan for the resource or project.")
}

enum NanoPred2 {
    Predict @alias(predict) @description("Indicates the act of forecasting or estimating future outcomes or states based on data or models. This predicate combines several original terms: 'are capable of making reliable predictions,' 'can offer reasonable predictions for,' 'can predict,' 'has ability to predict,' 'predicts,' 'predicts orientation of,' 'provided the most accurate predictions when trained on,' and 'showed proficiency in predicting.' These were grouped because they all describe prediction, varying only in specificity (e.g., reliability, orientation) or context (e.g., training data).")
    Classify @alias(classify) @description("Refers to the process of categorizing or labeling entities into groups based on characteristics. This predicate merges 'classified as,' 'classifies,' 'classify,' and 'have been used to classify,' as they all describe the act of classification, differing only in tense or phrasing.")
    Enhance @alias(enhance) @description("Denotes the improvement or augmentation of a process, system, or outcome. This predicate combines 'enhance the classification by including,' 'enhance the planning and layout of,' 'improves,' and 'increase the accuracy from,' which all involve making something better, whether it’s classification, planning, or accuracy.")
    Suggest @alias(suggest) @description("Indicates proposing ideas, possibilities, or extensions. This predicate merges 'can suggest' and 'suggest extensions of,' as both involve offering suggestions, differing only in the scope of what is suggested.")
    Reveal @alias(reveal) @description("Describes the act of uncovering, presenting, or making information known. This predicate combines 'can reveal,' 'provide information on,' and 'highlights,' as they all involve bringing information to light, with slight variations in emphasis.")
    Support @alias(support) @description("Refers to providing backing, evidence, or justification for a claim or concept. This predicate merges 'supports' and 'show evidence for,' as both indicate substantiating something, differing only in how the support is framed.")
    AreBecoming @alias(are_becoming) @description("Indicates a process of transformation or development into a new state or role.")
    AreNotMakingAsManyConnectionsAsExpected @alias(are_not_making_as_many_connections_as_expected) @description("Describes a situation where fewer relationships or links (e.g., in data or networks) are being established than anticipated.")
    ArePotentiallyBasedOn @alias(are_potentially_based_on) @description("Suggests that something may be founded or derived from a particular source or basis, with uncertainty.")
    AreTrainedWith @alias(are_trained_with) @description("Indicates that a model or system is developed or refined using specific data or methods.")
    CanReliablyCharacterize @alias(can_reliably_characterize) @description("Denotes the ability to consistently and accurately describe or define the properties of something.")
    DemonstratedAnIncreaseInPredictionAccuracyTo @alias(demonstrated_an_increase_in_prediction_accuracy_to) @description("Indicates that a system or method has shown improved precision in forecasting, often to a specific level.")
    Determines @alias(determines) @description("Refers to the act of establishing or deciding something definitively based on analysis or evidence.")
    FaceChallengesWhenGeneralizedTo @alias(face_challenges_when_generalized_to) @description("Describes difficulties encountered when applying a model or method to broader or different contexts.")
    HasPlasmaCharacteristicsSimilarTo @alias(has_plasma_characteristics_similar_to) @description("Indicates that an entity shares physical or behavioral traits with plasma, often in a scientific context.")
    HasPredictionAccuracyOf @alias(has_prediction_accuracy_of) @description("Specifies the level of precision achieved by a predictive model or method.")
    HaveSparkedInterestIn @alias(have_sparked_interest_in) @description("Refers to generating curiosity or attention toward a particular topic or field.")
    IllustratesShortcomingsIn @alias(illustrates_shortcomings_in) @description("Highlights deficiencies or limitations in a system, method, or concept.")
    IsDecreasing @alias(is_decreasing) @description("Indicates a reduction or decline in a quantity, quality, or extent.")
    IsIdentified @alias(is_identified) @description("Refers to the act of recognizing or naming something as a specific entity.")
    IsUsedFor @alias(is_used_for) @description("Describes the purpose or application of a tool, method, or entity in a specific context.")
    IsUsedToSimulate @alias(is_used_to_simulate) @description("Indicates that something is employed to model or replicate a system or process.")
    Used @alias(used) @description("A general term indicating that something is applied or employed, often without specifying the purpose.")
}

class Nanograph {
    triples Nanopub[]
}

class Nanopub {
    subject string  // @description("The main research question or proposed explanation the paper tests (e.g., Does X affect Y?).")
    predicate  NanoPred2 // @description("Evidence or reasoning backing the hypothesis, such as experimental data or cited studies.")
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
