import { FieldValue, CollectionReference } from "@google-cloud/firestore";
import { trace } from "@opentelemetry/api"

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

  public async getEmbedding(keyword: string): Promise<number[]> {
    return await trace
      .getTracer("GraphTMU")
      .startActiveSpan("KeywordRepository.getEmbedding", async (span) => {
        try {
          const embedding = await OpenAIClient.embeddings.create({
            model: EMBEDDING_MODEL,
            dimensions: EMBEDDING_DIMENSIONS,
            input: keyword,
          });
          return embedding.data[0].embedding;
        } finally {
          span.end()
        }
      })
  }

  public async findNearest(embedding: number[]): Promise<Keyword[]> {
    return await trace
      .getTracer("GraphTMU")
      .startActiveSpan("KeywordRepository.findNearest", async (span) => {
        try {
          const snapshot = await this.collection.findNearest(
            EMBEDDING_FIELD,
            FieldValue.vector(embedding),
            { limit: EMBEDDING_LIMIT, distanceMeasure: EMBEDDING_MEASURE },
          ).get();
          const docs = snapshot.docs.map((doc) => doc.data());
          return docs;
        } finally {
          span.end()
        }
      })
  }
}
