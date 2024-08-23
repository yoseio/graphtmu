import { initializeApp, cert, getApps } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore"

import { FIREBASE_SA_KEY } from "@/lib/constants";

if (!getApps()?.length) {
  initializeApp({
    credential: cert(JSON.parse(FIREBASE_SA_KEY))
  });
}
export const FirestoreClient = getFirestore();
