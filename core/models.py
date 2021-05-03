from django.db import models


# Create your models here.
class Employee(models.Model):

    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(max_length=1000)
    date_of_birth = models.DateField()
    join_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=1000, default="")
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=1000, default="")
    last_updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.first_name, self.last_name)


