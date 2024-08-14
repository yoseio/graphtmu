import { FieldValue, CollectionReference } from "@google-cloud/firestore";

import { KeywordConverter } from "@/lib/converters/keyword";
import { Keyword } from "@/lib/models/keyword";
import { FirestoreClient, OpenAIClient } from "@/lib/clients";

const COLLECTION_NAME = "keywords";
const EMBEDDING_MODEL = "text-embedding-3-small";
const EMBEDDING_DIMENSIONS = 512;
const EMBEDDING_FIELD = "embedding";
const EMBEDDING_LIMIT = 10;
const EMBEDDING_MEASURE = "EUCLIDEAN";

export class KeywordRepository {
  private collection: CollectionReference<Keyword>;

  constructor() {
    this.collection = FirestoreClient
      .collection(COLLECTION_NAME)
      .withConverter(KeywordConverter);
  }

  public async findNearest(keyword: string): Promise<Keyword[]> {
    const embedding = await OpenAIClient.embeddings.create({
      model: EMBEDDING_MODEL,
      dimensions: EMBEDDING_DIMENSIONS,
      input: keyword,
    });

    const snapshot = await this.collection.findNearest(
      EMBEDDING_FIELD,
      FieldValue.vector(embedding.data[0].embedding),
      { limit: EMBEDDING_LIMIT, distanceMeasure: EMBEDDING_MEASURE },
    ).get();
    const docs = snapshot.docs.map((doc) => doc.data());

    return docs;
  }
}
