class ValException:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
    def check_type_float(self):
        for a in self.args + tuple(self.kwargs.values()):
            try:
                data = float(a)
            except ValueError as e:
                return False
        return True
    def check_type_int(self):
        for a in self.args + tuple(self.kwargs.values()):
            try:
                data = int(a)
            except ValueError as e:
                return False
        return True

