import eel

from back.get_info import get_main_info, get_hours, get_end, get_addictional_info
from back.sheets import *
from back.generate_password import generate_daily_password


@eel.expose
def get_info(values: dict[str]) -> dict[str]:
    values = get_main_info(values)
    return get_addictional_info(values)


@eel.expose
def get_primary_info(values: dict[str]) -> dict[str]:
    return get_main_info(values)


@eel.expose
def update_hours(start: str, end: str) -> float:
    return get_hours(start, end)


@eel.expose
def update_end(start: str, hours: str) -> str:
    return get_end(start, hours)


@eel.expose
def get_sheets(values: dict) -> None:
    update_prepayment(values), update_reservation(values)
    # color_cells(values['checkbox-payment-confirmed'])


@eel.expose
def generate_password() -> str:
    return generate_daily_password()
