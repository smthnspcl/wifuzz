from threading import Thread


class Runnable(Thread):
    do_run = False
    daemon = True

    def __init__(self, **kwargs):
        Thread.__init__(self)
        self.__dict__.update(kwargs)
        self.do_run = True

    def stop(self):
        self.do_run = False

    def start(self) -> None:
        self.run()
