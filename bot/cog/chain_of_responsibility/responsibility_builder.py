from bot.cog.chain_of_responsibility.responsibility_handler import ResponsibilityHandler


class ResponsibilityBuilder:
    def __init__(self):
        self.__handler: ResponsibilityHandler or None = None

    def with_handler(self, handler: ResponsibilityHandler):
        if self.__handler:
            self.__handler.set_next(handler)
        else:
            self.__handler = handler
        return self

    def build(self) -> ResponsibilityHandler:
        return self.__handler
