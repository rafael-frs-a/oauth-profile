import { GetServerSidePropsContext } from "next";

export function makeInternalUrl(
  { locale, defaultLocale }: GetServerSidePropsContext,
  path: string
): string {
  const pathLocale = !locale || locale === defaultLocale ? "" : `/${locale}`;
  return `${pathLocale}${path}`;
}

export function makeExternalUrl(
  context: GetServerSidePropsContext,
  path: string
): string {
  const protocol = context.req.headers["x-forwarded-proto"] || "http";
  const host = context.req.headers.host;
  const internalUrl = makeInternalUrl(context, path);
  return `${protocol}://${host}${internalUrl}`;
}
