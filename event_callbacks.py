
from threading import Lock

from tortoise.signals import Signals
from tortoise.models import MODEL
from typing import List, Callable, Type, Tuple, Dict

# Tortoise-orm event listen cannot be removed
# This class is used to register single-usage callbacks 
class EventCallbacks:
    _listeners: Dict[Tuple[Signals, Type[MODEL]], List[Callable]] = {}
    _mutex: Lock = Lock()

    @classmethod
    def _register_signal(cls, signal, *senders) -> Callable:
        def decorator(f):
            for sender in senders:
                add_handler = False
                with cls._mutex:
                    callbacks = cls._listeners.setdefault((signal, sender))
                    if callbacks is None:
                        add_handler = True
                        callbacks = cls._listeners[(signal, sender)] = []
                if add_handler:
                    async def signal_handler(*args, **kwargs):
                        with cls._mutex:
                            todo = callbacks.copy()
                            callbacks.clear()
                        for callback in todo:
                            await callback(*args, **kwargs)
                    sender.register_listener(signal, signal_handler)
                callbacks.append(f)
            return f
        return decorator

    @classmethod
    def post_save(cls, *senders) -> Callable:
        return cls._register_signal(Signals.post_save, *senders)
    @classmethod
    def pre_save(cls, *senders) -> Callable:
        return cls._register_signal(Signals.pre_save, *senders)
    @classmethod
    def pre_delete(cls, *senders) -> Callable:
        return cls._register_signal(Signals.pre_delete, *senders)
    @classmethod
    def post_delete(cls, *senders) -> Callable:
        return cls._register_signal(Signals.post_delete, *senders)

on_event = EventCallbacks