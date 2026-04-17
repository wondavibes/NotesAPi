from django.apps import AppConfig


class NotesConfig(AppConfig):
    default_auto_field = 'django.db.models.bigAutoField'
    name = 'notes'
    def ready(self):
        import notes.signals  # This imports and registers the signal