from fastapi import HTTPException, status


class PortfolioInfoDoesNotExists(HTTPException):

    def __init__(self, *args, **kwargs):
        self.detail = 'Portfolio Info isn\'t created! Create it please.'
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(self.status_code, self.detail, kwargs.get('headers'))


class ExistsException(HTTPException):

    def __init__(self, *args, **kwargs):
        detail = kwargs.get('detail')

        self.detail = detail if detail is not None else 'This object is already exists!'
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(self.status_code, self.detail, kwargs.get('headers'))
