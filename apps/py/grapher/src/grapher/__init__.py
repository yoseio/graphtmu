from urllib.parse import quote, urljoin

from rdflib import RDF, Graph, Literal, URIRef
from rdflib.namespace import SDO

from models.sdo.teacher import (
    ContactPoint,
    DefinedTerm,
    Organization,
    Teacher,
    Thing,
)


def addOrganization(graph: Graph, data: Organization) -> URIRef:
    URI_BASE = "https://yoseio.github.io/GraphTMU/Organization/"
    sub = URIRef(urljoin(URI_BASE, quote(data.identifier)))
    if len(graph) != 0 and (sub, RDF.type, SDO.Organization) in graph:
        return sub

    graph.add((sub, RDF.type, SDO.Organization))
    graph.add((sub, SDO.identifier, Literal(data.identifier)))
    graph.add((sub, SDO.name, Literal(data.name)))
    if data.parentOrganization:
        parentOrganization = addOrganization(graph, data.parentOrganization)
        graph.add((sub, SDO.parentOrganization, parentOrganization))

    return sub


def addDefinedTerm(graph: Graph, data: DefinedTerm) -> URIRef:
    URI_BASE = "https://yoseio.github.io/GraphTMU/DefinedTerm/"
    sub = URIRef(urljoin(URI_BASE, quote(data.identifier)))
    if len(graph) != 0 and (sub, RDF.type, SDO.DefinedTerm) in graph:
        return sub

    graph.add((sub, RDF.type, SDO.DefinedTerm))
    graph.add((sub, SDO.identifier, Literal(data.identifier)))
    graph.add((sub, SDO.name, Literal(data.name)))

    return sub


def addThing(graph: Graph, data: Thing) -> URIRef:
    URI_BASE = "https://yoseio.github.io/GraphTMU/Thing/"
    sub = URIRef(urljoin(URI_BASE, quote(data.identifier)))
    if len(graph) != 0 and (sub, RDF.type, SDO.Thing) in graph:
        return sub

    graph.add((sub, RDF.type, SDO.Thing))
    graph.add((sub, SDO.identifier, Literal(data.identifier)))
    graph.add((sub, SDO.name, Literal(data.name)))

    return sub


def addContactPoint(graph: Graph, data: ContactPoint) -> URIRef:
    URI_BASE = "https://yoseio.github.io/GraphTMU/ContactPoint/"
    sub = URIRef(urljoin(URI_BASE, quote(data.identifier)))
    if len(graph) != 0 and (sub, RDF.type, SDO.ContactPoint) in graph:
        return sub

    graph.add((sub, RDF.type, SDO.ContactPoint))
    graph.add((sub, SDO.identifier, Literal(data.identifier)))
    graph.add((sub, SDO.areaServed, Literal(data.areaServed)))
    if data.telephone:
        graph.add((sub, SDO.telephone, Literal(data.telephone)))

    return sub


def addTeacher(graph: Graph, data: Teacher) -> URIRef:
    URI_BASE = "https://yoseio.github.io/GraphTMU/Person/"
    sub = URIRef(urljoin(URI_BASE, quote(data.identifier)))
    if len(graph) != 0 and (sub, RDF.type, SDO.Person) in graph:
        return sub

    graph.add((sub, RDF.type, SDO.Person))
    graph.add((sub, SDO.identifier, Literal(data.identifier)))
    graph.add((sub, SDO.name, Literal(data.name)))
    for affiliation in data.affiliation:
        affiliation = addOrganization(graph, affiliation)
        graph.add((sub, SDO.affiliation, affiliation))
    for alternateName in data.alternateName:
        graph.add((sub, SDO.alternateName, Literal(alternateName)))
    graph.add((sub, SDO.description, Literal(data.description)))
    if data.email:
        graph.add((sub, SDO.email, Literal(data.email)))
    if data.jobTitle:
        jobTitle = addDefinedTerm(graph, data.jobTitle)
        graph.add((sub, SDO.jobTitle, jobTitle))
    for knowsAbout in data.knowsAbout:
        knowsAbout = addThing(graph, knowsAbout)
        graph.add((sub, SDO.knowsAbout, knowsAbout))
    if data.workLocation:
        workLocation = addContactPoint(graph, data.workLocation)
        graph.add((sub, SDO.workLocation, workLocation))

    return sub
