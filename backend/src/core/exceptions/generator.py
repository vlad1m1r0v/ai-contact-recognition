from typing import Type, TYPE_CHECKING
from starlette import status

if TYPE_CHECKING:
    from src.core.exceptions.base import DefaultHTTPException


class ExamplesGenerator:
    """
    Class to generate the examples for the OpenAPI docs.
    """

    @staticmethod
    def generate_nested_schema_for_code(responses: dict, error_code: int) -> None:
        """
        Generate the nested schema for the given error code.
        """
        responses[error_code] = {}
        responses[error_code]["content"] = {}
        responses[error_code]["content"]["application/json"] = {}

    @classmethod
    def generate_examples(
        cls,
        *args: Type["DefaultHTTPException"],
        auth: bool = False,
        user: bool = False,
        role: bool = False,
    ) -> dict:
        """
        Generate the error responses for the OpenAPI docs.
        """
        responses: dict = {}
        error_codes = {error.status_code for error in args}

        for error_code in error_codes:
            examples = {}

            for error in args:
                instance = error()
                if instance.status_code == error_code:
                    examples[instance.error] = instance.example()

            cls.generate_nested_schema_for_code(responses, error_code)
            responses[error_code]["content"]["application/json"]["examples"] = examples

        cls.change_422_validation_schema(responses)

        return responses

    @classmethod
    def change_422_validation_schema(cls, responses: dict) -> None:
        """
        Change the 422 validation schema to match the one used in the API.
        """
        cls.generate_nested_schema_for_code(
            responses, status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        example = {
            "validation_errors": {
                "summary": "Validation Error",
                "value": {
                    "status": 422,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "details": [
                            {
                                "location": "string",
                                "field": "string",
                                "message": "string",
                            },
                        ],
                    },
                },
            },
        }
        responses[status.HTTP_422_UNPROCESSABLE_ENTITY]["content"]["application/json"][
            "examples"
        ] = example


generate_examples = ExamplesGenerator.generate_examples
