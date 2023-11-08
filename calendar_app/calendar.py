from calendar import HTMLCalendar
from datetime import date
from .models import Reservation

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        if day != 0:
            cssclass = 'day'
            today = date.today()
            reservation_dates = Reservation.objects.filter(date__year=self.year, date__month=self.month)
            if date(self.year, self.month, day) in [r.date for r in reservation_dates]:
                cssclass = 'reserved'
            elif date(self.year, self.month, day) < today:
                cssclass = 'past'
            if date(self.year, self.month, day) == today:
                cssclass = 'today'
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def day_cell(self, cssclass, day):
        return f'<td class="{cssclass}">{day}</td>'

    # Format a week as a tr
    def formatweek(self, theweek, events):
        week = ""
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f"<tr>{week}</tr>"

    # Format the month as a table
    def formatmonth(self, withyear=True):
        events = Reservation.objects.filter(date__year=self.year, date__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f"{self.formatmonthname(self.year, self.month, withyear=withyear)}\n"
        cal += f"{self.formatweekheader()}\n"
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"{self.formatweek(week, events)}\n"
        return cal
