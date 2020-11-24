from django.db import models

# Create your models here.


class EmailNewsletter(models.Model):
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
