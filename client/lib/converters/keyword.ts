import {
  FirestoreDataConverter,
  QueryDocumentSnapshot,
  WithFieldValue,
  DocumentData,
} from "@google-cloud/firestore";
import { Keyword } from "@/lib/models/keyword";

export const KeywordConverter: FirestoreDataConverter<Keyword> = {
  fromFirestore(snapshot: QueryDocumentSnapshot): Keyword {
    const data = snapshot.data();
    return {
      keyword: data.keyword,
      embedding: data.embedding,
      teachers: data.teachers,
    };
  },
  toFirestore(modelObject: WithFieldValue<Keyword>): WithFieldValue<DocumentData> {
    return {
      keyword: modelObject.keyword,
      embedding: modelObject.embedding,
      teachers: modelObject.teachers,
    };
  }
};
