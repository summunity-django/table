"""
Table REST API
=================

Rest API for retrieving formatted table

:Author: Nik Sumikawa
:Date: Aug 7, 2020
"""

import logging
log = logging.getLogger(__name__)

import pandas as pd

from rest_framework.response import Response

from django.conf.urls import url
from django.db.models import Q, F

from table.models import *
from django_config.rest_framework import RestFramework
from django_config.doc_framework import DocumentationSchema


class DocSchema(DocumentationSchema):
    """
    Overrides `get_link()` to provide Custom Behavior X
    """
    def __init__( self ):
        super().__init__()

        self.tags =  ['Tables']

        from table.docs.table import parameters, properties
        self.parameters = parameters.parameters
        self.properties = properties.properties


class TableAPI(RestFramework):

    schema = DocSchema()

    def get(self, request):
        """ returns a json object array containing the table contents """

        from django_config.request_params import request_params

        # parse the parameter from the request
        params = request_params(request, ['table', 'table_id'])

        table_obj = self.query( Table, **params )[0]

        # retrieve all cells, row and columns associated to the table
        row_objects = Row.objects.filter( table = table_obj, valid=True )
        col_objects = Column.objects.filter( table = table_obj, valid=True )
        cell_objects = Cell.objects.filter( row__table = table_obj, valid=True )

        # retieve the values for each column, row, and cell
        rows = row_objects.values_list('index', flat=True)
        cols = col_objects.values_list('name', flat=True)
        records = cell_objects.values('col__name', 'row__index', 'value')


        # convert the records into a DataFrame
        table_df = pd.DataFrame(records).pivot(
            index='row__index',
            columns='col__name',
            values='value')


        # add empty columns (with no cells)
        empty_col = set(cols).difference(set(list(table_df.columns)))
        for col in empty_col: table_df[col] = ""

        # add empty rows (with no cells)
        empty_row = list(set(rows).difference(set(list(table_df.index))))
        if len(empty_row) > 0 :
            table_df = table_df.append(pd.DataFrame(index=empty_row))

        # add the index column
        table_df['__index__'] = table_df.index

        # return JsonResponse( objects.values(), safe=False )
        return Response(data=table_df.fillna("").to_dict('records') )



    def post(self, request):
        """ creates the table object based on the provided name """

        import json

        # parses the json object from the body of the post request
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        table_obj = Table.objects.get_or_create( name = body['table'] )[0]

        return Response(data={'error': False})


    def delete(self, request):
        """ deletes the specified table object and all contents """

        import json

        # parses the json object from the body of the post request
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        table_obj = Table.objects.get_or_create( name = body['table'] )[0]
        table_obj.delete()

        return Response(data={'error': False})



    def query_parameters( self, variable, var_list ):
        """ returns a dictionary containing all queryset parameters """

        return {
            'table': Q(name__in = var_list ),
            'table_id': Q(id__in = var_list ),
        }



urlpatterns = [
    url(r'^table$', TableAPI.as_view(), name='TableAPI'),
]
