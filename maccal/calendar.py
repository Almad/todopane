import subprocess
from typing import List


def get_calendar_ids(calendar_names: List[str]) -> List[str]:
    calendar_list = ", ".join(f'"{name}"' for name in calendar_names)
    applescript = f"""
    tell application "Calendar"
        set calendarIDs to {{}}
        repeat with calName in {{{calendar_list}}}
            try
                set targetCalendar to (first calendar whose name is calName)
                set calID to id of targetCalendar
                set end of calendarIDs to calID
            on error
                set end of calendarIDs to "not_found"
            end try
        end repeat
        return calendarIDs
    end tell
    """

    print(applescript)

    process = subprocess.Popen(
        ["osascript", "-e", applescript],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Get output and error
    output, error = process.communicate()

    if process.returncode != 0:
        raise RuntimeError(f"AppleScript execution failed: {error}")

    # Parse the output - AppleScript returns comma-separated values
    calendar_ids = [id.strip() for id in output.strip().split(",") if id != "not_found"]

    if len(calendar_names) != len(calendar_ids):
        raise ValueError(f"Some calendars not found: {calendar_names}")

    print(calendar_ids)
    return calendar_ids
