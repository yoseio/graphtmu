import { Metadata } from "next"
import Link from "next/link";

import { getAllTeachersCached } from "@/lib/usecases/teacher";

export const metadata: Metadata = {
  title: "All Teachers - GraphTMU",
}

export default async function Page() {
  const teachers = await getAllTeachersCached();

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
