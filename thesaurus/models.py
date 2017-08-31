from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from parler.models import TranslatableModel, TranslatedFields


@python_2_unicode_compatible
class Vocabulary(TranslatableModel):
    translations = TranslatedFields(
        label=models.CharField(max_length=255, null=True, blank=True)
    )
    prefix = models.CharField(max_length=255, null=True, blank=True)
    uri = models.CharField(max_length=255, unique=True, null=True, blank=True)
    # The collection consisting of all the concepts in a vocabulary.
    # It's automatically created when a vocabulary is imported.
    collection = models.ForeignKey('Collection', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "{} ({})".format(self.safe_translation_getter("label", any_language=True), self.prefix)


@python_2_unicode_compatible
class Concept(TranslatableModel):
    translations = TranslatedFields(
        label=models.CharField(max_length=255, null=True, blank=True)
    )
    code = models.CharField(max_length=255, unique=True, null=True, blank=True)
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, blank=True)

    collections = models.ManyToManyField('Collection', through='Member', related_name='concepts')

    def __str__(self):
        return "{} ({})".format(self.safe_translation_getter("label", any_language=True), self.code)


@python_2_unicode_compatible
class Collection(TranslatableModel):
    translations = TranslatedFields(
        label=models.CharField(max_length=255, null=True, blank=True)
    )

    def __str__(self):
        label = self.safe_translation_getter("label", any_language=True)

        return label if label else '(EMPTY LABEL)'


@python_2_unicode_compatible
class Member(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
