import { CentredContainer } from "@/components/CentredContainer";
import { NextSeo } from "next-seo";
import getConfig from "next/config";
import useTranslation from "next-translate/useTranslation";

export default function NotFound() {
  const { publicRuntimeConfig: env } = getConfig();
  const { t } = useTranslation();
  const pageDescription = t("404:pageDescription");
  const SEO = {
    title: `${env.APP_NAME} | 404`,
    description: pageDescription,
  };

  return (
    <>
      <NextSeo {...SEO} />
      <CentredContainer>
        <h1 className="text-xl font-semibold">{pageDescription}</h1>
      </CentredContainer>
    </>
  );
}
