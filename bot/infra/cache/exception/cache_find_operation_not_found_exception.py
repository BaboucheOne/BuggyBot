class CacheFindOperationNotFoundException(RuntimeError):
    MESSAGE: str = "L'opération de recherche dans le cache n'a rien trouvé."

    def __init__(self):
        super().__init__(self.MESSAGE)
