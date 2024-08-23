import { unstable_cache } from "next/cache"
import {
  CollectionReference,
  DocumentData,
  FirestoreDataConverter,
  QueryDocumentSnapshot,
  WithFieldValue,
} from "@google-cloud/firestore";
import { trace } from "@opentelemetry/api"

import { Teacher } from "@/lib/models/teacher";
import { FirestoreClient } from "@/lib/clients/firebase";

const COLLECTION_NAME = "teachers";

export const TeacherConverter: FirestoreDataConverter<Teacher> = {
  fromFirestore(snapshot: QueryDocumentSnapshot): Teacher {
    const data = snapshot.data();
    return {
      identifier: data.identifier,
      affiliation: data.affiliation,
      alternateName: data.alternateName,
      description: data.description,
      email: data.email,
      jobTitle: data.jobTitle,
      knowsAbout: data.knowsAbout,
      name: data.name,
      workLocation: data.workLocation,
    };
  },
  toFirestore(modelObject: WithFieldValue<Teacher>): WithFieldValue<DocumentData> {
    return {
      identifier: modelObject.identifier,
      affiliation: modelObject.affiliation,
      alternateName: modelObject.alternateName,
      description: modelObject.description,
      email: modelObject.email,
      jobTitle: modelObject.jobTitle,
      knowsAbout: modelObject.knowsAbout,
      name: modelObject.name,
      workLocation: modelObject.workLocation,
    };
  }
};

export class TeacherRepository {
  private collection: CollectionReference<Teacher>;

  constructor() {
    this.collection = FirestoreClient
      .collection(COLLECTION_NAME)
      .withConverter(TeacherConverter);
  }

  public async getById(id: string): Promise<Teacher | undefined> {
    return await trace
      .getTracer("GraphTMU")
      .startActiveSpan("TeacherRepository.getById", async (span) => {
        try {
          const snapshot = await this.collection.doc(id).get();
          const data = snapshot.data();
          return data;
        } finally {
          span.end()
        }
      })
  }

  public getByIdWithCache(id: string): Promise<Teacher | undefined> {
    return trace
      .getTracer("GraphTMU")
      .startActiveSpan("TeacherRepository.getByIdWithCache", async (span) => {
        try {
          return unstable_cache((id) => this.getById(id))(id);
        } finally {
          span.end()
        }
      })
  }

  public async getAll(): Promise<Teacher[]> {
    return await trace
      .getTracer("GraphTMU")
      .startActiveSpan("TeacherRepository.getAll", async (span) => {
        try {
          const snapshot = await this.collection.get();
          const teachers = snapshot.docs.map(doc => doc.data());
          return teachers;
        } finally {
          span.end()
        }
      })
  }

  public getAllWithCache(): Promise<Teacher[]> {
    return trace
      .getTracer("GraphTMU")
      .startActiveSpan("TeacherRepository.getAllWithCache", async (span) => {
        try {
          return unstable_cache(() => this.getAll())();
        } finally {
          span.end()
        }
      })
  }
}
