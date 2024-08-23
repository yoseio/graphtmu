from dataclasses import asdict
from os import path

from firebase_admin import firestore, initialize_app
from google.cloud.firestore import ArrayUnion
from google.cloud.firestore_v1.vector import Vector
from pydantic import RootModel
from tqdm import tqdm

from graphtmu.extractor.llm import get_embeddings
from graphtmu.models.teacher import Teacher
from graphtmu.scraper.utils import identifier  # TODO: Fix this import
from graphtmu.utils.constants import DATA_PATH

if __name__ == "__main__":
    app = initialize_app()
    db = firestore.client()

    with open(path.join(DATA_PATH, "./teacher.jsonl"), mode="r") as f:
        for line in tqdm(f.readlines()):
            batch = db.batch()

            teacher = RootModel[Teacher].model_validate_json(line).root
            teacher_doc = db.collection("teachers").document(teacher.identifier)
            batch.set(teacher_doc, asdict(teacher))

            knowsAbout = [knowsAbout.name for knowsAbout in teacher.knowsAbout]
            embeddings = get_embeddings(knowsAbout)
            for keyword, embedding in zip(knowsAbout, embeddings):
                keyword = identifier(keyword)
                if keyword is None:
                    continue
                keyword_doc = db.collection("keywords").document(keyword)
                batch.set(
                    keyword_doc,
                    {
                        "keyword": keyword,
                        "embedding": Vector(embedding),
                        "teachers": [],
                    },
                )
                batch.update(keyword_doc, {"teachers": ArrayUnion([teacher_doc])})

            batch.commit()
