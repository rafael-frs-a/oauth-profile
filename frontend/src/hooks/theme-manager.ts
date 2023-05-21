import { useTheme } from "next-themes";

interface ThemeManagerHook {
  isDarkMode: boolean;
  theme: string;
  setTheme: (theme: string) => void;
}

export default function useThemeManager(): ThemeManagerHook {
  const { systemTheme, theme, setTheme } = useTheme();
  const currentTheme = theme === "system" ? systemTheme : theme;
  const isDarkMode = currentTheme === "dark";
  return { isDarkMode, theme: currentTheme as string, setTheme };
}
