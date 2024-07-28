class ExceptionHandlerNotFoundException(RuntimeError):

    MESSAGE: str = "Exception %s has no handler."

    def __init__(self, exception_class: any):
        super().__init__(self.MESSAGE % exception_class)
