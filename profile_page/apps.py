from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profile_page'

    # add this
    def ready(self):
        import profile_page.signals