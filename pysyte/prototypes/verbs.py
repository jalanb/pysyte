"""Module to prototype methods as verbs"""

from functools import singledispatch

def register_method(type_, verb_):
    method = getattr(type_, verb_, lambda *x, **y: '')
    return register_function(type_, verb_, method)

def register_function(type_, verb_, function):
    local = globals().get(verb_, False)
    return local.register(type_, function) if local else remote

def register_methods(type_, source=None):
    names = [_ for _ in dir(type_) if _[:2] != '__']
    attrs = [getattr(source if source else type_, _) for _ in names if _ in globals()]
    methods = [_ for _ in attrs if callable(_)]
    for method in methods:
        register_function(type_, method.__name__, method)


@singledispatch
def pull(subject, object_=None, from_=None):
    from_out = f' from {from_}' if from_ else ''
    return f'prototying {subject} is pulling {object_}{from_out}'

