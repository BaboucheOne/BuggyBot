class NotFoundException(RuntimeError):

    MESSAGE: str = "L'exception %s n'est pas prise en charge."

    def __init__(self, exception_class: any):
        super().__init__(self.MESSAGE % exception_class)
