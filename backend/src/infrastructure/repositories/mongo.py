import re as re_module
from typing import List, Optional, Tuple
from bson import ObjectId
from datetime import datetime
from pymongo import AsyncMongoClient

from src.core.config import Settings
from src.core.logging import get_logger
from src.core.schemas.contact import ContactExtractionSchema, CardListElement
from src.services.interfaces import ICardRepository
from src.core.exceptions.service import DatabaseConnectionException

logger = get_logger("app.infrastructure.repositories.mongo")


class CardRepository(ICardRepository):
    """
    MongoDB persistence repository implementing ICardRepository.
    Leverages PyMongo 4.x AsyncMongoClient for asynchronous database operations.
    """

    def __init__(self, settings: Settings, client: AsyncMongoClient) -> None:
        self.settings = settings
        self.client = client
        self.db = self.client[self.settings.mongodb_database]
        # Access the collection asynchronously
        self.collection = self.db["cards"]
        logger.finished("CardRepository database collection bindings initialized.")

    async def save_card(self, extraction: ContactExtractionSchema) -> str:
        logger.executing("Saving contact card record to MongoDB collection")
        try:
            # Map extraction schema to dictionary
            # Exclude id during insert as MongoDB generates its own _id
            data = extraction.model_dump(exclude={"id"})

            # Use current timestamp if created_at is not set
            if not data.get("created_at"):
                data["created_at"] = datetime.now()

            # Insert record asynchronously
            result = await self.collection.insert_one(data)
            inserted_id = str(result.inserted_id)
            logger.finished(f"Saved contact card to database with ID: {inserted_id}")
            return inserted_id
        except Exception as e:
            logger.finished(
                f"Database write operation failed: {e}", level=logger.logger.level
            )
            raise DatabaseConnectionException(f"Failed to persist contact card: {e}")

    async def list_cards(
        self, page: int, limit: int, search: Optional[str] = None
    ) -> Tuple[List[CardListElement], int]:
        logger.executing(
            f"Listing paginated scanned cards (page={page}, limit={limit}, search={search})"
        )
        try:
            skip = (page - 1) * limit

            # Build filter: case-insensitive substring search across display-name fields
            if search:
                escaped = re_module.escape(search)
                regex_filter = {"$regex": escaped, "$options": "i"}
                query_filter = {
                    "$or": [
                        {"company_name": regex_filter},
                        {"first_name": regex_filter},
                        {"last_name": regex_filter},
                        {"middle_name": regex_filter},
                    ]
                }
            else:
                query_filter = {}

            # Query count and cursor sorted by created_at descending
            total = await self.collection.count_documents(query_filter)
            cursor = (
                self.collection.find(query_filter)
                .sort("created_at", -1)
                .skip(skip)
                .limit(limit)
            )
            documents = await cursor.to_list()

            items: List[CardListElement] = []
            for doc in documents:
                # 1. Format Display Name: Company Name OR Person's full name
                company = doc.get("company_name")
                first = doc.get("first_name")
                middle = doc.get("middle_name")
                last = doc.get("last_name")

                full_name_parts = [n for n in [first, middle, last] if n]
                full_name = " ".join(full_name_parts)

                display_name = company or full_name or "Unnamed Organization"

                # 2. Build listing element
                items.append(
                    CardListElement(
                        id=str(doc["_id"]),
                        image_url=doc.get("image_url") or "",
                        display_name=display_name,
                        created_at=doc.get("created_at") or datetime.now(),
                    )
                )

            logger.finished(f"Retrieved {len(items)} scanned cards (total={total})")
            return items, total
        except Exception as e:
            logger.finished(
                f"Database read operation failed: {e}", level=logger.logger.level
            )
            raise DatabaseConnectionException(f"Failed to query database cards: {e}")

    async def get_card_by_id(self, card_id: str) -> Optional[ContactExtractionSchema]:
        logger.executing(f"Querying detailed card document with ID: {card_id}")
        try:
            # Validate and convert string ID to ObjectId
            try:
                oid = ObjectId(card_id)
            except Exception:
                logger.finished(
                    f"Invalid card document ID format: {card_id}",
                    level=logger.logger.level,
                )
                return None

            doc = await self.collection.find_one({"_id": oid})
            if not doc:
                logger.finished(f"Contact card document not found with ID: {card_id}")
                return None

            # Re-map Object ID back to standard string field
            doc["id"] = str(doc.pop("_id"))

            logger.finished(
                f"Contact card details successfully loaded for ID: {card_id}"
            )
            return ContactExtractionSchema(**doc)
        except Exception as e:
            logger.finished(f"Database query failed: {e}", level=logger.logger.level)
            raise DatabaseConnectionException(f"Failed to load contact card: {e}")

    async def delete_card(self, card_id: str) -> None:
        logger.executing(f"Deleting card document with ID: {card_id}")
        try:
            oid = ObjectId(card_id)
            result = await self.collection.delete_one({"_id": oid})
            if result.deleted_count == 0:
                logger.finished(f"Card not found for deletion: {card_id}")
        except Exception as e:
            logger.finished(
                f"Database delete operation failed: {e}", level=logger.logger.level
            )
            raise DatabaseConnectionException(f"Failed to delete contact card: {e}")

    async def update_card(
        self, card_id: str, data: dict
    ) -> Optional[ContactExtractionSchema]:
        logger.executing(f"Updating card document with ID: {card_id}")
        try:
            oid = ObjectId(card_id)
            result = await self.collection.update_one({"_id": oid}, {"$set": data})
            if result.matched_count == 0:
                logger.finished(f"Card not found for update: {card_id}")
                return None
            logger.finished(f"Card document updated successfully for ID: {card_id}")
            doc = await self.collection.find_one({"_id": oid})
            if doc:
                doc["id"] = str(doc.pop("_id"))
                return ContactExtractionSchema(**doc)
            return None
        except Exception as e:
            logger.finished(
                f"Database update operation failed: {e}", level=logger.logger.level
            )
            raise DatabaseConnectionException(f"Failed to update contact card: {e}")
