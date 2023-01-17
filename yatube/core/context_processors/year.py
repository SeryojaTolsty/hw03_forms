from django.utils import timezone


def year(request):
    """Добавляет переменную с текущим годом."""
    now = timezone.now()
    dt = now.year
    return {
        'year': dt
    }
