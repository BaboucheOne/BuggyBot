class UserNotInServerException(RuntimeError):

    MESSAGE = "L'utilisateur %s n'est pas présent sur le serveur."

    def __init__(self, discord_id: int):
        super().__init__(self.MESSAGE % discord_id)
