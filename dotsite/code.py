def init(self):

    def get():
        return self

    def set(value):
        nonlocal self
        self = value
        return self

    setattr(self, 'set', set)
    setattr(self, 'get', get)
    self.get = get
    return self
