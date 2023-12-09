class ApiResponse(dict):
    """
    Custom class for structuring API responses.

    This class extends the built-in Python dict and provides a standardized way to create
    API responses with common attributes such as success status, status code, data payload,
    error details, and an optional message.

    Parameters:
        - "success": A boolean indicating the success status of the API request.
        - "code": An integer representing a custom status or error code for the API response.
        - "data": Payload or data associated with the API response (optional, defaults to None).
        - "error": Information about any error that occurred during the API request (optional, defaults to None).
        - "message": A human-readable message providing additional context (optional, defaults to None).

    Example Usage:
    ```
    Creating a successful API response with data
    ApiResponse(
        success=True,
        code=200,
        data={'result': 'value'},
    )

    Creating an API response with an error and message
    ApiResponse(
        success=False,
        code=404,
        error='Not Found',
        message='Resource not found',
    )
    ```
    """

    def __init__(self, success, code, data=None, error=None, message=None):
        super(ApiResponse, self).__init__()
        self['success'] = success
        self['code'] = code

        if data is not None:
            self['data'] = data

        if error is not None:
            self['error'] = error

        if message is not None:
            self['message'] = message
