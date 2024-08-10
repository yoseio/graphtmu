"use client";

import { useSearchParams } from "next/navigation";
import useSWR from 'swr';

import { Input } from "@/components/ui/input"
import { TeacherCard } from "@/components/TeacherCard";
import { keywordsFetcher } from "@/lib/fetchers/keyword";
import { uniq } from "@/lib/utils";
import { useHandleParam } from "@/lib/hooks/useHandleParam";

export default function Page() {
  const searchParams = useSearchParams();
  const handleParam = useHandleParam("keyword");

  const query = searchParams.get("keyword")?.toString();
  const { data } = useSWR(query, keywordsFetcher);
  const teachers = uniq(data || []);

  return (
    <>
      <div className="mb-8">
        <Input
          className="bg-white dark:bg-gray-950"
          placeholder="Search for teachers..."
          onChange={(e) => handleParam(e.target.value)}
          defaultValue={query}
        />
      </div>
      <div className="grid gap-6">
        {teachers.map((teacher) => (
          <TeacherCard key={teacher.identifier} teacher={teacher} />
        ))}
      </div>
    </>
  )
}
