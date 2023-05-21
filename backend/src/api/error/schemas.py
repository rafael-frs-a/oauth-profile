from src.api.schemas import ApiErrorResponse, OpenApiResponse


INVALID_DATA_RESPONSE: OpenApiResponse = {
    '4XX': {
        'model': ApiErrorResponse,
    }
}
