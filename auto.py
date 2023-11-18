# WIP: Not used now
# The goal is to provide automatic form management (read/edit modes, automatic widget, ...)
# This is inspired by Odoo ERP.

from reactpy import component, html, hooks
from datetime import datetime, date

def use(callable):
    return lambda event: callable(event["target"]["value"])

@component
def DateField(field, date, set_date, **options):
    return html.input({
        "id": field,
        "name": field,
        "type": "date",
        "value": str(date),
        "on_change": use(set_date)
    })

@component
def DefaultField(field, value, set_value, **options):
    return html.input({
        "id": field,
        "name": field,
        "value": value,
        "on_change": use(set_value)
    })

def _get_field_component(value):
    if isinstance(value, (date, datetime)):
        return DateField
    return DefaultField


def field_component(field, value, **options):
    _component = _get_field_component(value)
    get, set = hooks.use_state(value)
    return _component(field, get, set, **options)


@component
def Form(data):
    # TODO: Create a dictionnary with all the getters
    fields = [
        field_component(f, value)
        for f, value in data.items()
    ]
    return html.div(
        *fields
        # html.button({"on_click": handle_login}, "Login"),
    )