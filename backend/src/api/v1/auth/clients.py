import httpx
from urllib.parse import urlencode
from fastapi import status
from pydantic.error_wrappers import ValidationError
from src.api import utils
from src.api.schemas import ApiError
from . import config, schemas


class Auth0Client:
    def get_authorization_data(
        self,
        nonce: str,
        authorize_request: schemas.AuthorizeRequest
    ) -> schemas.Authorization:
        params = {
            'response_type': 'code',
            'client_id': config.AUTH0_CLIENT_ID,
            'redirect_uri': authorize_request.callbackUrl,
            'scope': 'openid profile email',
            'nonce': nonce,
        }

        authorization_url = f'{config.AUTH0_BASE_URL}/authorize?{urlencode(params)}'
        params = {}

        if authorize_request.redirectAfterLogoutUrl:
            params['client_id'] = config.AUTH0_CLIENT_ID
            params['returnTo'] = authorize_request.redirectAfterLogoutUrl

        logout_url = f'{config.AUTH0_BASE_URL}/v2/logout?{urlencode(params)}'
        return schemas.Authorization(
            authorizationUrl=authorization_url,
            logoutUrl=logout_url,
            nonce=nonce
        )

    async def authenticate(
        self,
        login_request: schemas.LoginRequest
    ) -> schemas.Auth0Response:
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'authorization_code',
            'client_id': config.AUTH0_CLIENT_ID,
            'client_secret': config.AUTH0_CLIENT_SECRET,
            'code': login_request.code,
            'redirect_uri': login_request.callbackUrl,
        }

        url = f'{config.AUTH0_BASE_URL}/oauth/token'

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, data=data)

        if not response.is_success:
            error = ApiError(
                message='Failed response from Auth0',
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
            return schemas.Auth0Response(errors=[error])

        response_json = response.json()
        access_token = response_json.get('access_token')
        id_token = response_json.get('id_token')
        decode_result = utils.decode_jwt_token(id_token, verify_signature=False)

        if not decode_result.success:
            error = ApiError(
                message='Invalid id-token response from Auth0',
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
            return schemas.Auth0Response(errors=[error])

        user_info = decode_result.data or {}
        unwanted_keys = ['iss', 'aud', 'iat', 'exp', 'sid']

        for key in unwanted_keys:
            user_info.pop(key, None)

        nonce = user_info.pop('nonce', None)

        if nonce != login_request.nonce:
            error = ApiError(
                message='Nonce mismatch',
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
            return schemas.Auth0Response(errors=[error])

        try:
            result = schemas.Auth0Credentials(
                accessToken=access_token,
                userInfo=user_info,
            )

            return schemas.Auth0Response(data=result)
        except ValidationError:
            error = ApiError(
                message='Invalid response from Auth0',
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
            return schemas.Auth0Response(errors=[error])
