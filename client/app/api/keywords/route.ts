import { NextRequest, NextResponse } from "next/server";

import { TeacherUseCase } from "@/lib/usecases/teacher";

const teacherUseCase = new TeacherUseCase();

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const keyword = searchParams.get("keyword");
  if (!keyword) {
    return NextResponse.json([]);
  }
  const teachers = await teacherUseCase.findByKeyword(keyword);
  return NextResponse.json(teachers);
}
