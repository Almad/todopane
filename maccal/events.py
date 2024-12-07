import datetime
import subprocess
from typing import List, Dict, Any


EVENT_DELIMITER = "---EVENT_DELIMITER---"
# APPLECAL_DATE_FORMAT = "%A %-d %B %Y at %H:%M:%S"
APPLECAL_DATE_FORMAT = "%A %d %B %Y at %H:%M:%S"


def get_calendar_stdout(
    calendar_ids: str, start_date: datetime.date, end_date: datetime.date
) -> str:
    start_date_str = start_date.strftime(APPLECAL_DATE_FORMAT)
    end_date_str = end_date.strftime(APPLECAL_DATE_FORMAT)

    calendar_subroutine = """
        tell calendar "{0}"
		set foundEvents to (every event whose start date ≥ startDate and start date ≤ endDate)
		repeat with anEvent in foundEvents
			set eventProperties to properties of anEvent
			set eventDetails to {{name:summary of eventProperties, startDate:start date of eventProperties, endDate:end date of eventProperties, location:location of eventProperties}}
			copy eventDetails to end of eventList
            copy "{1}" to end of eventList
		end repeat
        end tell
    """

    calendars_subroutine = "\n".join(
        calendar_subroutine.format(calendar_id, EVENT_DELIMITER)
        for calendar_id in calendar_ids
    )

    apple_script = f"""
    set startDate to date "{start_date_str}"
    set endDate to date "{end_date_str}"
    tell application "Calendar"
        set eventList to {{}}

        {calendars_subroutine}

        return eventList
    end tell
    """
    # Execute AppleScript and capture output
    process = subprocess.Popen(
        ["osascript", "-e", apple_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    output, error = process.communicate()

    if error:
        raise Exception(f"AppleScript error: {error.decode()}")

    output_string = output.decode().strip()
    return output_string


def parse_event(raw_event: str) -> Dict[str, Any]:
    # Relies on attribute order from the apple script
    string_left = raw_event
    event = {}
    if not string_left.startswith("name:"):
        raise ValueError(f"Invalid event string: {raw_event}")

    string_left = string_left[5:]
    delimiter = ", startDate:date "
    event_data, string_left = string_left.split(delimiter, 1)
    event["name"] = event_data.strip()

    delimiter = ", endDate:date "
    event_data, string_left = string_left.split(delimiter, 1)
    event["startDate"] = datetime.datetime.strptime(
        event_data.strip(), APPLECAL_DATE_FORMAT
    )

    delimiter = ", location:"
    event_data, string_left = string_left.split(delimiter, 1)
    event["endDate"] = datetime.datetime.strptime(
        event_data.strip(), APPLECAL_DATE_FORMAT
    )

    event["location"] = string_left.strip()

    return event


def get_event_list_from_stdout(output_string: str) -> List[Dict[str, Any]]:
    raw_events = output_string.split(f", {EVENT_DELIMITER}, ")
    # example: name:Daria message, startDate:date Saturday 7 December 2024 at 20:15:00, endDate:date Saturday 7 December 2024 at 20:30:00, location:missing value, calendar:Almad Family Shared
    return [parse_event(raw_event) for raw_event in raw_events]


def get_events(
    config: dict, start_date: datetime.date, end_date: datetime.date
) -> List[Dict[str, Any]]:
    calendar_ids = config["calendars"]["personal"]["names"]
    calendar_ids += config["calendars"]["shared"]["names"]

    output_string = get_calendar_stdout(calendar_ids, start_date, end_date)
    return get_event_list_from_stdout(output_string)
