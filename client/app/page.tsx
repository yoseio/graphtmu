"use client";

import { useSearchParams, usePathname, useRouter } from "next/navigation";
import { useDebouncedCallback } from "use-debounce";
import useSWR, { Fetcher } from 'swr'

import { Input } from "@/components/ui/input"
import { TeacherCard } from "@/components/TeacherCard";
import { Teacher } from "@/lib/teacher";

const fetcher: Fetcher<Teacher[], string> = (query: string) =>
  fetch(`/api/teachers?query=${query}`)
    .then((res) => res.json())
    .then((data) => data as Teacher[]);

export default function Home() {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const { replace } = useRouter();

  const query = searchParams.get("query")?.toString();
  const { data } = useSWR(query, fetcher);
  const teachers = data || [];
  console.log(teachers);

  const handleSearch = useDebouncedCallback((term: string) => {
    const params = new URLSearchParams(searchParams);
    if (term) {
      params.set("query", term);
    } else {
      params.delete("query");
    }
    replace(`${pathname}?${params.toString()}`);
  }, 500);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-8">
        <Input
          className="bg-white dark:bg-gray-950"
          placeholder="Search for teachers..."
          onChange={(e) => handleSearch(e.target.value)}
          defaultValue={query}
        />
      </div>
      <div className="grid gap-6">
        {teachers.map((teacher) => (
          <TeacherCard key={teacher.identifier} teacher={teacher} />
        ))}
      </div>
    </div>
  )
}
