class BadEnvironmentVariableTypeException(RuntimeError):

    MESSAGE = "Environment variable %s should be a %s"

    def __init__(self, environment_variable_name: str, environment_variable_type: type):
        super(self).__init__(
            self.MESSAGE % (environment_variable_name, type(environment_variable_type))
        )
