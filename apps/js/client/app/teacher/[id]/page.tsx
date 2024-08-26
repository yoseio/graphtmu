import { Metadata, ResolvingMetadata } from "next";
import { notFound } from "next/navigation";

import { Separator } from "@/components/ui/separator";
import { TeacherUseCase } from "@/lib/usecases/teacher";

const teacherUseCase = new TeacherUseCase();

interface Props {
  params: {
    id: string;
  };
}

export async function generateMetadata(
  props: Props,
  parent: ResolvingMetadata,
): Promise<Metadata> {
  const id = props.params.id;
  const teacher = await teacherUseCase.getByIdWithCache(id);

  return {
    title: `${teacher?.name} - GraphTMU`,
  };
}

export async function generateStaticParams() {
  const teachers = await teacherUseCase.getAllWithCache();
  return teachers.map((teacher) => ({ id: teacher.identifier }));
}

export default async function Page(props: Props) {
  const id = props.params.id;
  const teacher = await teacherUseCase.getByIdWithCache(id);

  if (!teacher) {
    notFound();
  }

  return (
    <div className="grid gap-8">
      <div className="grid gap-4">
        <div className="flex items-center gap-4">
          <div className="grid gap-1">
            <h1 className="text-2xl font-bold">{teacher.name}</h1>
            <div className="text-muted-foreground">
              {teacher.jobTitle?.name}
            </div>
          </div>
        </div>
        <div className="grid gap-2 text-muted-foreground">
          <div>
            <span className="font-medium">所属：</span>
            {teacher.affiliation.map(
              (aff, idx, arr) =>
                `${aff.name}${idx < arr.length - 1 ? ", " : ""}`,
            )}
          </div>
          <div>
            <span className="font-medium">メール：</span>
            {teacher.email}
          </div>
        </div>
      </div>
      <Separator />
      <div className="grid gap-4">
        <h2 className="text-lg font-semibold">研究テーマ</h2>
        <p className="text-muted-foreground">{teacher.description}</p>
      </div>
    </div>
  );
}
