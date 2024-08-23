import { initializeApp, cert, getApps } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore"

const FIREBASE_SERVICE_ACCOUNT_KEY = process.env["FIREBASE_SERVICE_ACCOUNT_KEY"] || "";

if (!getApps()?.length) {
  initializeApp({
    credential: cert(JSON.parse(FIREBASE_SERVICE_ACCOUNT_KEY))
  });
}
export const FirestoreClient = getFirestore();
