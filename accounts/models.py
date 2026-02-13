from django.db import models
from django.contrib.auth.models import AbstractUser

class NoteUser(AbstractUser):

    class AccountType(models.TextChoices):
        PRO = "pro", "Pro"
        STANDARD = "standard", "Standard"

    account_type = models.CharField(
        max_length=20, choices=AccountType.choices, default=AccountType.STANDARD
    )
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.username