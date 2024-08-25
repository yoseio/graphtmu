import { Fetcher } from 'swr'
import { Teacher } from '@/lib/models/teacher';

export const keywordsFetcher: Fetcher<Teacher[], string> = (keyword: string) =>
  fetch(`/api/keywords?keyword=${keyword}`)
    .then((res) => res.json())
    .then((data) => data as Teacher[]);
