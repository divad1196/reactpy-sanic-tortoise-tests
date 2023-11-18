# This is WIP, not used anywhere
from reactpy import component, run, web


_mui = web.module_from_template(
    "react@^17.0.0",
    "@material-ui/core@4.12.4",
    fallback="⌛",
)

Autocomplete = web.export(_mui, "Autocomplete")
Button = web.export(_mui, "Button")