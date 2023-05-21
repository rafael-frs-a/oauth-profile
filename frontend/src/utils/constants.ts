import { ApiResponse } from "@/api/types";

export const STORE_KEYS = {
  loginNonce: "LOGIN_NONCE",
  appAccessToken: "APP_ACCESS_TOKEN",
  appRefreshToken: "APP_REFRESH_TOKEN",
  userProfile: "USER_PROFILE",
  auth0LogoutUrl: "AUTH0_LOGOUT_URL",
};

export const REDIRECTS = {
  redirectAfterAuthorize: "/login/callback",
  redirectAfterLogin: "/profile",
  redirectAfterLogout: "/",
  redirectAfterAuthenticationFailed: "/login",
};

export const INVALID_SERVER_RESPONSE: ApiResponse = {
  success: false,
  errors: [
    {
      message: "common:invalidServerResponse",
      status: 500,
      pointer: null,
      header: null,
    },
  ],
};
