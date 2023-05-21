import { NavList, NavListAction } from "../NavList";
import useTranslation from "next-translate/useTranslation";

export function Login() {
  const { t } = useTranslation();
  const actions: NavListAction[] = [
    {
      href: "/",
      label: t("common:home"),
    },
  ];

  return (
    <div className="mt-10 flex justify-center">
      <NavList actions={actions} />
    </div>
  );
}
