# https://github.com/phihos/idom-auth-example-sanic/blob/main/session.py

from reactpy import component, html, hooks
from reactpy.backend.sanic import configure, Options
from reactpy_router import route, simple
from sanic import Sanic
from sanic.response import text
import asyncio

from session import configure_sessions, use_session
from uuid import uuid4


from tortoise.contrib.sanic import register_tortoise


from event_callbacks import on_event
from store import Store, use_store
from callbacks import callback_once
from models import Message

async def create_messages():
    while True:
        await asyncio.sleep(1)
        # print("creating message")
        await Message.create(msg=f"Message: {uuid4()}")

# ======================================


app = Sanic("MyHelloWorldApp")
register_tortoise(
    app, db_url="sqlite://:memory:", modules={"models": ["models"]}, generate_schemas=True
)


@component
def set_title(title):
    if not title:
        return None
    code = """document.title = "{}"; """.format(
        title
    )
    return html.script(code)

@component
def bootstrap(*children):
    store, _ = use_store()
    title = store.get("title")
    return html._(
        # html.h1("Hello, world!"),
        *children,
        html.script(dict(
            src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js",
            integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM",
            crossorigin="anonymous",
        )),
        set_title(title),
    )

@component
def login():
    store, set_store = use_store()
    set_store({**store, "title": "Login"})
    session = use_session()

    error, set_error = hooks.use_state("")
    username, set_username = hooks.use_state(store.get("username", ""))
    password, set_password = hooks.use_state("")
    def handle_login(event):
        if password != "admin":
            set_error("The password must be 'admin' (yeah, this is not safe)")
            return
        if error:
            set_error("")
        session.values["username"] = username
        set_store({**store, "username": username})
    store_username = store.get("username")
    return html.div(
        html.div({"background-color": "red"}, error) if error else "",
        html.input({"value": username, "on_change": use(set_username)}),
        html.input({"value": password, "on_change": use(set_password)}),
        html.span(f"You are logged in as {store_username}" if store_username else "You are not logged in"),
        html.br(),
        html.button({"on_click": handle_login}, "Login"),
        # Form({"birthday": date.today()}),
    )

@component
def counter():
    # https://sanic.dev/en/guide/basics/tasks.html#named-tasks
    counter, set_counter = hooks.use_state(0)

    # Don't use as decorator to prevent linting issues
    # @callback_once(app)
    async def callback():
        await asyncio.sleep(1)
        set_counter(counter + 1)
    callback_once(app)(callback)
    return html.h1(
        f"Counter: {counter}",
    )



@component
def messages():
    messages, set_messages = hooks.use_state([])

    # Don't use as decorator to prevent linting issues
    # @on_event.post_save(Message)
    async def get_messages(
        *args, **kwargs
    ) -> None:
        messages = await Message.all()
        set_messages(messages)

    on_event.post_save(Message)(get_messages)

    return html.div(
        html.h1("Messages"),
        html.ul(
        *[
            html.li(str(message))
            for message in messages
        ]
    
    ))


@component
def home():
    pages = [
        ("Login", "/login"),
        ("Counter", "/counter"),
        ("Messages", "/messages"),
        ("Api - test", "/api/test"),
    ]
    return html.div(
        html.h1("Home"),
        html.ul(
        *[
            html.li(
                html.a({"href": url}, str(title))
            )
            for (title, url) in pages
        ]
    
    ))


@component
def routes():
    return simple.router(
        route("/", home()),
        route("/login", login()),
        route("/counter", counter()),
        route("/messages", messages()),
        route("*", html.h1("Missing Link 🔗‍💥")),
    )



@component
def root():
    store_data = {}
    session = use_session()
    store_data["username"] = session.values.get("username", "")

    return Store(
        bootstrap(routes()),
        init=store_data,
    )


def use(callable):
    return lambda event: callable(event["target"]["value"])

def get_head():
    return html.head(
        html.meta({"charset": "utf-8"}),
        html.meta({"name": "viewport", "content": "width=device-width, initial-scale=1"}),
        html.link(dict(
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css",
            rel="stylesheet",
            integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC",
            crossorigin="anonymous",
        )),
        html.title("Hello, world!"),
    )



@app.get("/api/test")
async def test(request):
    return text("test")

configure(app, root, Options(head=get_head()))
configure_sessions(app)

app.add_task(create_messages) # Note: we are passing the callable and not coroutine object ...

if __name__ == "__main__":
    app.run()


# @app.on_request
# async def do_something(request):
#     if request.route.ctx.label == "something":
#         ...