import { GetServerSidePropsContext } from "next";
import AuthClient from "@/api/clients/auth";
import { LoginRequest } from "@/api/clients/auth/types";
import { REDIRECTS, STORE_KEYS } from "@/utils/constants";
import Cookies from "@/utils/cookies";
import { makeExternalUrl, makeInternalUrl } from "@/utils/make-external-url";

export default function CallbackPage() {
  return <></>;
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const authClient = new AuthClient(context);
  const { query } = context;
  const cookies = new Cookies(context);

  if (await authClient.isLoggedIn()) {
    return {
      redirect: {
        destination: makeInternalUrl(context, REDIRECTS.redirectAfterLogin),
        permanent: false,
      },
    };
  }

  const loginRequest: LoginRequest = {
    code: query.code as string,
    callbackUrl: makeExternalUrl(context, REDIRECTS.redirectAfterAuthorize),
    nonce: "",
  };

  await authClient.login(loginRequest);
  // Force logout on Auth0, should redirect back to profile page
  let redirectUrl = cookies.getCookie(STORE_KEYS.auth0LogoutUrl);

  if (redirectUrl) {
    cookies.deleteCookie(STORE_KEYS.auth0LogoutUrl);
  } else {
    redirectUrl = makeInternalUrl(context, REDIRECTS.redirectAfterLogout);
  }

  return {
    redirect: {
      destination: redirectUrl,
      permanent: false,
    },
  };
}
