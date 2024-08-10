import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

import { Identifiable } from "@/lib/models";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const uniq = <T extends Identifiable>(arr: T[]): T[] =>
  Array.from(new Map(arr.map((x) => [x.identifier, x])).values());
