from __future__ import absolute_import

from rest_framework import serializers

from .literals import LANGUAGE_CHOICES
from .models import Document, DocumentVersion, DocumentPage, DocumentType


class DocumentPageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DocumentPage


class DocumentVersionSerializer(serializers.HyperlinkedModelSerializer):
    pages = DocumentPageSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = DocumentVersion
        read_only_fields = ('document',)


class DocumentImageSerializer(serializers.Serializer):
    status = serializers.CharField()
    data = serializers.CharField()


class DocumentTypeSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField('get_documents_count')

    class Meta:
        model = DocumentType
        fields = ('id', 'name', 'documents')

    def get_documents_count(self, obj):
        return obj.documents.count()


class DocumentSerializer(serializers.ModelSerializer):
    versions = DocumentVersionSerializer(many=True, read_only=True)
    # TODO: Deprecate, move this as an entry point of DocumentVersion's pages
    image = serializers.HyperlinkedIdentityField(view_name='document-image')
    new_version = serializers.HyperlinkedIdentityField(view_name='document-new-version')
    document_type = DocumentTypeSerializer()

    class Meta:
        fields = ('id', 'label', 'image', 'new_version', 'uuid', 'document_type', 'description', 'date_added', 'versions')
        model = Document


class NewDocumentSerializer(serializers.Serializer):
    description = serializers.CharField(required=False)
    document_type = serializers.ChoiceField(choices=[(document_type.pk, document_type) for document_type in DocumentType.objects.all()])
    expand = serializers.BooleanField(default=False)
    file = serializers.FileField()
    label = serializers.CharField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, blank_display_value=None, required=False)
