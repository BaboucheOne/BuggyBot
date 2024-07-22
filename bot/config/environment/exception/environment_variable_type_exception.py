class EnvironmentVariableTypeException(RuntimeError):

    MESSAGE: str = "La variable d'environnement %s devrait être de type %s."

    def __init__(self, environment_variable_name: str, environment_variable_type: type):
        super().__init__(
            self.MESSAGE
            % (environment_variable_name, environment_variable_type.__name__)
        )
