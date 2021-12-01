import threading
# A class that takes in a function and a dictionary of arguments.
# The keys in args have to match the parameters in the function.
class DBThread(threading.Thread):
    def __init__(self, function, args):
        super(DBThread, self).__init__()
        self.function = function
        self.args = args
    def run(self):
        try:
            self.function(**self.args)
        except Exception as e:
            print(e)