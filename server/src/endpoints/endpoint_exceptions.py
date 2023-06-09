from fastapi import HTTPException, status


class ItemNotFoundException(HTTPException):
    def __init__(self, id, collection_name: str | None = None):
        self.id = id
        self.collection_name = collection_name
        self.message = f"Item id {id} not found or current user has no permission to access it. (collection: {collection_name})"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=self.message)


class NoItemUpdatedException(HTTPException):
    def __init__(self, id, collection_name: str | None = None):
        self.id = id
        self.collection = collection_name
        self.message = f"Item id {id} not found or current user has no permission to access it. No item updated. (collection: {collection_name})"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=self.message)


class NotImplementedException(HTTPException):
    def __init__(self, featureName=None):
        self.featureName = featureName
        if featureName:
            self.message = f"{featureName} not implemented"
        else:
            self.message = f"Feature not implemented"
        super().__init__(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=self.message
        )


class EndPointValidationError(HTTPException):
    def __init__(self, message=None):
        """HTTP 422 Unprocessable Entity - use this exception when validation fails at endpoint."""
        self.message = message
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=self.message
        )


class PermissionValidationError(HTTPException):
    def __init__(self, message=None):
        """HTTP 403 Forbidden - use this exception when operation is not permitted with current user's permissions."""
        self.message = message
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=self.message)


class OpenAIError(HTTPException):
    def __init__(self, message=None, inference_id=None, error=None):
        """Raises HTTP 502 Bad Gateway - use this exception when OpenAI API call returns with error."""
        self.message = message
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "inference_id": str(inference_id),
                "message": self.message,
                "openAI_error_class": error.get("error_class") if error else None,
                "openAI_message": error.get("message") if error else None,
                "openAI_error": error.get("error") if error else None,
            },
        )


class OpenAITimeOutError(HTTPException):
    def __init__(self, message=None, inference_id=None, error=None):
        """Raises HTTP 504 Gateway Timeout - use this if openai api call times out."""
        self.message = message

        super().__init__(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail={
                "inference_id": str(inference_id),
                "message": self.message,
                "openAI_error_class": error.get("error_class") if error else None,
                "openAI_message": error.get("message") if error else None,
                "openAI_error": error.get("error") if error else None,
            },
        )


class MalformedRequestError(HTTPException):
    def __init__(self, message=None):
        """Raises HTTP 400 Bad Request - use this if query/request malformed."""
        self.message = message

        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": self.message,
            },
        )


class EmailAlreadyExistsError(HTTPException):
    def __init__(self, email=None):
        self.message = f"Email `{email}` already exists"

        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=self.message
        )


class CredentialExpiredError(HTTPException):
    def __init__(self):
        self.message = f"Authorization token has expired. Re-authorize and try again"

        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=self.message)
