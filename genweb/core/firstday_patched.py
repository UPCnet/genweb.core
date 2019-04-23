from plone.app.event.base import construct_calendar
from plone.event.utils import is_datetime
from plone.event.utils import is_date
from datetime import timedelta
from plone.event.interfaces import IEventAccessor

def custom_construct_calendar(events, start=None, end=None):
    """Patch to plone.app.event
    The first day of the calendar is not marked even if the event happens in that day
    We use this method instead of the original one in plone.app.event.base.py
    to fix this issue. 

    The same issue is fixed in higher versions of plone.app.event, but these versions 
    does not support plone 4, so we have to fix it by overwriten the method

    """
    if start:
        if is_datetime(start):
            start = start.date()
        assert is_date(start)
    if end:
        if is_datetime(end):
            end = end.date()
        assert is_date(end)

    cal = {}

    def _add_to_cal(cal_data, event, date):
        date_str = date.isoformat()
        if date_str not in cal_data:
            cal_data[date_str] = [event]
        else:
            cal_data[date_str].append(event)
        return cal_data

    for event in events:
        acc = IEventAccessor(event)
        start_date = acc.start.date()
        end_date = acc.end.date()

        # day span between start and end + 1 for the initial date
        range_days = (end_date - start_date).days + 1
        for add_day in range(range_days):
            next_start_date = start_date + timedelta(add_day)  # initial = 0

            # avoid long loops
            if start and end_date < start:
                break  # if the date is completly outside the range
            if start and next_start_date < start:
                continue  # if start is outside but end reaches into range
            if end and next_start_date > end:
                break  # if date is outside range

            _add_to_cal(cal, event, next_start_date)

    return cal


construct_calendar.func_code = custom_construct_calendar.func_code
