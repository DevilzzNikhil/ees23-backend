from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if not value.isdigit() or len(value) != 10:
        raise ValidationError("Enter a valid phone number")
    else:
        return value


# Create your models here.
class Query(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(verbose_name="email", max_length=60)
    contact = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10), validate_phone_number],
    )
    query = models.CharField(max_length=500)

    def __str__(self):
        return self.query
