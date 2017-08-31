import rdflib
from django.core.management.base import BaseCommand
from rdflib import RDF
from rdflib.namespace import DC, SKOS

from thesaurus.models import Collection, Concept, Member, Vocabulary


def get_or_create_vocabulary(g, scheme_uri):
    try:
        vocabulary = Vocabulary.objects.get(uri=str(scheme_uri))
    except Vocabulary.DoesNotExist:
        scheme_prefix = None

        for (prefix, namespace) in g.namespace_manager.namespaces():
            if namespace == scheme_uri:
                scheme_prefix = prefix

        vocabulary = Vocabulary.objects.create(uri=scheme_uri, prefix=scheme_prefix)
        collection = Collection.objects.create()

        for title_object in g.objects(subject=scheme_uri, predicate=DC.title):
            vocabulary.set_current_language(title_object.language)
            vocabulary.label = title_object.value
            collection.set_current_language(title_object.language)
            collection.label = title_object.value

        collection.save()
        vocabulary.collection = collection
        vocabulary.save()

    return vocabulary


def create_concept(g, subject):
    data = {
        'uri': str(subject),
        'code': str(subject).split('/')[-1],
        'labels': {},
        'parent_uri': None,
        'scheme': None,
    }

    scheme_uri = g.value(subject, SKOS.inScheme)

    # Ignore concepts not having a scheme for now.
    if not scheme_uri:
        return None

    vocabulary = get_or_create_vocabulary(g, scheme_uri)

    try:
        concept = Concept.objects.get(code=data['code'], vocabulary=vocabulary)

        return concept
    except Concept.DoesNotExist:
        pass

    for (ref, literal) in g.preferredLabel(subject):
        data['labels'][literal.language] = literal.value

    data['parent_uri'] = g.value(subject, SKOS.broader)

    parent_member = None
    # Only consider parent concepts that are part of the same scheme for now.
    if data['parent_uri'] and data['parent_uri'].startswith(scheme_uri):
        parent_concept = create_concept(g, data['parent_uri'])

        try:
            parent_member = Member.objects.get(collection=vocabulary.collection, concept=parent_concept)
        except Member.DoesNotExist:
            pass

    concept = Concept(code=data['code'], vocabulary=vocabulary)

    for (lang, label) in data['labels'].items():
        concept.set_current_language(lang)
        concept.label = label

    concept.save()

    if vocabulary.collection:
        Member.objects.create(collection=vocabulary.collection, concept=concept, parent=parent_member)

    return concept


def import_from_file(file):
    g = rdflib.Graph()
    print("Starting parse. This could take minutes if there are a lot of statements.")
    g.parse(file=file)
    print("Parse ended.")

    print("Importing concepts...")
    count = 0
    for subject in g.subjects(predicate=RDF.type, object=SKOS.Concept):
        create_concept(g, subject)

        count += 1
        if count % 100 == 0:
            print(count)


class Command(BaseCommand):
    help = "Import vocabulary from file(s)"

    def add_arguments(self, parser):
        parser.add_argument('skos_files', nargs="+")

    def handle(self, *args, **options):
        for filename in options['skos_files']:
            with open(filename, "r") as f:
                print("Importing {}.".format(filename))
                import_from_file(f)

        from django.db import connection
        print("Queries: {}".format(len(connection.queries)))
