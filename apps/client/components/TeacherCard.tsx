import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Teacher } from "@/lib/models/teacher";
import Link from "next/link";

export interface TeacherCardProps {
  teacher: Teacher
}

export function TeacherCard(props: TeacherCardProps) {
  return (
    <Card className="group flex flex-col">
      <CardContent className="p-4 flex-1">
        <Link href={`/teacher/${props.teacher.identifier}`}>
          <h3 className="text-lg font-semibold hover:underline">
            {props.teacher.name}
          </h3>
        </Link>
        <p className="text-muted-foreground">
          {props.teacher.affiliation.map((aff, idx, arr) => (
            `${aff.name}${idx < arr.length - 1 ? ', ' : ''}`
          ))}
        </p>
        <div className="mt-2 flex flex-wrap gap-2">
          {props.teacher.knowsAbout.map(knowsAbout => (
            <Badge key={knowsAbout.identifier} variant="secondary" className="hover:bg-secondary/50">
              {knowsAbout.name}
            </Badge>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
