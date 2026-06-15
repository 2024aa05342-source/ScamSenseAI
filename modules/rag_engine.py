def get_knowledge():

    with open(
        "data/fraud_knowledge_base.txt",
        "r",
        encoding="utf-8"
    ) as f:

        knowledge = f.read()

    return knowledge