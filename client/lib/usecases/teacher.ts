import { unstable_cache } from 'next/cache'

import { TeacherConverter } from "@/lib/converters/teacher";
import { Teacher } from "@/lib/models/teacher";
import { findNearestKeywords, unrefKeyword } from "@/lib/usecases/keyword";
import { FirestoreClient } from "@/lib/clients";

export async function getTeacherById(id: string): Promise<Teacher | undefined> {
  const collection = FirestoreClient
    .collection("teachers")
    .withConverter(TeacherConverter);
  const snapshot = await collection.doc(id).get();
  const data = snapshot.data();
  return data;
}

export const getTeacherByIdCached = unstable_cache(getTeacherById);

export async function getAllTeachers(): Promise<Teacher[]> {
  const collection = FirestoreClient
    .collection("teachers")
    .withConverter(TeacherConverter);
  const snapshot = await collection.get();
  const teachers = snapshot.docs.map(doc => doc.data());
  return teachers;
}

export const getAllTeachersCached = unstable_cache(getAllTeachers);

export async function findTeachersByKeyword(keyword: string): Promise<Teacher[]> {
  const keywords = await findNearestKeywords(keyword);
  const unrefedKeywords = await Promise.all(keywords.map(unrefKeyword));
  const scores: Map<Teacher, number> = new Map();

  unrefedKeywords.forEach((keyword, index) => {
    const weight = 1 / (index + 1);
    keyword.teachers.forEach(teacher => {
      const prevWeight = scores.get(teacher) || 0;
      scores.set(teacher, prevWeight + weight);
    });
  });

  const rankedTeachers = Array.from(scores.entries())
    .sort((a, b) => b[1] - a[1])
    .map(entry => entry[0]);

  return rankedTeachers;
}
