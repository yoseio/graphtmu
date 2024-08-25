import { DocumentReference } from "firebase-admin/firestore";
import { Teacher } from "@/lib/models/teacher";

export interface Keyword {
  keyword: string;
  embedding: number[];
  teachers: DocumentReference<Teacher>[];
}

export interface UnrefedKeyword {
  keyword: string;
  embedding: number[];
  teachers: Teacher[];
}
