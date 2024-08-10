import { FirestoreDataConverter, QueryDocumentSnapshot, WithFieldValue, DocumentData, DocumentReference } from "@google-cloud/firestore";
import { Teacher } from "./teacher";

export interface Keyword {
  keyword: string,
  embedding_field: number[],
  teachers: DocumentReference<Teacher>[],
}

export const KeywordConverter: FirestoreDataConverter<Keyword> = {
  fromFirestore(snapshot: QueryDocumentSnapshot): Keyword {
    const data = snapshot.data();
    return {
      keyword: data.keyword,
      embedding_field: data.embedding_field,
      teachers: data.teachers,
    };
  },
  toFirestore(modelObject: WithFieldValue<Keyword>): WithFieldValue<DocumentData> {
    return {
      keyword: modelObject.keyword,
      embedding_field: modelObject.embedding_field,
      teachers: modelObject.teachers,
    };
  }
};
