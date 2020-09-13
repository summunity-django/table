from django.db import models

from oAuth.models import User

class Table(models.Model):
    name = models.CharField(max_length=512)

    # valid flag is used to disable content instead of deleting it
    valid = models.BooleanField( default=True )

class Column(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)

    # valid flag is used to disable content instead of deleting it
    valid = models.BooleanField( default=True )

class Row(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    index = models.IntegerField()

    # valid flag is used to disable content instead of deleting it
    valid = models.BooleanField( default=True )


class Cell(models.Model):
    col = models.ForeignKey(Column, on_delete=models.CASCADE)
    row = models.ForeignKey(Row, on_delete=models.CASCADE)

    # date when the product was added
    value = models.CharField(max_length=512)

    # valid flag is used to disable content instead of deleting it
    valid = models.BooleanField( default=True )

    # differentiate between the most uptodate entry and everything else
    archived = models.BooleanField( default=False )

    date = models.DateTimeField(auto_now_add=True)
