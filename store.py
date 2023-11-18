from reactpy import hooks

GlobalStore = hooks.create_context(None)

def use_store():
    store, set_store = hooks.use_context(GlobalStore)
    return store, set_store

def Store(component, /, init=None):
    if init is None:
        init = {}
    store, set_store = hooks.use_state(init)
    return GlobalStore(
        component,
        value=(store, set_store)
    )