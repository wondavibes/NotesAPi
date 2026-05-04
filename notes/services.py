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

def unshare_note(note, users):
    """
    Remove access for given users from a note.

    Args:
        note: Note instance
        users: iterable of User instances

    Returns:
        int: number of removed access entries
    """

    deleted_count, _ = NoteAccess.objects.filter(
        note=note,
        user__in=users
    ).delete()

    return deleted_count

def list_shared_notes(user):
    ...