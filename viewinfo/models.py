from django.db import models

# Create your models here.
MONEY = (
    (1, u'RUB'),
    (2, u'USD'),
)

STATE = (
    (1,  u'Ожидает начала торгов'), 
)
class ZakupkiGov(models.Model):
    number = models.CharField(max_length=25)
    placementMethod = models.CharField(max_length = 150)
    name = models.TextField(null = True)
    numberOfLot = models.CharField(max_length=25, null = True)
    nameOfLot = models.TextField(null = True)
    beginPrice = models.FloatField(null = True)
    moneyCode = models.IntegerField(choices = MONEY, null = True)
    OKPDClass = models.TextField(null = True)
    Organization = models.TextField(null = True)
    BeginDate = models.DateField()
    ChangeDate = models.DateField(null = True)
    DescriptionOrder = models.TextField(null = True)
    BeginDateCall = models.DateField()
    EndDateCall = models.TextField(null = True)

class EtpZakazrfTenders(models.Model):
    number = models.CharField(max_length=25)
    subject = models.TextField()
    price = models.FloatField(null=True)
    organizer = models.TextField()
    publication_date_time = models.DateTimeField(null = True)
    start_date_time = models.DateTimeFiled(null = True)
    state = models.IntegerField(choices = STATE)
