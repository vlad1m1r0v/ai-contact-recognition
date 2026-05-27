from dishka import Provider, Scope, provide

from src.core.config import Settings, settings
from src.services.interfaces import IContactExtractorService
from src.services.extractor import ContactExtractorService


class AppModuleProvider(Provider):
    """
    Dishka Provider to register and wire core backend dependencies.
    """

    @provide(scope=Scope.APP)
    def provide_settings(self) -> Settings:
        """
        Provide application settings instance.
        """
        return settings

    @provide(scope=Scope.APP)
    def provide_extractor_service(self, settings: Settings) -> IContactExtractorService:
        """
        Provide contact extractor service implementing IContactExtractorService.
        """
        return ContactExtractorService(settings)
