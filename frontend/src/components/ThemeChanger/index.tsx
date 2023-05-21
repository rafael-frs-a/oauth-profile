import { useState, useEffect } from "react";
import { Sun } from "../icons/Sun";
import { Moon } from "../icons/Moon";
import useThemeManager from "@/hooks/theme-manager";

export interface ThemeChangerProps {
  className?: string;
}

export function ThemeChanger({ className }: ThemeChangerProps) {
  const { isDarkMode, setTheme } = useThemeManager();
  const [mounted, setMounted] = useState<boolean>(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  const changeTheme = () => setTheme(isDarkMode ? "light" : "dark");

  if (isDarkMode) {
    return <Sun onClick={changeTheme} className={className} />;
  }

  return <Moon onClick={changeTheme} className={className} />;
}
