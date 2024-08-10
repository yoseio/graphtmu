export interface Organization {
  identifier: string,
  name: string,
  parentOrganization?: Organization,
}

export interface DefinedTerm {
  identifier: string,
  name: string,
}

export interface ContactPoint {
  areaServed: string,
  identifier: string,
  telephone?: string,
}

export interface Teacher {
  affiliation: Organization[],
  alternateName: string[],
  description: string,
  email?: string,
  identifier: string,
  jobTitle?: DefinedTerm,
  knowsAbout: string[],
  name: string,
  workLocation?: ContactPoint,
}
