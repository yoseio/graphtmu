import { Metadata } from "next"
import Link from "next/link";

import { TeacherUseCase } from "@/lib/usecases/teacher";

const teacherUseCase = new TeacherUseCase();

export const metadata: Metadata = {
  title: "All Teachers - GraphTMU",
}

export default async function Page() {
  const teachers = await teacherUseCase.getAllWithCache();

  return (
    <ul>
      {teachers
        .sort((a, b) => a.name.localeCompare(b.name))
        .map((teacher) => (
          <li key={teacher.identifier} className="hover:underline">
            <Link href={`/teacher/${teacher.identifier}`}>
              {teacher.name}
            </Link>
          </li>
      ))}
    </ul>
  )
}
