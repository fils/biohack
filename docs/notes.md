# Hypothesis playground

## About

This document contains some prompts and results associated with extracting hypothesis and related properties from a text.

### Resource to Markdown and JSON results

For this, you can follow:

#### convert mode

The convert mode allows you to convert HTML or PDF documents to Markdown format. You can specify either a URL or a local file as the input source.

Convert an HTML document from a URL:
```bash
python biohack.py convert -url https://example.com -output output/example.md
```

Convert a local PDF file:
```bash
python biohack.py convert -local path/to/document.pdf -output output/document.md
```

This functionality uses html2text for HTML conversion and PyPDF2 for PDF conversion. Make sure to install the required dependencies:

#### Hypothesis from LLM

Use the code bamlTest.py to use OpenAI (set the key with something like)

```bash
export OPENAI_API_KEY="..."
```

> Note: Since this is using [BAML](https://github.com/BoundaryML/baml) it's easy to 
> modify [clients.baml](baml_src/clients.baml) and add in any client.  Ollama, for local,
> Xai, Google Gemini, etc.  You will then need to modify the ``` client "openai/gpt-4o" ```
> in [hypothesis.baml](baml_src/hypothesis.baml) and rerun ```baml-cli generate```

Then run with

```bash
python bamlTest.py --input input.md --output output.json
```

### Future

As a next step, I will compare this approach with the following. I will convert the paper to a graph via entity resolution.  I can then look for clusters and motifs in there that can be extracted and passed to the LLM to see if it can formulate similar results or do other types of inferencing.  


## Elements

* Hypothesis: The main research question or proposed explanation the paper tests (e.g., "Does X affect Y?").
* Supporting Arguments: Evidence or reasoning backing the hypothesis, such as experimental data or cited studies.
* Research Opportunities: Areas for future research or gaps in knowledge suggested by the paper.
* Methodology: How the research was conducted, including experimental design and techniques.
* Results: The key outcomes or findings from the study.
* Conclusions: The paper’s final interpretations or decisions based on the results.
* Limitations: Weaknesses or constraints in the study that might impact the findings.
* Future Directions: Specific suggestions for next steps in research (slightly distinct from research opportunities by being more actionable).
* Key Findings: The most significant or impactful results highlighted in the paper.
* References: Cited works that provide context or support for the study.

## Prompt

```
Instructions:Analyze the provided text from a biosciences research paper and extract the following elements. 
For each element, provide a concise summary or direct quote from the text where possible. If an element is not 
explicitly stated, indicate "Not explicitly mentioned" or infer it from the context if reasonable. 
Organize your output with clear headings for each element.

Hypothesis  
Identify the main hypothesis or research question the paper addresses. Look for statements 
like "We hypothesize that..." or "This study aims to determine..." in the introduction or abstract.

Supporting Arguments  
Extract key evidence or reasoning supporting the hypothesis, such as experimental data, 
observations, or references to prior studies. Check the results, discussion, or literature review sections.

Research Opportunities  
Highlight areas suggested for further research or gaps in knowledge. Look for phrases 
like "Future studies could explore..." or "This raises questions about..." in the discussion or conclusion.

Methodology  
Summarize the methods or techniques used to test the hypothesis, including experimental 
design, data collection, and analysis. Typically found in the "Methods" or "Materials and Methods" section.

Results  
Describe the main findings or outcomes of the study, including quantitative data (e.g., 
measurements, statistics) or qualitative observations. Look in the "Results" section, tables, or figures.

Conclusions  
Extract the final interpretations or decisions drawn from the research, such as whether 
the hypothesis was supported. Found in the "Conclusion" or "Discussion" section.

Limitations  
Note any constraints, weaknesses, or biases mentioned that might affect the results. 
Look for phrases like "A limitation of this study is..." in the discussion.

Future Directions  
Identify specific suggestions for future research based on the findings. Look for 
actionable recommendations like "Future work should investigate..." in the conclusion.

Key Findings  
Highlight the most significant or impactful results emphasized by the authors. 
Check the abstract, conclusion, or discussion for standout points.

References  
List key studies or papers cited in the text that provide context or support. 
Found in in-text citations or the reference list.

```

Using this approach on the resource,  https://www.aging-us.com/article/205322/text, resulted in the following output.

## Results

Direct link to [results1.json](results1.json) for easier reading.  Also included inline below.  

```json
{
  "hypothesis": [
    "This study hypothesizes that Angiopep-2-based chemical exchange saturation transfer (CEST) MRI can visualize and assess the clearance function of the glymphatic system in vivo, as indicated by statements like 'we describe an MRI method based on chemical exchange saturation transfer (CEST) of the Angiopep-2 probe to visualize the clearance function of the glymphatic system.'"
  ],
  "supportingArguments": [
    "Experimental data showed higher CEST signals in rats with impaired glymphatic function (e.g., deep cervical lymph node ligation and ageing groups) compared to controls, supporting the hypothesis; references to prior studies (e.g., Iliff et al. 2012, 2013) on glymphatic dysfunction provide additional reasoning."
  ],
  "researchOpportunities": [
    "Gaps include challenges in imaging the glymphatic system due to the blood-brain barrier, as noted in the introduction; the discussion suggests opportunities like exploring CEST sequence optimization and Angiopep-2 modifications for better results."
  ],
  "methodology": [
    "Rats were injected with Angiopep-2 via the tail vein and scanned using CEST-MRI at 7 T at various time points (0, 30, 60, 90, 120 min); models included bilateral deep cervical lymph node ligation and ageing rats, with fluorescence staining and behavioral tests (e.g., Morris water maze) also employed."
  ],
  "results": [
    "DCLN and ageing rats showed higher CEST signals than controls, with peak enhancement at 60 minutes; fluorescence staining confirmed more FITC-Angiopep-2 residue in impaired glymphatic models, and behavioral tests indicated spatial memory decline in DCLN rats."
  ],
  "conclusions": [
    "The study concludes that Angiopep-2 CEST MRI can visualize clearance in the glymphatic system, as stated: 'We conclude that this new MRI method can visualize clearance in the glymphatic system.'"
  ],
  "limitations": [
    "Not explicitly mentioned, but inferred: GBCAs have limited blood-brain barrier penetration, higher doses were used which may not translate to clinical settings, and scanning was limited to a single layer due to time constraints, potentially affecting applicability."
  ],
  "futureDirections": [
    "Future work should investigate modifying Angiopep-2 concentration, optimizing CEST sequences for reduced scanning time and 3D whole-brain imaging, and addressing clinical limitations like injection volume, as suggested in the discussion."
  ],
  "keyFindings": [
    "Angiopep-2 CEST MRI demonstrated feasibility for assessing glymphatic clearance, with higher signals in impaired models (DCLN and ageing rats), confirming its potential for visualizing dysfunction."
  ],
  "references": [
    "Goedert M. (2015). NEURODEGENERATION. Alzheimer’s and Parkinson’s diseases: The prion concept in relation to assembled Aβ, tau, and α-synuclein. Science.",
    "Iliff JJ et al. (2012). A paravascular pathway facilitates CSF flow through the brain parenchyma and the clearance of interstitial solutes, including amyloid β. Sci Transl Med.",
    "Iliff JJ et al. (2013). Cerebral arterial pulsation drives paravascular CSF-interstitial fluid exchange in the murine brain. J Neurosci.",
    "Kress BT et al. (2014). Impairment of paravascular clearance pathways in the aging brain. Ann Neurol.",
    "Other key citations include studies on glymphatic system and MRI techniques, such as those by Da Mesquita S. (2018) and Ringstad G. (2017)."
  ]
}

```


## Assertions


```text

Extract the most significant Cardinal Assertions from the research paper.
Cardinal Assertions are the novel, significant, or central claims that
represent the core contribution of the research. These are often found
in the abstract, introduction, results, and discussion sections and may
use language such as "we found that," "our results show," or
"this study demonstrates."
 
 For example, a Cardinal Assertion might be: "This study demonstrates 
 that X leads to Y, challenging the previous understanding that 
 Z is the primary factor."

For each Cardinal Assertion, list the corresponding Supporting 
Assertions that provide context, methodology, provenance, or 
evidence. Supporting Assertions are typically found in the methods
and introduction sections and may include phrases like "using the method of,"
"based on data from," or "as defined by." For example, a 
Supporting Assertion might be: "The data was collected from a 
sample of 100 participants using a randomized controlled trial design."

Ensure that all extracted assertions are directly supported by the 
text and do not infer or generate information not explicitly stated
in the research paper. If you do not find anything simply
do not repot for that elements, do not state that nothing is found.

```

```json
{
  "Cardinal": [
    "This study demonstrates the feasibility of using Angiopep-2 CEST MRI to visualize the clearance function of the glymphatic system.",
    "The results show that damage to the glymphatic clearance system impedes the clearance of Angiopep-2, resulting in more Angiopep-2 remaining in the brain.",
    "We found that in rats with impaired glymphatic system clearance function, such as the DCLN and OLD rats, the CESTR values were elevated compared to normal SD rats after Angiopep-2 injection."
  ],
  "Supporting": [
    "We describe an MRI method based on chemical exchange saturation transfer (CEST) of the Angiopep-2 probe to visualize the clearance function of the glymphatic system.",
    "Using a rat model, we injected Angiopep-2 via the tail vein and performed _in vivo_ MRI at 7 T to track differences in Angiopep-2 signal changes.",
    "The same principles were applied in a bilateral deep cervical lymph node ligation rat model and in ageing rats.",
    "Fluorescence imaging confirmed that Angiopep-2 can penetrate the blood-brain barrier by binding to low-density lipoprotein receptor-related protein 1 (LRP-1).",
    "Chemical exchange saturation transfer (CEST) imaging allows noninvasive tracking of substances at the molecular level and was used to assess glymphatic clearance in rat models.",
    "FITC-Angiopep-2 was used for further validation in brain parenchyma, indicating impaired glymphatic clearance in the DCLN group compared to SHAM."
  ]
}

```