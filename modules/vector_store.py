import os

def load_knowledge():

    knowledge_chunks = []

    data_folder = "data"

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

                content = f.read()

                entries = content.split("\n")

                for entry in entries:

                    entry = entry.strip()

                    if entry:
                        knowledge_chunks.append(
                            {
                                "source": file_name,
                                "text": entry
                            }
                        )

    return knowledge_chunks

def retrieve_context(user_text):

    knowledge_chunks = load_knowledge()

    user_text = user_text.lower()

    matches = []

    for chunk in knowledge_chunks:

        score = 0

        words = chunk["text"].lower().split()

        for word in words:

            if word in user_text:
                score += 1

        if score > 0:
            matches.append(
                (
                    score,
                    chunk
                )
            )

    matches.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    top_matches = matches[:5]

    return [
        item[1]
        for item in top_matches
    ]