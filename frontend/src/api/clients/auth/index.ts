import BaseClient from "..";
import { getApiClient } from "@/api";
import { ApiResponse } from "@/api/types";
import {
  AuthorizationToken,
  AuthorizeRequest,
  AuthorizeResponse,
  AuthorizeResponseSchema,
  LoginRequest,
  LoginResponse,
  LoginResponseSchema,
  RefreshTokenRequest,
  RefreshTokenResponse,
  RefreshTokenResponseSchema,
} from "./types";
import {
  STORE_KEYS,
  REDIRECTS,
  INVALID_SERVER_RESPONSE,
} from "@/utils/constants";
import Cookies from "@/utils/cookies";
import router from "next/router";

export default class AuthClient extends BaseClient {
  cookies: Cookies;

  constructor(context?: any) {
    super(context);
    this.cookies = new Cookies(this.context);
  }

  async authorize(
    authorizeRequest: AuthorizeRequest
  ): Promise<AuthorizeResponse> {
    const api = getApiClient(this.context);
    const response = await api.post("/auth/authorize", authorizeRequest);
    const parseResult = AuthorizeResponseSchema.safeParse(response.data);

    if (!parseResult.success) return INVALID_SERVER_RESPONSE;

    const result: AuthorizeResponse = response.data;

    if (result.success && result.data!.nonce) {
      this.cookies.setCookie(STORE_KEYS.loginNonce, result.data!.nonce);
    }

    return result;
  }

  loadTokenCookies({ accessToken, refreshToken }: AuthorizationToken) {
    this.cookies.setCookie(STORE_KEYS.appAccessToken, accessToken);
    this.cookies.setCookie(STORE_KEYS.appRefreshToken, refreshToken);
  }

  async login(loginRequest: LoginRequest): Promise<LoginResponse> {
    const api = getApiClient(this.context);
    const nonce = this.cookies.getCookie(STORE_KEYS.loginNonce);

    if (nonce) {
      loginRequest.nonce = nonce;
      this.cookies.deleteCookie(STORE_KEYS.loginNonce);
    }

    const response = await api.post("/auth/login", loginRequest);
    const parseResult = LoginResponseSchema.safeParse(response.data);

    if (!parseResult.success) return INVALID_SERVER_RESPONSE;

    const result: LoginResponse = response.data;

    if (result.success) {
      this.loadTokenCookies(result.data!);
    }

    return result;
  }

  async isLoggedIn(): Promise<boolean> {
    const accessToken = this.cookies.getCookie(STORE_KEYS.appAccessToken);
    return !!accessToken;
  }

  async logout(): Promise<ApiResponse> {
    this.cookies.deleteCookie(STORE_KEYS.appAccessToken);
    this.cookies.deleteCookie(STORE_KEYS.appRefreshToken);
    const result: ApiResponse = {
      success: true,
      data: null,
      errors: null,
    };
    return result;
  }

  accessTokenAccepted(response: ApiResponse): boolean {
    response.errors?.forEach((error) => {
      if (error.status == 401) return false;
    });

    return true;
  }

  async refreshToken(
    refreshTokenRequest: RefreshTokenRequest
  ): Promise<RefreshTokenResponse> {
    await this.logout();
    const api = getApiClient(this.context);
    const response = await api.post("/auth/refresh-token", refreshTokenRequest);
    const parseResult = RefreshTokenResponseSchema.safeParse(response.data);

    if (!parseResult.success) return INVALID_SERVER_RESPONSE;

    const result: RefreshTokenResponse = response.data;

    if (result.success) {
      this.loadTokenCookies(result.data!);
    } else {
      router.push(REDIRECTS.redirectAfterAuthenticationFailed);
    }

    return result;
  }

  async refreshTokenIfRejected(
    method: () => Promise<ApiResponse>,
    ...params: any
  ): Promise<ApiResponse> {
    let result = await method(...(params as []));

    if (this.accessTokenAccepted(result)) {
      return result;
    }

    const refreshToken = this.cookies.getCookie(STORE_KEYS.appRefreshToken);
    const refreshTokenRequet: RefreshTokenRequest = { refreshToken };
    result = await this.refreshToken(refreshTokenRequet);

    if (!result.success) {
      return {
        success: false,
        errors: [
          {
            message: "common:invalidServerResponse",
            status: 401,
            pointer: null,
            header: null,
          },
        ],
      };
    }

    return await method(...(params as []));
  }
}
