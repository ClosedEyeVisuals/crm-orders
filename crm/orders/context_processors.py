from orders.models import Category


def get_categories(request):
    """Добавляет список категорий в контекст."""
    return {
        'categories': Category.objects.all()
    }
