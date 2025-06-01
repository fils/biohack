import kuzu
import lancedb
import pandas as pd
import hashlib
from sentence_transformers import SentenceTransformer

db = lancedb.connect("../lancedb")
model = SentenceTransformer("all-MiniLM-L6-v2")

sources_df = pd.DataFrame(db.open_table("sources").to_pandas())
claims_df = pd.DataFrame(db.open_table("claims").to_pandas())
entities_df = pd.DataFrame(db.open_table("entities").to_pandas())

# ['filename' 'id' 'location' 'markdown']
# ---------------------------------
# ['filename' 'node_name' 'index' 'text']
# ---------------------------------
# ['start' 'end' 'text' 'label' 'score' 'filename' 'nodename' 'index']


# claims_df = claims_df[claims_df['filename'] != '2202.05901v2.pdf']
claims_df['composite_id'] = claims_df['filename'] + '_' + claims_df['node_name'] + '_' + claims_df['index'].astype(str)
claims_df['text_embeddings'] = claims_df['text'].apply(lambda x: model.encode(str(x)).tolist())
claims_df = claims_df.dropna(subset=['composite_id'])

# entities_df = entities_df[entities_df['filename'] != '2202.05901v2.pdf']
entities_df['text_md5'] = entities_df['text'].apply(lambda x: hashlib.md5(str(x).encode()).hexdigest())
entities_df['composite_id'] = entities_df['filename'] + '_' + entities_df['nodename'] + '_' + entities_df['index'].astype(str)
entities_df = entities_df.dropna(subset=['composite_id'])

# model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Open a new in-memory database
db = kuzu.Database("./graphdb")
conn = kuzu.Connection(db)
conn.execute("INSTALL vector; LOAD vector;")


# # TODO  bring in the "text" from claims and .. add columns "description" and desc_embedding
# nodes = pd.DataFrame(pd.concat([
#     pd.concat([sources_df['filename'].rename('id'), pd.Series(['source'] * len(sources_df), name='type')], axis=1),
#     pd.concat([claims_df['composite_id'].rename('id'), pd.Series(['claim'] * len(claims_df), name='type')], axis=1),
#     pd.concat([entities_df['text'].rename('id'), pd.Series(['entities'] * len(entities_df), name='type')], axis=1)
# ])).drop_duplicates('id')

# MEW APPROACH
# alternate node table(s) approach
conn.execute("CREATE NODE TABLE SOURCES(id STRING PRIMARY KEY, filename string)")
kuzu_sources_df = pd.DataFrame({
    'id': sources_df['id'],
    'filename': sources_df['filename']
})
conn.execute("COPY SOURCES FROM kuzu_sources_df (ignore_errors=true)")

conn.execute("CREATE NODE TABLE CLAIMS(id STRING PRIMARY KEY, text string, text_embedding FLOAT[384], nodename string, filename string)")
kuzu_sources_df1 = pd.DataFrame({
    'id': claims_df['composite_id'],
    'text': claims_df['text'],
    'text_embeddings': claims_df['text_embeddings'], #.apply(lambda x: str(x)),
    'nodename': claims_df['node_name'],
    'filename': claims_df['filename']
})
conn.execute("COPY CLAIMS FROM kuzu_sources_df1 (ignore_errors=true)")

conn.execute("CREATE NODE TABLE ENTITIES(id STRING PRIMARY KEY, text string, label string, nodename string, filename string)")
kuzu_sources_df2 = pd.DataFrame({
    'id': entities_df['composite_id'],
    'text': entities_df['text'],
    'label': entities_df['label'],
    'nodename': entities_df['nodename'],
    'filename': claims_df['filename']
})
conn.execute("COPY ENTITIES FROM kuzu_sources_df2 (ignore_errors=true)")

# Create the relations dataframe from claims_df
relations_df = pd.concat([
    pd.DataFrame({
        'from': claims_df['composite_id'],
        'to': entities_df['composite_id']
    })
]).dropna()

conn.execute("CREATE REL TABLE IF NOT EXISTS rels( FROM CLAIMS TO ENTITIES)")
res = conn.execute("COPY rels FROM relations_df")

# To get properties of a specific node table
# result = conn.execute("CALL TABLE_INFO('CLAIMS') RETURN *;")
# print(result.get_as_df());

conn.execute("CALL CREATE_VECTOR_INDEX('CLAIMS', 'text_vec_index', 'text_embedding')")
