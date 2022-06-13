import datetime
import os
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from werkzeug.utils import secure_filename
from import_export.formats import base_formats
import tablib
from tablib import Dataset


# Extension csv with custom delimiter
class ECSV(base_formats.CSV):

    def create_dataset(self, in_stream, **kwargs):
        kwargs['delimiter'] = settings.IMPORT_EXPORT_CSV_DELIMITER
        return super().create_dataset(in_stream, **kwargs)

    def export_data(self, dataset, **kwargs):
        kwargs['delimiter'] = settings.IMPORT_EXPORT_CSV_DELIMITER
        return super().export_data(dataset, **kwargs)


def export_csv(request, resource_class, prefix_file_name, query=None):
    item_resource = resource_class()
    
    # dataset = item_resource.export()
    if query:
        dataset = item_resource.export_with_custom_delimiter(query)
    else:
        dataset = item_resource.export_with_custom_delimiter()

    t = datetime.datetime.now()
    t = '{:%Y-%m-%d_%H-%M}'.format(t)
    
    response = HttpResponse(dataset, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{prefix_file_name}-{str_date}.csv"'.format(
      prefix_file_name=prefix_file_name,
      str_date=t
    )
    response['Access-Control-Expose-Headers'] = 'Content-Disposition'
    return response


def import_csv(request, resource_class):
    if 'file' not in request.data:
        raise ParseError("Empty content")

    # Save temp file
    f = request.data['file']
    file_name = secure_filename(request.data['fileName'])
    file_id = file_name
    tmp_file_dir = 'static/upload/'
    tmp_file_path = '{tmp_file_dir}/{file_name}'.format(
        tmp_file_dir = tmp_file_dir,
        file_name = file_name
    )
    stored_path = default_storage.save(tmp_file_path, ContentFile(f.read()))
    # Read csv file from the temp file
    new_items = open(stored_path).read()
    # Read dataset with custom delimiter
    dataset = tablib.import_set(
        new_items,
        format='csv',
        delimiter=settings.IMPORT_EXPORT_CSV_DELIMITER,
        headers=False
    )
    
    # Check header was appeared
    first_row = dataset[0]
    if first_row and first_row[0] == 'id':
        # Remove first row
        del dataset[0]

    # dataset.headers=['name', 'description']
    item_resource = resource_class()
    # Test import now
    result = item_resource.import_data(dataset, dry_run=True)
    # Remove temp file
    os.remove(stored_path)

    if not result.has_errors():
        # Actually import now
        item_resource.import_data(dataset, dry_run=False)
        return Response(status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_403_FORBIDDEN)


def export_json(request, resource_class, prefix_file_name):
    item_resource = resource_class()
    dataset = item_resource.export()
    response = HttpResponse(dataset.json, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="{file_name}.json"'.format(
      file_name=prefix_file_name
    )
    return response


def export_excel(request, resource_class, prefix_file_name):
    item_resource = resource_class()
    dataset = item_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{file_name}.xls"'.format(
      file_name=prefix_file_name
    )
    return response
