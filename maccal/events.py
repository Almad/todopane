from datetime import date
import subprocess
from typing import List, Dict, Any


def get_events(config: dict, start_date: date, end_date: date) -> List[Dict[str, Any]]:
    start_date_str = start_date.strftime("%A %-d %B %Y at %H:%M:%S")
    end_date_str = end_date.strftime("%A %-d %B %Y at %H:%M:%S")

    calendar_ids = config["calendars"]["personal"]["names"]
    calendar_ids += config["calendars"]["shared"]["names"]
    calendar_subroutine = """
        tell calendar "{0}"
		set foundEvents to (every event whose start date ≥ startDate and start date ≤ endDate)
		repeat with anEvent in foundEvents
			set eventProperties to properties of anEvent
			set eventDetails to {{name:summary of eventProperties, startDate:start date of eventProperties, endDate:end date of eventProperties, location:location of eventProperties, calendar:"{0}"}}
			copy eventDetails to end of eventList
		end repeat
        end tell
    """

    calendars_subroutine = "\n".join(
        calendar_subroutine.format(calendar_id) for calendar_id in calendar_ids
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
    print(calendar_ids)
    print(apple_script)

    try:
        # Execute AppleScript and capture output
        process = subprocess.Popen(
            ["osascript", "-e", apple_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        output, error = process.communicate()

        if error:
            raise Exception(f"AppleScript error: {error.decode()}")

        # Parse the output and convert to Python objects
        events = []
        raw_events = output.decode().strip().split(", {")

        for event_str in raw_events:
            if event_str:
                # Clean up the event string
                event_str = event_str.replace("{", "").replace("}", "")
                event_parts = event_str.split(", ")

                event = {}
                for part in event_parts:
                    if ":" in part:
                        key, value = part.split(":", 1)
                        key = key.strip()
                        value = value.strip()
                        event[key] = value

                # Convert date strings to datetime objects
                if "start" in event:
                    event["start"] = datetime.strptime(
                        event["start"], "%Y-%m-%d %H:%M:%S +0000"
                    )
                if "end" in event:
                    event["end"] = datetime.strptime(
                        event["end"], "%Y-%m-%d %H:%M:%S +0000"
                    )

                events.append(event)

        return events

    except Exception as e:
        print(f"Error: {str(e)}")
        return []


# Example usage
if __name__ == "__main__":
    from datetime import datetime, timedelta
    import json
    from datetime import datetime

    # Example dates
    start = datetime.now()
    end = start + timedelta(days=7)

    # Example calendar names
    calendars = ["Work", "Personal"]

    # Get events
    events = get_calendar_events(start, end, calendars)

    # Custom JSON encoder to handle datetime objects
    class DateTimeEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            return super().default(obj)

    # Print events
    for event in events:
        print(json.dumps(event, indent=2, cls=DateTimeEncoder))
        print("-" * 30)
