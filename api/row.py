"""
Row REST API
=================

Rest API for retrieving the Row information for the specified table

:Author: Nik Sumikawa
:Date: Aug 7, 2020
"""

import logging
log = logging.getLogger(__name__)

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

        from table.docs.row import parameters, properties
        self.parameters = parameters.parameters
        self.properties = properties.properties


class TableRowAPI(RestFramework):

    schema = DocSchema()

    def get(self, request):
        """ returns a list of all row index assigned to the Table """

        from django_config.request_params import request_params

        # parse the parameter from the request
        params = request_params(request, ['table', 'row', 'row_id'])

        objects = self.query( Row, **params )

        # return JsonResponse( objects.values(), safe=False )
        return Response(data=objects.values(
            'index',
            'table__name'
        ))



    def post(self, request):
        """ Creates a row object assigned to the table """

        import json

        # parses the json object from the body of the post request
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        table_obj = Table.objects.get_or_create( name = body['table'] )[0]

        row_obj = Row.objects.get_or_create(
            table = table_obj,
            index = body['row']
        )[0]

        return Response(data={'error': False})


    def delete(self, request):
        """ deletes the specified row object """

        import json

        # parses the json object from the body of the post request
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        table_obj = Table.objects.get_or_create( name = body['table'] )[0]


        row_obj = Row.objects.get_or_create(
            table = table_obj,
            index = body['row']
        )[0]


        col_obj.delete()

        return Response(data={'error': False})


    def query_parameters( self, variable, var_list ):
        """ returns a dictionary containing all queryset parameters """

        return {
            'table': Q(row__table__name__in = var_list ),
            'row': Q(row__index__in = var_list ),
            'row_id': Q(row__id__in = var_list ),
        }



urlpatterns = [
    url(r'^row$', TableRowAPI.as_view(), name='TableRowAPI'),
]
