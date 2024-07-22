class MissingEnvironmentVariableException(RuntimeError):

    MESSAGE = "Environment variable %s is not found."

    def __init__(self, environment_variable_name: str):
        super(self).__init__(self.MESSAGE % environment_variable_name)
