import { GetServerSidePropsContext } from "next";
import AuthClient from "@/api/clients/auth";
import { REDIRECTS } from "@/utils/constants";
import { makeInternalUrl } from "@/utils/make-external-url";

export default function LogoutPage() {
  return <></>;
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const authClient = new AuthClient(context);
  await authClient.logout();
  return {
    redirect: {
      destination: makeInternalUrl(context, REDIRECTS.redirectAfterLogout),
      permanent: false,
    },
  };
}
