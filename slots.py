
import requests
from datetime import datetime, timedelta

request_url = 'https://backend.dr-plano.com/courses_dates'
bouldergarten_id = 67359814


class Slot:
    def __init__(self, datetime: datetime, available_slots: int):
        self.datetime = datetime
        datetime
        self.available_slots = available_slots


def get_slots(date_time: str) -> str:
    slots = get_all_slots()
    select_time = parse_date_time(date_time)

    if select_time is None:
        return 'Please provide a valid date_time, for example:\n/check mi14'

    message = ''

    if len(date_time) > 2:
        selected_slot_idx = next((i for i, slot in enumerate(
            slots) if slot.datetime == select_time), None)
        if selected_slot_idx is None:
            message += print_no_slots_available(select_time)
            return message

        slot = slots[selected_slot_idx]

        message += print_slot(slot)

        if slot.available_slots == 0:
            message += '\n' + '~ Next free slots are:'
            slot_previous = get_next_available_slot(
                selected_slot_idx, slots, True)
            slot_next = get_next_available_slot(selected_slot_idx, slots)

            if slot_previous:
                message += '\n' + print_slot(slot_previous)
            if slot_next:
                message += '\n' + print_slot(slot_next)
        # else:
        #     message += '\n' + '~ Should I book it for you? (y/n)'

    else:
        slots = list(filter(lambda x: x.datetime.day ==
                     select_time.day and x.available_slots > 0, slots))
        if len(slots) == 0:
            message += print_no_slots_available(select_time, False)
            return message
        
        message += print_slots(slots) + '\n'

    return message


def parse_date_time(input: str) -> datetime:
    weekday = parse_weekday(input[:2].lower())
    time = parse_time(input[2:])
    if weekday is None or time is None:
        return None
    return datetime.combine(weekday.date(), time.time())


def parse_time(time: str) -> datetime:
    time_format = datetime.now()
    if len(time) < 2:
        return time_format

    if len(time) > 2:
        time_format = "%H%M"
    else:
        time_format = "%H"

    try:
        return datetime.strptime(time, time_format)
    except:
        return None


def parse_weekday(weekday: str) -> datetime:
    weekdays = ['mo', 'di', 'mi', 'do', 'fr', 'sa', 'so']
    current_date = datetime.now()
    current_weekday = current_date.weekday()

    # check if weekdays contains the desired weekday
    weekday = weekday.lower()
    if weekday not in weekdays:
        return None
    desired_weekday = weekdays.index(weekday)

    # Calculate the difference between the current day of the week and the desired day of the week
    days_ahead = desired_weekday - current_weekday

    # If the desired day has already passed in the current week
    if days_ahead <= 0:
        days_ahead += 7

    # Add the calculated difference to the current date
    return current_date + timedelta(days=days_ahead)


def get_next_available_slot(current_slot_idx: int, slots: list[Slot], reverse=False) -> Slot | None:
    if not reverse:
        for i in range(current_slot_idx, len(slots)):
            slot = slots[i]
            if slot.available_slots > 0:
                return slot
    else:
        for i in range(current_slot_idx - 1, -1, -1):
            slot = slots[i]
            if slot.available_slots > 0:
                return slot
    return None


def get_all_slots() -> list[Slot]:
    courses_data = fetch_courses_data()
    if not courses_data:
        return []

    # Filter and sort the fetched available days which contain the slot information
    days = list(filter(
        lambda x: x['state'] == 'BOOKABLE' or x['state'] == 'FULLY_BOOKED', courses_data))
    days = sorted(days, key=lambda x: x['dateList'][0]['start'])

    slots = []
    for day in days:
        # get datetime object from misslis
        date_time = datetime.fromtimestamp(day['dateList'][0]['start'] / 1000)
        available_slots = day['maxCourseParticipantCount'] - \
            day['currentCourseParticipantCount']
        slots.append(Slot(date_time, available_slots))

    return slots


def current_time() -> int:
    current_time = datetime.now()
    current_time_unix = current_time.timestamp()
    return int(current_time_unix * 1000)


def fetch_courses_data():
    response = requests.get(
        request_url, params=request_params(), headers=request_headers())

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")


def print_no_slots_available(select_time: datetime, print_time: True) -> str:
    date_time = select_time.strftime('%d.%m.')
    if print_time:
        date_time = select_time.strftime('%d.%m. %H:%M')
    return "No slots available for " + date_time + '\n'


def print_slots(slots: list[Slot]) -> str:
    message = 'Here are the available slots for the ' + slots[0].datetime.strftime('%d.%m.') + ':\n'
    for slot in slots:
        message += print_slot(slot, False) + '\n'
    return message


def print_slot(slot: Slot, print_date = True) -> str:
    slot_expression = "slot" if slot.available_slots == 1 else "slots"
    
    date_time = slot.datetime.strftime('%H:%M')
    if print_date:
        date_time = slot.datetime.strftime('%d.%m. %H:%M')
        
    return f"{date_time} - {slot.available_slots} {slot_expression} available"


def request_params():
    return {
        'id': bouldergarten_id,
        'advanceToFirstMonthWithDates': '',
        'start': current_time(),
        'end': current_time()
    }


def request_headers():
    return {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
