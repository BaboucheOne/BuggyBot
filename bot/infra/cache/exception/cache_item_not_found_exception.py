class CacheItemNotFoundException(RuntimeError):
    MESSAGE: str = "L'élément avec l'identifiant %s n'est pas dans la cache."

    def __init__(self, cache_id: any):
        super().__init__(self.MESSAGE % cache_id)
