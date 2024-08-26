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
class Thing:
    """Thing

    https://schema.org/Thing


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
        identifier : https://schema.org/identifier
        areaServed : https://schema.org/areaServed
        telephone  : https://schema.org/telephone
    """

    identifier: str
    areaServed: str
    telephone: Optional[str]


@dataclass
class Teacher:
    """Teacher

    https://schema.org/Person


    Attributes:
        identifier    : https://schema.org/identifier
        name          : https://schema.org/name
        affiliation   : https://schema.org/affiliation
        alternateName : https://schema.org/alternateName
        description   : https://schema.org/description
        email         : https://schema.org/email
        jobTitle      : https://schema.org/jobTitle
        knowsAbout    : https://schema.org/knowsAbout
        workLocation  : https://schema.org/workLocation
    """

    identifier: str
    name: str
    affiliation: List[Organization]
    alternateName: List[str]
    description: str
    email: Optional[str]
    jobTitle: Optional[DefinedTerm]
    knowsAbout: List[Thing]
    workLocation: Optional[ContactPoint]
