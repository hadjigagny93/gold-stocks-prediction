from django.db import models

# Create your models here.
class Current(models.Model):
    header_hash = models.CharField(max_length=255, blank=True, null=True)
    scraping_date = models.CharField(max_length=255, blank=True, null=True)
    new_header = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    public_date = models.CharField(max_length=255, blank=True, null=True)

class Back(models.Model):
    header_hash = models.CharField(max_length=255, blank=True, null=True)
    scraping_date = models.CharField(max_length=255, blank=True, null=True)
    new_header = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    public_date = models.CharField(max_length=255, blank=True, null=True)

class Stock(models.Model):
    date = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    news = models.CharField(max_length=255, blank=True, null=True)

class Predictors(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    algo = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    domaine = models.CharField(max_length=255, blank=True, null=True)
    path = models.CharField(max_length=255, blank=True, null=True)

class Track(models.Model):
    ml_model = models.ForeignKey(Predictors, on_delete=models.CASCADE)
    feature = models.ForeignKey(Stock, on_delete=models.CASCADE)
    predict = models.FloatField()
