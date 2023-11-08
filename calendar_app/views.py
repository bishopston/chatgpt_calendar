from django.shortcuts import render, redirect
from .models import Reservation
from .forms import ReservationForm
import datetime
from .calendar import Calendar
from django.http import JsonResponse

def display_calendar(request, year=None, month=None):
    today = datetime.date.today()
    if year is None or month is None:
        today = datetime.date.today()
        year, month = today.year, today.month

    # Calculate the previous and next months
    prev_month = month - 1 if month > 1 else 12
    prev_year = year - 1 if month == 1 else year
    next_month = month + 1 if month < 12 else 1
    next_year = year + 1 if month == 12 else year
    #month_days = Reservation.objects.filter(date__year=today.year, date__month=today.month)
    # Calculate the list of timeslots from 09:00 to 21:00
    timeslots = [str(i).zfill(2) + ":00" for i in range(9, 22)]

    # Query the database to get reserved timeslots for the given month and year
    reserved_timeslots = Reservation.objects.filter(date__year=year, date__month=month)
    

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendar_month', year=year, month=month)
    else:
        form = ReservationForm()

    #reservations = Reservation.objects.filter(date__year=year, date__month=month)
    reservations = Reservation.objects.filter(date__year=today.year, date__month=today.month)

    cal = Calendar(year, month)
    html_calendar = cal.formatmonth(withyear=True)
    weeks = cal.formatmonth()

    context = {
        'year': year,
        'month': month,
        'weeks': weeks,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'reservations': reservations,
        'form': form,
        'html_calendar': html_calendar,
        'timeslots': timeslots,
        'reserved_timeslots': reserved_timeslots,
        #'month_days': month_days,
    }

    return render(request, 'calendar_app/calendar2.html', context)



def is_timeslot_reserved(request):
    if request.method == "POST":
        date = request.POST.get("date")
        timeslot = request.POST.get("timeslot")
        is_reserved = Reservation.objects.filter(date=date, timeslot=timeslot).exists()
        return JsonResponse({"is_reserved": is_reserved})