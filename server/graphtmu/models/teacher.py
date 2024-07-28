from typing import List, Optional, Self

from pydantic.dataclasses import dataclass


@dataclass
class Organization:
    """Organization

    https://schema.org/Organization


    Attributes:
        identifier         : https://schema.org/identifier
        name               : https://schema.org/name
        parentOrganization : https://schema.org/parentOrganization
    """

    identifier: str
    name: str
    parentOrganization: Optional[Self]


@dataclass
class DefinedTerm:
    """DefinedTerm

    https://schema.org/DefinedTerm


    Attributes:
        identifier : https://schema.org/identifier
        name       : https://schema.org/name
    """

    identifier: str
    name: str


@dataclass
class ContactPoint:
    """ContactPoint

    https://schema.org/ContactPoint


    Attributes:
        areaServed : https://schema.org/areaServed
        identifier : https://schema.org/identifier
        telephone  : https://schema.org/telephone
    """

    areaServed: str
    identifier: str
    telephone: Optional[str]


@dataclass
class Teacher:
    """Teacher

    https://schema.org/Person


    Attributes:
        affiliation   : https://schema.org/affiliation
        alternateName : https://schema.org/alternateName
        description   : https://schema.org/description
        email         : https://schema.org/email
        identifier    : https://schema.org/identifier
        jobTitle      : https://schema.org/jobTitle
        knowsAbout    : https://schema.org/knowsAbout
        name          : https://schema.org/name
        workLocation  : https://schema.org/workLocation
    """

    affiliation: List[Organization]
    alternateName: List[str]
    description: str
    email: Optional[str]
    identifier: str
    jobTitle: Optional[DefinedTerm]
    knowsAbout: List[str]
    name: str
    workLocation: Optional[ContactPoint]
