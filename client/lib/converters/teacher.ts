import {
  FirestoreDataConverter,
  QueryDocumentSnapshot,
  WithFieldValue,
  DocumentData,
} from "@google-cloud/firestore";
import { Teacher } from "@/lib/models/teacher";

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
