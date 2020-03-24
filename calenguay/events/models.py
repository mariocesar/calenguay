from datetime import timedelta

from dateutil.relativedelta import relativedelta
from dateutil.rrule import MINUTELY, rrule, rruleset
from django.contrib.auth import get_user_model
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, through="UserCategory", blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class EventType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    duration = models.IntegerField(
        validators=[validators.MinValueValidator(15), validators.MaxValueValidator(60)]
    )

    max_booking_time = models.IntegerField(
        "Tiempo máximo de reserva (en dias)",
        validators=[validators.MinValueValidator(1), validators.MaxValueValidator(30)],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user})"

    def slots(self):
        ruleset = rruleset()

        if not self.rules.all().exists():
            ruleset.rrule(
                rrule(
                    MINUTELY,
                    interval=self.duration,
                    dtstart=now(),
                    until=now() + relativedelta(days=self.max_booking_time),
                )
            )
        else:
            for rule in self.rules.all():
                ruleset.rrule(rule.as_rrule())

        for event in Event.objects.filter(eventtype=self):
            ruleset.exrule(rrule(
                MINUTELY,
                dtstart=event.start_at,
                until=event.ends_at,
            ))

        return ruleset


class EventRule(models.Model):
    class DayOfWeek(models.IntegerChoices):
        MONDAY = 1
        TUESDAY = 2
        WEDNESDAY = 3
        THURSDAY = 4
        FRIDAY = 5
        SATURDAY = 6
        SUNDAY = 7

    class State(models.TextChoices):
        AVAILABLE = "available", "Available"
        UNAVAILABLE = "unavailable", "Unavailable"

    class Type(models.TextChoices):
        DOW = "dow", "Day of the week"
        DATE = "date", "Until date"

    status = models.CharField(
        choices=State.choices, max_length=12, default=State.AVAILABLE
    )

    eventtype = models.ForeignKey(
        EventType, related_name="rules", on_delete=models.CASCADE
    )
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    ruletype = models.CharField(choices=Type.choices, max_length=4)

    # Type.DOW
    rule_dow = models.IntegerField(choices=DayOfWeek.choices, blank=True, null=True)

    # Type.DATE
    rule_to_date = models.DateField(blank=True, null=True)
    rule_from_date = models.DateField(blank=True, null=True)

    def as_rrule(self):
        return rrule()

    def clean(self):
        if self.ruletype == self.Type.DOW:
            if not self.rule_dow:
                raise ValidationError({"rule_dow": "This field is required"})
        elif self.ruletype == self.Type.DATE:
            if not (self.rule_from_date and self.rule_to_date):
                raise ValidationError(
                    {
                        "rule_from_date": "This field is required",
                        "rule_to_date": "This field is required",
                    }
                )

            if not (self.rule_to_date < self.rule_from_date):
                raise ValidationError(
                    {
                        "rule_from_date": "Has to be before to_date",
                        "rule_to_date": "Has to be after from_date",
                    }
                )


class Event(models.Model):
    eventtype = models.ForeignKey(EventType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="events", on_delete=models.CASCADE)

    start_at = models.DateTimeField()
    ends_at = models.DateTimeField(blank=True)

    def __str__(self):
        return f"{self.start_at} {self.ends_at} / {self.eventtype}"

    def clean(self):
        if not self.ends_at:
            self.ends_at = self.start_at + timedelta(minutes=self.eventtype.duration)
