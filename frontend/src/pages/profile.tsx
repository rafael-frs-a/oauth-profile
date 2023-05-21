import getConfig from "next/config";
import { NextSeo } from "next-seo";
import useTranslation from "next-translate/useTranslation";
import useLoginRequired from "@/hooks/login-required";
import { Profile } from "@/components/Profile";

export default function ProfilePage() {
  const { publicRuntimeConfig: env } = getConfig();
  const { t } = useTranslation();
  const SEO = {
    description: t("profile:pageDescription"),
    title: `${env.APP_NAME} | ${t("common:profile")}`,
  };

  const { authenticated } = useLoginRequired();
  return (
    <>
      <NextSeo {...SEO} />
      {authenticated && <Profile />}
    </>
  );
}
