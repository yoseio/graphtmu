import { Identifiable } from "@/lib/models";

export interface Organization extends Identifiable {
  name: string,
  parentOrganization?: Organization,
}

export interface DefinedTerm extends Identifiable {
  name: string,
}

export interface Thing extends Identifiable {
  name: string,
}

export interface ContactPoint extends Identifiable {
  areaServed: string,
  telephone?: string,
}

export interface Teacher extends Identifiable {
  affiliation: Organization[],
  alternateName: string[],
  description: string,
  email?: string,
  jobTitle?: DefinedTerm,
  knowsAbout: Thing[],
  name: string,
  workLocation?: ContactPoint,
}
