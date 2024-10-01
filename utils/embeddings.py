from langchain_huggingface import HuggingFaceEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore

from numpy import dot
from numpy.linalg import norm


_embeddings = HuggingFaceEmbeddings()

query_store = LocalFileStore("./cache/query-cache/")
doc_store = LocalFileStore("./cache/doc-cache/")

embeddings = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings=_embeddings, query_embedding_cache=query_store,
    document_embedding_cache=doc_store
)

def cosine_similarity(a, b):
    cos_sim = dot(a, b)/(norm(a)*norm(b))
    return cos_sim

if __name__ == "__main__":
    from langchain.docstore.document import Document
    print(embeddings.embed_documents(Document(page_content="Hi")))
    print(embeddings.embed_query("Hi"))