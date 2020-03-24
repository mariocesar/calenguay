from django.shortcuts import render, get_object_or_404

from calenguay.events.models import Category, EventType


def landing(request):
    categories = Category.objects.all()

    return render(request, "landing.html", {"categories": categories})


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    event_types = EventType.objects.filter(user__in=category.users.all())

    return render(request, "categories/detail.html", {
        "category": category,
        "event_types": event_types
    })


def eventtype_detail(request, pk):
    event_type = get_object_or_404(EventType, pk=pk)

    return render(request, "eventtypes/detail.html", {
        "event_type": event_type
    })