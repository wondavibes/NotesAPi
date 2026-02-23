from django.db import transaction
from .models import NoteAccess


def share_note(note, shares):
    with transaction.atomic():
        for share in shares:
            user = share["user"]
            access_level = share["access_level"]

            if user == note.owner:
                continue

            NoteAccess.objects.update_or_create(
                note=note,
                user=user,
                defaults={"access_level": access_level},
            )
