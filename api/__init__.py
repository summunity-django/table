""" url patterns for the table api """

from table.api import \
    cell, \
    col, \
    row, \
    table

urlpatterns = []
urlpatterns += cell.urlpatterns
urlpatterns += col.urlpatterns
urlpatterns += row.urlpatterns
urlpatterns += table.urlpatterns
