import { useState, useEffect } from "react";
import AuthClient from "@/api/clients/auth";
import { useRouter } from "next/router";
import { REDIRECTS } from "@/utils/constants";
import useRenderingState, { RenderingState } from "./rendering-state";

interface LoginRequiredHook {
  authenticated: boolean;
}

export default function useLoginRequired(): LoginRequiredHook {
  const { state } = useRenderingState();
  const [authenticated, setAuthenticated] = useState<boolean>(false);
  const authClient = new AuthClient();
  const { push } = useRouter();

  const checkAuthenticated = async () => {
    const authenticated = await authClient.isLoggedIn();
    setAuthenticated(authenticated);

    if (!authenticated) {
      push(REDIRECTS.redirectAfterAuthenticationFailed);
    }
  };

  useEffect(() => {
    if (state === RenderingState.READY) {
      checkAuthenticated();
    }
  }, [state]);

  return { authenticated };
}
