import { unstable_cache } from "next/cache"
import { CollectionReference } from "@google-cloud/firestore";
import { trace } from "@opentelemetry/api"

import { TeacherConverter } from "@/lib/converters/teacher";
import { Teacher } from "@/lib/models/teacher";
import { FirestoreClient } from "@/lib/clients";

const COLLECTION_NAME = "teachers";

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
