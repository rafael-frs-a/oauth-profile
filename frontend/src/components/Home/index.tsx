import { useRouter } from "next/router";
import { useState, useEffect } from "react";
import { NavList, NavListAction } from "../NavList";
import useTranslation from "next-translate/useTranslation";
import useRenderingState, { RenderingState } from "@/hooks/rendering-state";
import AuthClient from "@/api/clients/auth";

export function Home() {
  const [actions, setActions] = useState<NavListAction[]>([]);
  const { t } = useTranslation();
  const authClient = new AuthClient();
  const { state } = useRenderingState();
  const { locale } = useRouter();

  const loadActions = async () => {
    const authenticated = await authClient.isLoggedIn();

    if (authenticated) {
      setActions([
        {
          href: "/profile",
          label: t("common:profile"),
        },
      ]);
    } else {
      setActions([
        {
          href: "/login",
          label: t("common:login"),
        },
      ]);
    }
  };

  useEffect(() => {
    if (state != RenderingState.IDLE) {
      loadActions();
    }
  }, [state, locale]);

  return (
    <div className="mt-10 flex justify-center">
      <NavList actions={actions} />
    </div>
  );
}
