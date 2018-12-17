from plone.app.event.base import construct_calendar
from plone.event.utils import is_datetime
from plone.event.utils import is_date
from datetime import timedelta
from plone.event.interfaces import IEventAccessor

def custom_construct_calendar(events, start=None, end=None):
    """Return a dictionary with dates in a given timeframe as keys and the
    actual occurrences for that date for building calendars.
    Long lasting events will occur on every day until their end.

    :param events: List of IEvent and/or IOccurrence objects, to construct a
                   calendar data structure from.
    :type events: list

    :param start: An optional start range date.
    :type start: Python datetime or date

    :param end: An optional start range date.
    :type end: Python datetime or date

    :returns: Dictionary with isoformat date strings as keys and event
              occurrences as values.
    :rtype: dict

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
