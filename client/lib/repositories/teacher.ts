import { CollectionReference } from "@google-cloud/firestore";

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
    const snapshot = await this.collection.doc(id).get();
    const data = snapshot.data();
    return data;
  }

  public async getAll(): Promise<Teacher[]> {
    const snapshot = await this.collection.get();
    const teachers = snapshot.docs.map(doc => doc.data());
    return teachers;
  }
}
