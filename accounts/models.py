from django.db import models
from django.contrib.auth.models import AbstractUser

class NoteUser(AbstractUser):

    class AccountType(models.TextChoices):
        PRO = "pro", "Pro"
        STANDARD = "standard", "Standard"

    account_type = models.CharField(
        max_length=20, choices=AccountType.choices, default=AccountType.STANDARD
    )
    email = models.EmailField(unique=True)
    def __str__(self):
        return f"{self.username} {self.email} {self.account_type}"


"""
def __str__(self):
    display = self.get.full_name() or self.username
    if self.account_type:
    display += f'self.account_type'
    return display
    """