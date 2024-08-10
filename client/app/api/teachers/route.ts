import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";
import { initializeApp, cert, getApps } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore"
import { FieldValue } from "@google-cloud/firestore";

import { KeywordConverter } from "@/lib/keyword";

const FIREBASE_SA_KEY = process.env["FIREBASE_SA_KEY"] || "";
const OPENAI_API_KEY = process.env["OPENAI_API_KEY"] || "";


if (!getApps()?.length) {
  initializeApp({
    credential: cert(JSON.parse(FIREBASE_SA_KEY))
  });
}
const FirestoreClient = getFirestore();

const OpenAIClient = new OpenAI({
  apiKey: OPENAI_API_KEY,
});

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get("query");
  if (!query) {
    return NextResponse.json([]);
  }

  const embedding = await OpenAIClient.embeddings.create({
    model: "text-embedding-3-small",
    dimensions: 512,
    input: query,
  });

  const collection = FirestoreClient
    .collection("keywords")
    .withConverter(KeywordConverter);
  const snapshot = await collection.findNearest(
    "embedding_field",
    FieldValue.vector(embedding.data[0].embedding),
    { limit: 5, distanceMeasure: "EUCLIDEAN" },
  ).get();
  const docs = snapshot.docs.map((doc) => doc.data());

  return NextResponse.json(docs);
}
