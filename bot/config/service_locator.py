import logging

logger = logging.getLogger(__name__)


class ServiceLocator:
    __dependencies = {}

    @classmethod
    def register_dependency(cls, dependency_class, service):
        if service in cls.__dependencies:
            logger.error(
                f"ServiceLocator - Dependency {dependency_class.__name__} is already registered"
            )
            raise Exception(
                f"Dependency {dependency_class.__name__} is already registered."
            )
        cls.__dependencies[dependency_class] = service

    @classmethod
    def get_dependency(cls, dependency_class):
        if dependency_class not in cls.__dependencies:
            logger.error(
                f"ServiceLocator - Dependency {dependency_class.__name__} not registered"
            )
            raise Exception(f"Dependency {dependency_class.__name__} not registered.")
        return cls.__dependencies[dependency_class]

    @classmethod
    def clear(cls):
        cls.__dependencies.clear()
        logger.error(f"ServiceLocator - Dependencies cleared")
