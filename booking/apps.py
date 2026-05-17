from django.apps import AppConfig


class BookingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "booking"

    def ready(self):
        # Auto-seed bus data and admin on first run
        try:
            from .views import seed_data
            seed_data()
        except Exception:
            pass  # DB not ready yet (e.g. during migrate), skip silently
