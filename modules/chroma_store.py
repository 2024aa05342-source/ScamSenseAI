import os
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="fraud_knowledge"
)


def build_vector_store():

    data_folder = "data"

    documents = []
    ids = []
    metadatas = []

    count = 0

    for file_name in os.listdir(data_folder):

        if file_name.endswith(".txt"):

            file_path = os.path.join(
                data_folder,
                file_name
            )

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as f:

                lines = f.readlines()

                for line in lines:

                    line = line.strip()

                    if line:

                        documents.append(line)

                        ids.append(
                            f"doc_{count}"
                        )

                        metadatas.append(
                            {
                                "source": file_name
                            }
                        )

                        count += 1

    # Avoid duplicate entries if build_db.py is run again
    try:
        client.delete_collection(
            "fraud_knowledge"
        )
    except:
        pass

    collection = client.get_or_create_collection(
        name="fraud_knowledge"
    )

    collection.add(
        documents=documents,
        ids=ids,
        metadatas=metadatas
    )

    print(
        f"Loaded {count} fraud entries"
    )


def retrieve_context(query):

    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    retrieved = []

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    for doc, meta in zip(
        docs,
        metas
    ):

        retrieved.append(
            {
                "source": meta["source"],
                "text": doc
            }
        )

    return retrieved