from calendar import HTMLCalendar
from .models import Reservation

class Calendar(HTMLCalendar):
    def __init__(self, year, month):
        super(Calendar, self).__init__()
        self.year = year
        self.month = month

    # Format a day as a td
    def formatday(self, day, events):
        events_per_day = events.filter(date__day=day)
        d = ""
        for event in events_per_day:
            d += f"<li>{event.user_name}</li>"
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul>{d}</ul></td>"
        return '<td></td>'

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
