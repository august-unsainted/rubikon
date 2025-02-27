from typing import Tuple

import eel

from back.get_info import get_main_info, get_hours, get_end
from back.sheets import *


@eel.expose
def get_info(values: dict[str]) -> dict[str]:
    return get_main_info(values)


@eel.expose
def update_hours(start: str, end: str) -> int:
    return get_hours(start, end)


@eel.expose
def update_end(start: str, hours: str) -> str:
    return get_end(start, hours)


@eel.expose
def get_sheets(values: dict) -> None:
    update_prepayment(values), update_reservation(values)
    color_cells(values['checkbox-payment-confirmed'])
