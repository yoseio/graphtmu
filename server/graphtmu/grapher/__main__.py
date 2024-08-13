if __name__ == "__main__":
    from os import environ

    from dotenv import load_dotenv
    from pydantic import RootModel
    from rdflib import Graph
    from rdflib_neo4j import HANDLE_VOCAB_URI_STRATEGY, Neo4jStore, Neo4jStoreConfig
    from tqdm import tqdm

    from graphtmu.grapher import addTeacher
    from graphtmu.models.teacher import Teacher

    load_dotenv()

    config = Neo4jStoreConfig(
        auth_data={
            "uri": environ["NEO4J_URI"],
            "database": environ["NEO4J_DATABASE"],
            "user": environ["NEO4J_USER"],
            "pwd": environ["NEO4J_PASSWORD"],
        },
        handle_vocab_uri_strategy=HANDLE_VOCAB_URI_STRATEGY.IGNORE,
        batching=True,
    )

    graph = Graph(store=Neo4jStore(config=config))
    if len(graph) != 0:
        for triple in graph:
            graph.remove(triple)

    with open("data/teacher.jsonl", mode="r") as f:
        for line in tqdm(f.readlines()):
            teacher = RootModel[Teacher].model_validate_json(line).root
            addTeacher(graph, teacher)

    graph.close(True)
