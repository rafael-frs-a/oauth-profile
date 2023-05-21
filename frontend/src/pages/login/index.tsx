import { GetServerSidePropsContext } from "next";
import getConfig from "next/config";
import { Login } from "@/components/Login";
import { NextSeo } from "next-seo";
import useTranslation from "next-translate/useTranslation";
import { displayServerError } from "@/utils/display-error-message";
import { useEffect } from "react";
import AuthClient from "@/api/clients/auth";
import { AuthorizeRequest } from "@/api/clients/auth/types";
import useRenderingState, { RenderingState } from "@/hooks/rendering-state";
import { REDIRECTS, STORE_KEYS } from "@/utils/constants";
import Cookies from "@/utils/cookies";
import { makeExternalUrl, makeInternalUrl } from "@/utils/make-external-url";
import { ApiError } from "@/api/types";

export interface LoginPageProps {
  serverErrors?: ApiError[];
}

export default function LoginPage({ serverErrors }: LoginPageProps) {
  const { state } = useRenderingState();
  const { publicRuntimeConfig: env } = getConfig();
  const { t } = useTranslation();
  const SEO = {
    description: t("login:pageDescription"),
    title: `${env.APP_NAME} | ${t("common:login")}`,
  };

  useEffect(() => {
    if (state === RenderingState.READY && serverErrors) {
      displayServerError(t, serverErrors);
    }
  }, [state]);

  return (
    <>
      <NextSeo {...SEO} />
      <Login />
    </>
  );
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const authClient = new AuthClient(context);
  const cookies = new Cookies(context);

  if (await authClient.isLoggedIn()) {
    return {
      redirect: {
        destination: makeInternalUrl(context, REDIRECTS.redirectAfterLogin),
        permanent: false,
      },
    };
  }

  const authorizeRequest: AuthorizeRequest = {
    callbackUrl: makeExternalUrl(context, REDIRECTS.redirectAfterAuthorize),
    redirectAfterLogoutUrl: makeExternalUrl(
      context,
      REDIRECTS.redirectAfterLogin
    ),
  };

  const result = await authClient.authorize(authorizeRequest);

  if (result.success) {
    cookies.setCookie(STORE_KEYS.auth0LogoutUrl, result.data!.logoutUrl);
    return {
      redirect: {
        destination: result.data!.authorizationUrl,
        permanent: false,
      },
    };
  }

  return {
    props: {
      serverErrors: result.errors,
    },
  };
}
