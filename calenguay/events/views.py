from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import message
from django.shortcuts import get_object_or_404, redirect, render

from calenguay.events.models import Category, Event, EventType


def landing(request):
    categories = Category.objects.all()

    return render(request, "landing.html", {"categories": categories})


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    event_types = EventType.objects.filter(user__in=category.users.all())

    return render(
        request,
        "categories/detail.html",
        {"category": category, "event_types": event_types},
    )


def eventtype_detail(request, pk):
    event_type = get_object_or_404(EventType, pk=pk)

    return render(request, "eventtypes/detail.html", {"event_type": event_type})


class AppointmentForm(forms.Form):
    start_at = forms.DateTimeField()


def eventtype_make_appointment(request, pk):
    event_type = get_object_or_404(EventType, pk=pk)
    form = AppointmentForm(request.POST or None)

    if form.is_valid():
        event = Event(
            eventtype=event_type,
            start_at=form.cleaned_data["start_at"],
            user=request.user,
        )

        try:
            event.full_clean()
        except ValidationError as err:
            messages.error(request, repr(err))
        else:
            event.save()
    else:
        messages.error(request, repr(form.errors))

    return redirect("eventtype_detail", pk=pk)
