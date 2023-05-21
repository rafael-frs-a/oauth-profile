import pytest
import httpx
import respx
from fastapi import status
from src.api import utils
from src.api.v1.auth import clients, schemas


@pytest.mark.anyio
@respx.mock
async def test_authenticate(auth0_oauth_url: str) -> None:
    client = clients.Auth0Client()
    login_request = schemas.LoginRequest(
        code='test-code',
        callbackUrl='http://localhost:3000/login/callback',
        nonce='test-nonce',
    )

    respx.post(auth0_oauth_url).mock(return_value=httpx.Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY))

    response = await client.authenticate(login_request)
    assert not response.success
    assert response.errors
    assert len(response.errors) == 1
    assert response.errors[0].message == 'Failed response from Auth0'

    auth0_response = {'id_token': 'invalid-token'}
    respx.post(auth0_oauth_url).mock(return_value=httpx.Response(
        status_code=status.HTTP_200_OK,
        json=auth0_response
    ))

    response = await client.authenticate(login_request)
    assert not response.success
    assert response.errors
    assert len(response.errors) == 1
    assert response.errors[0].message == 'Invalid id-token response from Auth0'

    payload = {'email': 'john@doe.com', 'nonce': 'fake-nonce'}
    auth0_response['id_token'] = utils.make_app_token(payload)
    respx.post(auth0_oauth_url).mock(return_value=httpx.Response(
        status_code=status.HTTP_200_OK,
        json=auth0_response
    ))

    response = await client.authenticate(login_request)
    assert not response.success
    assert response.errors
    assert len(response.errors) == 1
    assert response.errors[0].message == 'Nonce mismatch'

    payload = {'email': 'john@doe.com', 'nonce': login_request.nonce}
    auth0_response['id_token'] = utils.make_app_token(payload)
    respx.post(auth0_oauth_url).mock(return_value=httpx.Response(
        status_code=status.HTTP_200_OK,
        json=auth0_response
    ))

    response = await client.authenticate(login_request)
    assert not response.success
    assert response.errors
    assert len(response.errors) == 1
    assert response.errors[0].message == 'Invalid response from Auth0'

    auth0_response['access_token'] = 'test-access-token'
    respx.post(auth0_oauth_url).mock(return_value=httpx.Response(
        status_code=status.HTTP_200_OK,
        json=auth0_response
    ))

    response = await client.authenticate(login_request)
    assert response.success
    assert not response.errors
    assert response.data
    assert response.data.accessToken == auth0_response['access_token']
    assert response.data.userInfo
    assert response.data.userInfo['email'] == payload['email']
