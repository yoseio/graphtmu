import { FieldValue } from "@google-cloud/firestore";

import { KeywordConverter } from "@/lib/converters/keyword";
import { Keyword, UnrefedKeyword } from "@/lib/models/keyword";
import { Teacher } from "@/lib/models/teacher";
import { FirestoreClient, OpenAIClient } from "@/lib/clients";

export async function findNearestKeywords(keyword: string): Promise<Keyword[]> {
  const embedding = await OpenAIClient.embeddings.create({
    model: "text-embedding-3-small",
    dimensions: 512,
    input: keyword,
  });

  const collection = FirestoreClient
    .collection("keywords")
    .withConverter(KeywordConverter);
  const snapshot = await collection.findNearest(
    "embedding",
    FieldValue.vector(embedding.data[0].embedding),
    { limit: 5, distanceMeasure: "EUCLIDEAN" },
  ).get();
  const docs = snapshot.docs.map((doc) => doc.data());

  return docs;
}

export async function unrefKeyword(keyword: Keyword): Promise<UnrefedKeyword> {
  const snapshots = await Promise.all(keyword.teachers.map(async (ref) => ref.get()));
  const teachers = snapshots.map((snapshot) => snapshot.data()).filter((item): item is Teacher => !!item);

  return {
    keyword: keyword.keyword,
    embedding: keyword.embedding,
    teachers,
  };
}
