from django.shortcuts import render, redirect
from .models import Reservation
from .forms import ReservationForm
import datetime
from .calendar import Calendar

def display_calendar(request, year=None, month=None):
    if year is None or month is None:
        today = datetime.date.today()
        year, month = today.year, today.month

    # Calculate the previous and next months
    prev_month = month - 1 if month > 1 else 12
    prev_year = year - 1 if month == 1 else year
    next_month = month + 1 if month < 12 else 1
    next_year = year + 1 if month == 12 else year

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendar_month', year=year, month=month)
    else:
        form = ReservationForm()

    reservations = Reservation.objects.filter(date__year=year, date__month=month)

    cal = Calendar(year, month)
    html_calendar = cal.formatmonth(withyear=True)

    context = {
        'year': year,
        'month': month,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'reservations': reservations,
        'form': form,
        'html_calendar': html_calendar,
    }

    return render(request, 'calendar_app/calendar.html', context)
