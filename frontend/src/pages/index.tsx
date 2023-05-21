import { Home } from "@/components/Home";
import { NextSeo } from "next-seo";
import useTranslation from "next-translate/useTranslation";

export default function HomePage() {
  const { t } = useTranslation();
  const SEO = {
    description: t("home:pageDescription"),
  };

  return (
    <>
      <NextSeo {...SEO} />
      <Home />
    </>
  );
}
