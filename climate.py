# TODO  Add other apis and data
# TODO fix time drifting (time.sleep(1) is not 100% accurate) 
 
import requests
import time
from datetime import datetime, timezone

NOAA_TOKEN = "yBfEYSwhsUSNjUeZhTorLqdgYIXvfqkW"
seconds_per_hour = 3600
seconds_per_day = 86400
climate_clock_refresh_rate = seconds_per_day

seconds = 0

def get_climate_clock_data():
    climate_clock_resp = requests.get("https://api.climateclock.world/v2/clock.json")
    if(climate_clock_resp.status_code == 200):
        json = climate_clock_resp.json()
        now = datetime.now(timezone.utc)

        renewables = json["data"]["modules"]["renewables_1"]
        renewables_description = json["data"]["modules"]["renewables_1"]["description"]
        renewables_rate = json["data"]["modules"]["renewables_1"]["rate"]
        renewables_timestamp = json["data"]["modules"]["renewables_1"]["timestamp"]
        renewables_initial = json["data"]["modules"]["renewables_1"]["initial"]
        renewables_timestamp_formatted = datetime.fromisoformat(renewables_timestamp)

        seconds_from_renewables_timestamp = (now - renewables_timestamp_formatted).total_seconds()
        renewables_current = renewables_rate * seconds_from_renewables_timestamp + renewables_initial

        carbon_deadline = json["data"]["modules"]["carbon_deadline_1"]
        deadline_description = json["data"]["modules"]["carbon_deadline_1"]["description"]
        deadline = json["data"]["modules"]["carbon_deadline_1"]["timestamp"]
        deadline_formatted = datetime.fromisoformat(deadline)

        data = {
            "deadline_description" : deadline_description,
            "deadline" : deadline_formatted,
            "renewables_current" : renewables_current,
            "renewables_rate" : renewables_rate,
            "renewables_description" : renewables_description
        }
        return data 
        
    else:
        print(f"ERROR, climate clock api: {climate_clock_resp.status_code}")
def get_climate_trace_data():
    climate_trace_resp = requests.get("https://api.climatetrace.org/v7/sources/emissions")
    if(climate_trace_resp.status_code = 200):
        return climate_trace_resp.json()
    
#get data from apis daily
climate_clock_data = get_climate_clock_data()
deadline = climate_clock_data["deadline"]
deadline_description = climate_clock_data["deadline_description"]

renewables_rate = climate_clock_data["renewables_rate"]
renewables_current = climate_clock_data["renewables_current"]
renewables_description = climate_clock_data["renewables_description"]


climate_trace_data = get_climate_trace_data()
total_emissions = climate_trace_data[""]

while(True): # mainloop
    get_climate_trace_data()
    time.sleep(1)
    seconds +=1
     
    #calculate print the time left till the deadline
    now = datetime.now(timezone.utc)
    time_difference = deadline - now

    seconds_until = int(time_difference.total_seconds())
    days_until = int(time_difference.days)

    weeks_until = int(days_until//7)
    days_rem_weeks = days_until % 7

    seconds_rem_days = seconds_until - (days_until * seconds_per_day)
    hours_rem_days = seconds_rem_days//3600
    mins_rem_hours = (seconds_rem_days - (hours_rem_days*3600))//60
    seconds_rem_total = seconds_rem_days - (mins_rem_hours*60+hours_rem_days*3600)
    # calculate the current percent of renewables
    renewables_current += renewables_rate
    
    # print all values
    print(deadline_description)
    print(f"weeks: {weeks_until}")
    print(f"days: {days_rem_weeks}")
    print(f"hours: {hours_rem_days}")
    print(f"mins: {mins_rem_hours}")
    print(f"seconds: {seconds_rem_total}")
    print(renewables_description)
    print(f"{renewables_current:.8f}%") # .8 truncates it to 8 decimal places
    print("\n")

    if(seconds >= seconds_per_day):
        get_climate_clock_data()


    # print the degrees warmed since pre-industrial times (update daily)
    # print the gigatons of CO2 emitted this year (update every second)
    # print the biomass lost due to human actions (figure out how to update this by the second)
