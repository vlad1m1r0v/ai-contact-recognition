from pymongo import AsyncMongoClient
from dishka import Provider, Scope, provide

from src.core.config import Settings, settings
from src.services.interfaces import (
    IContactExtractorService,
    ICloudinaryService,
    ICardRepository,
    ICardUsecaseService,
)
from src.services.extractor import ContactExtractorService
from src.services.card_usecase import CardUsecaseService
from src.infrastructure.services.cloudinary import CloudinaryService
from src.infrastructure.repositories.mongo import CardRepository


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
    def provide_mongo_client(self, settings: Settings) -> AsyncMongoClient:
        """
        Provide a singleton AsyncMongoClient connected to MongoDB.
        """
        return AsyncMongoClient(settings.mongodb_url)

    @provide(scope=Scope.APP)
    def provide_extractor_service(self, settings: Settings) -> IContactExtractorService:
        """
        Provide contact extractor service implementing IContactExtractorService.
        """
        return ContactExtractorService(settings)

    @provide(scope=Scope.APP)
    def provide_cloudinary_service(self, settings: Settings) -> ICloudinaryService:
        """
        Provide Cloudinary image hosting service implementing ICloudinaryService.
        """
        return CloudinaryService(settings)

    @provide(scope=Scope.APP)
    def provide_card_repository(
        self, settings: Settings, client: AsyncMongoClient
    ) -> ICardRepository:
        """
        Provide MongoDB card repository implementing ICardRepository.
        """
        return CardRepository(settings, client)

    @provide(scope=Scope.APP)
    def provide_card_usecase_service(
        self,
        extractor: IContactExtractorService,
        cloudinary: ICloudinaryService,
        repository: ICardRepository,
    ) -> ICardUsecaseService:
        """
        Provide card use-case orchestrator implementing ICardUsecaseService.
        """
        return CardUsecaseService(extractor, cloudinary, repository)
