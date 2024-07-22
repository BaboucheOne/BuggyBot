class MissingEnvironmentVariableException(RuntimeError):

    MESSAGE = "La variable d'environnement %s est introuvable."

    def __init__(self, environment_variable_name: str):
        super().__init__(self.MESSAGE % environment_variable_name)
