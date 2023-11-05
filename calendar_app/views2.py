def display_calendar(request, year=None, month=None):
    class Calendar(HTMLCalendar):
        def __init__(self, year, month):
            super(Calendar, self).__init__()
            self.year = year
            self.month = month

        # Format a day as a td
        def formatday(self, day, events):
            if day != 0:
                cssclass = self.cssclasses[day % 7]
                if day == datetime.date.today().day and self.month == datetime.date.today().month:
                    cssclass += ' today'
                if day in events:
                    cssclass += ' filled'
                return f"<td class='{cssclass}'>{day}</td>"
            return '<td></td>'

        # Format a week as a tr
        def formatweek(self, theweek, events):
            week = ''.join(self.formatday(day, events) for day in theweek)
            return f'<tr>{week}</tr>'

        # Format the month as a table
        def formatmonth(self, withyear=True):
            events = [1, 2, 3]  # Replace with your reservation data
            cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
            cal += self.formatmonthname(self.year, self.month, withyear=withyear)
            cal += self.formatweekheader()
            for week in self.monthdays2calendar(self.year, self.month):
                cal += self.formatweek(week, events)
            return cal

    if year is None or month is None:
        today = datetime.date.today()
        year, month = today.year, today.month

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendar_month', year=year, month=month)
    else:
        form = ReservationForm()

    reservations = Reservation.objects.filter(date__year=year, date__month=month)
    
    # Define the day names
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    cal = Calendar(year, month)
    cal.cssclasses = day_names  # Set day names as custom CSS classes

    html_calendar = cal.formatmonth(withyear=True)

    context = {
        'year': year,
        'month': month,
        'reservations': reservations,
        'form': form,
        'html_calendar': html_calendar,
    }

    return render(request, 'calendar_app/calendar.html', context)
