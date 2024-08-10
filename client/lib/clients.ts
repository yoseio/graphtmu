import { initializeApp, cert, getApps } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore"
import OpenAI from "openai";

const FIREBASE_SA_KEY = process.env["FIREBASE_SA_KEY"] || "";
const OPENAI_API_KEY = process.env["OPENAI_API_KEY"] || "";

if (!getApps()?.length) {
  initializeApp({
    credential: cert(JSON.parse(FIREBASE_SA_KEY))
  });
}
export const FirestoreClient = getFirestore();

export const OpenAIClient = new OpenAI({
  apiKey: OPENAI_API_KEY,
});
