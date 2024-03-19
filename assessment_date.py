from datetime import datetime

def assessment_date(string):
    year = string[-4:]
    period = "15/03/"
    # Check if we are in the start or end assessment period
    if "Start" not in string:
        period = "15/11/"
    date = period+year
    parsed_date = datetime.strptime(date, "%d/%m/%Y")
    formatted_date = parsed_date.strftime("%d/%m/%Y")
    return formatted_date, year