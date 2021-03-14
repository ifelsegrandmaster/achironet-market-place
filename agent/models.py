from django.db import models
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from users.models import User, Photo
from order.models import Order
from sell.models import BankDetails

WEEK_DAYS = dict(
    [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday')
    ]
)

MONTHS = dict([
    (1, "January"),
    (2, "February"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
    (11, "November"),
    (12, "December")
])

# Create your models here.


class AgentProfile(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    phone_number = PhoneNumberField()
    email = models.EmailField(max_length=254)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    address = models.CharField(max_length=90)
    agent_code = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    profile_picture = models.OneToOneField(
        Photo, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_total_earnings(self):
        return sum(item.get_amount() for item in self.commissions.all())


class Commission(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    claimed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    agent = models.ForeignKey(
        AgentProfile, null=False, blank=False, on_delete=models.CASCADE, related_name="commissions")
    bank_details = models.OneToOneField(
        BankDetails, related_name="bank_details", null=True, blank=True, on_delete=models.SET_NULL)

    def get_amount(self):
        return sum(item.get_amount() for item in self.days.all())

    def is_claimable(self):
        return (self.get_amount() > 20)

    def __str__(self):
        return MONTHS[self.created.month]

    def get_weekly_data(self):
        days = self.days.all().order_by('-date')[:7]
        week = []
        for day in days:
            daily_data = {
                'day': WEEK_DAYS[day.date.weekday()],
                'amount': day.get_amount()
            }
            week.append(daily_data)
        return week[::-1]

    def get_monthly_data(self):
        days = self.days.all().order_by('-date')
        month = []
        for day in days:
            daily_data = {
                'day': day.date.day,
                'amount': day.get_amount()
            }
            month.append(daily_data)
        return month[::-1]


def get_yearly_data(agent):
    months = agent.commissions.all().order_by('-created')
    # now get the data for the whole year
    year = []
    for month in months:
        monthly_data = {
            'month': MONTHS[month.created.month],
            'amount': month.get_amount()
        }
        year.append(monthly_data)
    return year[::-1]


class Day(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    commission = models.ForeignKey(
        Commission, null=False, blank=False, on_delete=models.CASCADE, related_name="days"
    )

    def get_amount(self):
        return sum(item.amount for item in self.earnings.all())


class Earning(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    day = models.ForeignKey(
        Day, null=False, blank=False, on_delete=models.CASCADE, related_name="earnings"
    )
    order = models.ForeignKey(
        Order, null=False, blank=False, on_delete=models.CASCADE, related_name="agent_earnings")
    created = created = models.DateTimeField(auto_now_add=True)
