from bot.cog.chain_of_responsibility.responsibility_handler import ResponsibilityHandler


class StripHandler(ResponsibilityHandler):

    def __init__(self):
        super().__init__()

    def handle(self, request: str):
        return super().handle(request.strip())
