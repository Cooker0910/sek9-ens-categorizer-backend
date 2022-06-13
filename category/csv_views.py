import datetime
import os
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import tablib
from tablib import Dataset
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .resources import CategoryResource
from utils.csv_utils import (
    export_csv,
    export_excel,
    export_json,
    import_csv,
)

PREFIX_FILE_NAME = 'category'

class ExportCsv(APIView):
    def get(self, request, format=None):
        """
        Download csv file
        """
        return export_csv(request, CategoryResource, PREFIX_FILE_NAME)


class ImportCsv(APIView):
    parser_class = (MultiPartParser,)
    
    def post(self, request, format=None):
        """
        Upload csv file.
        """
        return import_csv(request, CategoryResource)