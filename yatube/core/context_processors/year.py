from django.utils import timezone

now = timezone.now()


def year(request):
    # про текущий год я не совсем понял задачу
    """Добавляет переменную с текущим годом."""
    dt = now.year
    return {
        'year': dt
    }
