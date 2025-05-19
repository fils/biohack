from gliner import GLiNER

model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

def my_function(text):
    labels = [
        "Author", "Researcher", "Scientist", "Corresponding Author", "Collaborator",
        "Patient", "Study Participant", "Institution", "Research Institute", "University",
        "Laboratory", "Company", "Funding Agency", "Consortium", "Hospital",
        "Government Agency", "Gene", "peptide", "Protein", "Enzyme", "Pathway", "Disease",
        "Virus", "Bacteria", "Drug", "Compound", "Cell Type", "Tissue", "Organ",
        "System", "Biomarker", "Mutation", "Phenotype", "Genotype", "Citation", "Journal",
        "Publisher", "Article Title", "DOI", "Grant Number", "Ethics Committee",
        "Study Type", "Dataset", "Software", "Algorithm", "Model", "Protocol",
        "Experiment", "Figure", "Table", "Keyword", "Technology",
        "Equipment", "Location", "Date", "Event", "Project", "Standard", "Metric",
        "Method", "Result", "Failure", "Success"
    ]

    entities = model.predict_entities(text, labels, threshold=0.5)
    return entities