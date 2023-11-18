from uuid import uuid4

# https://sanic.dev/en/guide/basics/tasks.html#named-tasks
def callback_once(app):
    def decorator(f):
        callback_once_uuid = uuid4()
        async def callback_once():
            await f()
            await app.cancel_task(callback_once_uuid)
        app.add_task(callback_once(), name=callback_once_uuid)
        return f
    return decorator