from os import path

from pydantic import RootModel
from rdflib import Graph
from rdflib_neo4j import HANDLE_VOCAB_URI_STRATEGY, Neo4jStore, Neo4jStoreConfig
from tqdm import tqdm

from grapher import addTeacher
from models.sdo.teacher import Teacher
from utils.constants import (
    DATA_PATH,
    NEO4J_DATABASE,
    NEO4J_PASSWORD,
    NEO4J_URI,
    NEO4J_USER,
)

if __name__ == "__main__":
    config = Neo4jStoreConfig(
        auth_data={
            "uri": NEO4J_URI,
            "database": NEO4J_DATABASE,
            "user": NEO4J_USER,
            "pwd": NEO4J_PASSWORD,
        },
        handle_vocab_uri_strategy=HANDLE_VOCAB_URI_STRATEGY.IGNORE,
        batching=True,
    )

    graph = Graph(store=Neo4jStore(config=config))  # type: ignore
    if len(graph) != 0:
        for triple in graph:
            graph.remove(triple)

    with open(path.join(DATA_PATH, "./teacher.jsonl"), mode="r") as f:
        for line in tqdm(f.readlines()):
            teacher = RootModel[Teacher].model_validate_json(line).root
            addTeacher(graph, teacher)

    graph.close(True)
