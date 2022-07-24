from django_elasticsearch_dsl import Document, fields  
from django_elasticsearch_dsl.registries import registry

from .models import Classroom

@registry.register_document
class ClassroomDocument(Document):
    
    # creating index for Classroom
    class Index:

        name='classroom'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }
    
    class Django:
        model = Classroom
        
        # The fields of the model you want to be indexed in Elasticsearch
        fields = ['id', 'class_name', 'class_description',]
