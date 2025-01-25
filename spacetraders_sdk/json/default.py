from datetime import date, datetime


def default(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return obj
