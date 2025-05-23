# BioHack 


## References

### Setup

I'm assuming you have set up a working environment with your triplestore and other systems you want.
Note this repo is using the UV package management system. (see: https://docs.astral.sh/uv/)
Ensure all dependencies are installed by running `uv pip install -r requirements.txt` or by ensuring your `pyproject.toml` is up to date and then running `uv pip sync`.

#### Dependencies
The shell scripts `scripts/loadDirToTriplestore.sh` and `scripts/loadSitemapToTriplestore.sh` rely on the `jsonld` command-line tool for processing JSON-LD data. A common implementation is the Node.js `jsonld-cli` package.
You can install it via npm:
```bash
npm install -g jsonld-cli
```
For more information, visit: [https://www.npmjs.com/package/jsonld-cli](https://www.npmjs.com/package/jsonld-cli)

### Running Tests

Unit tests are located in the `tests/` directory. To run the tests, navigate to the root of the repository and execute the following command:

```bash
python -m unittest discover -s tests
```
This command will discover and run all tests within the `tests` directory. Make sure all project dependencies, including any test-specific dependencies like `reportlab` (which should be listed in `requirements.txt` or `pyproject.toml`), are installed using `uv`.

### Notebook prototype

Just playing with some established patterns to quickly load the graph. Used 
this notebook: [typeTypeView.ipynb](notebooks/typeTypeView.ipynb).  Eventually, 
you get to this type to type style network. 

![img.png](./docs/img.png)


### RDF load Quick start 

> NOTE: This is basically just the jsonldToTriple.ts read into python.  ref: https://ai-docs.bio.xyz/developers/knowledge-graphs

First set up your triplestore, I'll use oxigraph, but later we can make this work for others too.  

So there is JSON-LD for the groups to start with at https://github.com/bio-xyz/BioAgents. Specifically

* https://github.com/bio-xyz/BioAgents/tree/main/sampleJsonLds
* https://github.com/bio-xyz/BioAgents/tree/main/sampleJsonLdsNew

Since this is at GitHub it's easy to convert a directory to a sitemap format pointing to the raw URLs.
We will use a tool from the [Gleaner.io Archetype repo](https://github.com/gleanerio/archetype). 

We can run these:

```bash
./scripts/github_jsonld_sitemap.py --output output/jld-sitemap.xml https://github.com/bio-xyz/BioAgents sampleJsonLds 
```

```bash
./scripts/github_jsonld_sitemap.py --output output/jldnew-sitemap.xml https://github.com/bio-xyz/BioAgents sampleJsonLdsNew 
```

To load out JSON-LD now, we can use the sitemap to pull the resources directly from GitHub. (Make sure you have `jsonld-cli` installed, see "Dependencies" section under "Setup").

```bash
./scripts/loadSitemapToTriplestore.sh ./output/jld-sitemap.xml http://homelab.lan:7878/store
```

and

```bash
`./scripts/loadSitemapToTriplestore.sh ./output/jldnew-sitemap.xml http://homelab.lan:7878/store
````


If you have been working and testing your triplestore, we can reset it to empty with:

> WARNING: use this with caution!

```bash
curl -i -X POST -H 'Content-Type: application/sparql-update' --data 'DROP ALL' http://homelab.lan:7878/update
```



### biohack.py notes

#### query mode

```bash
python biohack.py query --source http://homelab.lan:7878/query  --sink foo  --query ./sparql/getsubjects.rq --table bar
```

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

`bamlTest.py` is a utility script for sending a markdown file to BAML functions (`ExtractIdea` or `ExtractAssertion`) and saving the JSON output. It can be used for manual testing or exploration of these BAML functions.

> Note: Since this is using [BAML](https://github.com/BoundaryML/baml) it's easy to 
> modify [clients.baml](baml_src/clients.baml) and add in any client.  Ollama, for local,
> Xai, Google Gemini, etc.  You will then need to modify the ``` client "openai/gpt-4o" ```
> in [hypothesis.baml](baml_src/hypothesis.baml) and rerun ```baml-cli generate```

Then run with

```bash
python bamlTest.py --input input.md --output output.json
```




## Notes

```bash
pip install html2text PyPDF2
```

Also worked up a notebook ([typeTypeView.ipynb](notebooks/typeTypeView.ipynb)) to play around with search to visualization approaches.  


References: 

* BioAgent repo: https://github.com/bio-xyz/plugin-bioagent
* DKG (origin trail): https://docs.origintrail.io/build-with-dkg/quickstart-test-drive-the-dkg-in-5-mins
