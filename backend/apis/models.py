from django.db import models
from app_utils.settings import SERVICES

# Create your models here
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
    new_hash = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    news = models.TextField(blank=True, null=True)

class Predictor(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    algo = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    domaine = models.CharField(max_length=255, blank=True, null=True)
    #path = models.CharField(max_length=255, blank=True, null=True
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.CharField(max_length=255, blank=True, null=True) # dev staging, production
    active = models.BooleanField() # on off


class Track(models.Model):
    ml_model = models.ForeignKey(Predictor, on_delete=models.CASCADE)
    feature = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    predict = models.FloatField()

class Mode(models.Model):
    name = models.CharField(
        unique=True, max_length=100, blank=False, null=False, choices=SERVICES
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "apis"

class ApiCallerTask(models.Model):
    current_datetime = models.DateTimeField()
    # end_date = models.DateTimeField(null=False)
    from_tab = models.ForeignKey(Mode, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, blank=True, null=True)


class TransferTask(models.Model):
    current_datetime = models.DateTimeField(null=False)
    from_tab = models.ForeignKey(Mode, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, blank=True, null=True)


class ForecastCallerTask(models.Model):
    agent = models.ForeignKey(Predictor, on_delete=models.CASCADE)
    current_datetime = models.DateTimeField(null=False)
    from_tab = models.ForeignKey(Mode, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, blank=True, null=True)
