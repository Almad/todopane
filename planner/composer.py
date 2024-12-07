import datetime

import maccal

PLAN_TEMPLATE = """
# Plan for {from_date} to {to_date}

{plan_output}
"""


def get_plan(config: dict, from_date: datetime.date, to_date: datetime.date) -> str:
    event_data = maccal.get_events(config, from_date, to_date)

    return PLAN_TEMPLATE.format(
        from_date=from_date, to_date=to_date, plan_output=event_data
    )


def get_daily_plan(config: dict) -> str:
    return get_plan(
        config,
        datetime.date.today() + datetime.timedelta(days=0),
        datetime.date.today() + datetime.timedelta(days=2),
    )
