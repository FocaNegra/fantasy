from .admin_functions import *
from .insert_functions import *
from .update_functions import *

def initialize_calendar(calendar):
    set_calendar_status(calendar, "locked")
    match_report = get_match_report(calendar)

    print(match_report["success"])

    insert_match_report(match_report["match_report"], calendar)
    
    set_calendar_status(calendar, "punctuating")