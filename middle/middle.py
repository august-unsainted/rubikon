import eel

from back.get_info import get_main_info, get_hours, get_end


@eel.expose
def get_info(values: dict[str]) -> dict[str]:
    return get_main_info(values)


@eel.expose
def update_hours(start: str, end: str) -> int:
    return get_hours(start, end)


@eel.expose
def update_end(start: str, hours: str) -> str:
    return get_end(start, hours)
