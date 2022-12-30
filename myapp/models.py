from django.db import models
from django.utils import timezone

# Create your models here.

class Card(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.title

    # Create card link
    def card_link(self):
        return 'http://wanilmie.pythonanywhere.com/'+ self.title.replace(' ', '')

    # Calculate time difference
    def num_day(self):
        if (timezone.now() - self.pub_date).days > 0: # time difference in days [> 0 day]
            return str((timezone.now() - self.pub_date).days)+' day(s) ago'
        elif (timezone.now() - self.pub_date).days <= 0 and (timezone.now() - self.pub_date).total_seconds()// 3600 > 0: # time difference in hours [<= 0 day and > 0 hr]
            return str(round((timezone.now() - self.pub_date).total_seconds()//3600))+' hour(s) ago'
        else: # time difference in minutes [<= 0 hr]
            return str(round((timezone.now() - self.pub_date).total_seconds()//60))+' minute(s) ago'
