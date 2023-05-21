import { useEffect } from "react";
import { NavList, NavListAction } from "../NavList";
import useTranslation from "next-translate/useTranslation";
import { displayServerError } from "@/utils/display-error-message";
import { JSONTree } from "react-json-tree";
import useThemeManager from "@/hooks/theme-manager";
import useFetchUserProfile from "@/hooks/user-profile";

export function Profile() {
  const { isDarkMode } = useThemeManager();
  const { t } = useTranslation();
  const { data: userProfile, error } = useFetchUserProfile();
  const actions: NavListAction[] = [
    {
      href: "/",
      label: t("common:home"),
    },
    {
      href: "/logout",
      label: t("common:logout"),
      className:
        "bg-red-500 border-red-800 hover:bg-red-600 text-white dark:border-red-800 dark:hover:bg-red-600",
    },
  ];

  useEffect(() => {
    if (error) {
      displayServerError(t, error.errors);
    }
  }, [error]);

  return (
    <div className="mt-4 flex flex-col items-center space-y-2">
      <div className="w-1/2 min-w-fit max-w-lg">
        <h1>{t("profile:profileData")}</h1>
        <JSONTree
          data={userProfile}
          theme={{
            extend: "ocean",
            tree: {
              padding: "0.5rem",
            },
          }}
          shouldExpandNodeInitially={() => true}
          invertTheme={!isDarkMode}
        />
      </div>
      <NavList actions={actions} />
    </div>
  );
}
