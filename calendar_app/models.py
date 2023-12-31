from django.db import models

class Reservation(models.Model):
    date = models.DateField()
    timeslot = models.TimeField()
    user_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user_name} - {self.date} {self.timeslot}"
