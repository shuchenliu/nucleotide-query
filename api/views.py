from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import SearchTermSerializer


class QueryView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):

        # use serializer to conduct validation
        serializer = SearchTermSerializer(data=request.data)

        # handle invalid requests
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

