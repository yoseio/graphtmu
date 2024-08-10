import Link from "next/link"

import { Card, CardContent } from "@/components/ui/card"
import { Teacher } from "@/lib/teacher"

export interface TeacherCardProps {
  teacher: Teacher
}

export function TeacherCard(props: TeacherCardProps) {
  return (
    <Link href="#">
      <Card className="group flex flex-col">
        <CardContent className="p-4 flex-1">
          <h3 className="text-lg font-semibold">
            {props.teacher.name}
          </h3>
          {/*
          <p className="text-muted-foreground">
            {props.teacher.affiliation[0].identifier}
          </p>
          */}
          <div className="mt-2 flex flex-wrap gap-2">
            {props.teacher.knowsAbout.map(knowsAbout => (
              <span key={knowsAbout} className="rounded-full bg-muted px-3 py-1 text-xs font-medium">
                {knowsAbout}
              </span>
            ))}
          </div>
        </CardContent>
      </Card>
    </Link>
  )
}
