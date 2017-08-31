import os

import pytest
import rdflib
from rdflib import RDF
from rdflib.namespace import SKOS

from thesaurus.management.commands.import_skos import create_concept
from thesaurus.models import Concept, Vocabulary


@pytest.mark.django_db
def test_import_rdf(vocabulary_factory):
    g = rdflib.Graph()

    test_rdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixtures/example.rdf'))

    with open(test_rdf_path, "r") as f:
        g.parse(file=f)

    for subject in g.subjects(predicate=RDF.type, object=SKOS.Concept):
        create_concept(g, subject)

    vocabulary = Vocabulary.objects.get(uri='http://example.com/onto/example/')

    assert bool(vocabulary.collection)
    assert vocabulary.prefix == 'example'

    assert Concept.objects.all().count() == 6


@pytest.mark.django_db
def test_import_ttl(vocabulary_factory):
    g = rdflib.Graph()

    test_rdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixtures/example.ttl'))

    with open(test_rdf_path, "r") as f:
        g.parse(file=f, format='turtle')

    for subject in g.subjects(predicate=RDF.type, object=SKOS.Concept):
        create_concept(g, subject)

    vocabulary = Vocabulary.objects.get(uri='http://example.com/onto/example/')

    assert bool(vocabulary.collection)
    assert vocabulary.prefix == 'example'

    assert Concept.objects.all().count() == 6
