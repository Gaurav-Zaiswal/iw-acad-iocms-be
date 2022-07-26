from django.shortcuts import render
from django.http import HttpResponse
from elasticsearch_dsl import Q
from msrest import Serializer
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework import status

# from classroom.serializers import ClassroomSerializer
from classroom.serializers import ClassroomListElasticSerializer, RecommendationListSerializer
from classroom.documents import ClassroomDocument

from .recommed import ComputeRecommendation


# Create your views here.
class SearchClassroom(APIView, LimitOffsetPagination):
    # serializer_class = ClassroomSerializer
    serializer_class = ClassroomListElasticSerializer
    document_class = ClassroomDocument

    def generate_q_expression(self, query):
        return Q(
            'multi_match', query=query,
            fields=[
                'class_name'
            ], fuzziness='auto'
        )

    def get(self, request, query):
        try:
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            response = search.execute()

            # print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return HttpResponse(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecomendationView(APIView):
    def get(self, request):
        recommended_classes_dict = ComputeRecommendation.generateRecommendation(request)
        serializer = RecommendationListSerializer(recommended_classes_dict, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
 