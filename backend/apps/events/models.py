from django.db import models


class Event(models.Model):
    type = models.CharField(max_length=100)
    source = models.CharField(max_length=50)
    reference_id = models.BigIntegerField(null=True, blank=True)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '"event"."events"'

    def __str__(self):
        return f'{self.created_at}, {self.source}, {self.type}'