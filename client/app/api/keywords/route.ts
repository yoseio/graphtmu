import { NextRequest, NextResponse } from "next/server";
import { findTeachersByKeyword } from "@/lib/usecases/teacher";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const keyword = searchParams.get("keyword");
  if (!keyword) {
    return NextResponse.json([]);
  }
  const teachers = await findTeachersByKeyword(keyword);
  return NextResponse.json(teachers);
}
