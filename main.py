from utils.code_parser import extract_functions_from_repo
from utils.embeddings import embeddings, cosine_similarity
import pandas as pd
from pathlib import Path


GITHUB_DATA_DIR = "./knowledge/github"

all_funcs = extract_functions_from_repo(GITHUB_DATA_DIR)


print("Embedding start")

df = pd.DataFrame(all_funcs)
df['code_embedding'] = df['code'].apply(lambda x: embeddings.embed_query(x))
df['filepath'] = df['filepath'].map(lambda x: Path(x).relative_to(GITHUB_DATA_DIR))
df.to_csv("./static/code_search_openai-python.csv", index=False)
df.head()

print("Embedding end")

def search_functions(df, code_query, n=3, pprint=True, n_lines=7):
    embedding = embeddings.embed_query(code_query)
    df['similarities'] = df.code_embedding.apply(lambda x: cosine_similarity(x, embedding))

    res = df.sort_values('similarities', ascending=False).head(n)

    if pprint:
        for r in res.iterrows():
            print(f"{r[1].filepath}:{r[1].function_name}  score={round(r[1].similarities, 3)}")
            print("\n".join(r[1].code.split("\n")[:n_lines]))
            print('-' * 70)

    return res

while True:
    query = input(">> ")
    res = search_functions(df, query, n=3)
    print(res)