# README

[TOC]

## About this repository

This repository explore the possibilities provided by:

* [Reactpy](https://reactpy.dev/docs/index.html): React-like and backend-managed web framework. It works similarly to phoenix live views, I selected it [among other](https://github.com/liveviews/liveviews#python) because of its design.
* [Sanic](https://sanic.dev/en/): Framework recommended by Reactpy. It is fast, asynchronous and is a lot alike flask
* [Tortoise-ORM](https://github.com/tortoise/tortoise-orm/tree/0ec208b652b0d4dd03bd1fab7ae94cdafa58b8b7): ORM recommended async framework for Sanic. IIt is fast and support signal management

The [feature explored](#Features explored) are meant to be used in a later project (see [Final Goals](#Final Goals)).
You can run the test file:

```bash
sanic demo
```



## TODO

* Package the utilities once the project is ready
* Create a template using [copier.org](https://copier.readthedocs.io/en/stable/)



## Features explored

### Session management

**Why cookies**

JWT also work (We can store anything in the cookies after all) but it is not useful to keep it on the client side console. `Reactpy` is purely browser-oriented for the responses and the computation are all made in the backend (meaning no `fetch` for the client side).

Cookies are not incompatible with OAuth2.0 and other authentication protocols. It is also the safer choice.



**implementation**

Even if [sanic-session](https://github.com/ahopkins/sanic-session) exists, this is not working well with Reactpy. I therefore took the code [phihos/idom-auth-example-sanic](https://github.com/phihos/idom-auth-example-sanic/tree/main) which is mostly working great and served as a good example of the behaviour of Reactpy.

I added a small utility to manage the sessions:

```python
def use_session():
    request = use_request()
    return request.ctx.session
```



### Javascript execution (e.g. set the title)

This just uses the `script` element, we don't necessarily need to write new frontend component.

We can use a snippet like this one:

```python
@component
def set_title(title):
    if not title:
        return None
    code = """document.title = "{}"; """.format(
        title
    )
    return html.script(code)
```

This will change the title if a value is provided.



### Real-time database

This uses the signal feature of `tortoise-orm`. The issue is that a signal added to a models will stay until the end of the program.
I wrapped the decorators so that we can add single-use callbacks to tortoise. Combine with a `use_state` hook, we can produce a real-time database.

see the `/messages` page

```python
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
```

Each time a message is created, this will update the list of messages and re-render the frontend.



### Delayed/Background tasks

As done with `tortoise-orm`, we can wrap Sanic's `named-task` to produce single-usage calls.
See the `/counter` page

```python
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
```



### Global Store

This wraps Reactpy's context to easily provide a top-level context that acts like a store.

**Declare the store**

```python
configure(app, Store(RootComponent, init=None))
```

Nb: We can use `init` parameter to define a default value. We can also use `Store` in `RootCompoment` and wrap the whole return value.

**Use the store**

```python
store, set_store = use_store()
set_store({**store, "title": "Login"})
```



### Automatic View Generation (WIP)

This is inspired by Odoo's framework. This will create view with read/edit mode, auto-save, pre-defined widget set for the fields, ...



## Final Goals

Provide a simple and automated way to create data driven web project.
The inspiration comes from Odoo:

- Declare a model
- (Add at least one permission)
- and it's done (A default view is generated)
  We just need to declare the fields groupement to define a custom view.


Python "LiveViews": https://github.com/liveviews/liveviews#python





## Other informations discovered

### Sanic automatic documentation

https://sanic.dev/en/plugins/sanic-ext/openapi/basic.html#changing-specification-metadata
localhost:8000/docs


```bash
sanic [file_without_extension] [OPTIONS]
```



### Custom JS component

https://github.com/reactive-python/reactpy-js-component-template
https://reactpy.dev/docs/guides/escape-hatches/javascript-components.html#custom-javascript-components



