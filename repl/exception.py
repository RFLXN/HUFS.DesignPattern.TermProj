class ExitSignal(Exception):
    def __init__(self):
        super(ExitSignal, self).__init__()
