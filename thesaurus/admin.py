from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Collection, Concept, Member, Vocabulary


@admin.register(Concept)
class ConceptAdmin(TranslatableAdmin):
    def concept_label(self):
        return self.label

    concept_label.admin_order_field = 'translations__label'

    list_display = ('code', concept_label, 'vocabulary')
    list_filter = ('vocabulary', )
    search_fields = ('code', 'translations__label')
    model = Concept

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        language_code = self.get_queryset_language(request)

        return qs.prefetch_related('translations', 'vocabulary__translations').translated(language_code)


@admin.register(Collection)
class CollectionAdmin(TranslatableAdmin):
    model = Collection


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    def concept_label(self):
        return self.concept.label

    def parent_concept_label(self):
        return self.parent.concept.label if self.parent else None

    def collection_label(self):
        return self.collection.label if self.collection else None

    list_display = (concept_label, parent_concept_label, collection_label,)
    list_filter = ('concept__vocabulary', 'collection')
    raw_id_fields = ('concept', 'parent', )
    search_fields = ('concept__code', 'concept__translations__label')
    model = Member

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.select_related('concept', 'collection', 'parent', 'parent__concept').prefetch_related(
            'concept__translations', 'collection__translations', 'parent__concept__translations')


@admin.register(Vocabulary)
class VocabularyAdmin(TranslatableAdmin):
    model = Vocabulary
