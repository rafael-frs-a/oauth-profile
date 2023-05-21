import { Logo } from "../icons/Logo";
import { ThemeChanger } from "../ThemeChanger";
import { LanguageSelector } from "../LanguageSelector";

export function Header() {
  return (
    <nav className="sticky top-0 z-10 flex h-16 items-center justify-between border-b border-gray-700 bg-gray-900 text-white">
      <Logo href="/" className="flex h-16 w-14 justify-center py-3.5" />
      <div className="flex h-16 items-center">
        <ThemeChanger className="flex h-16 w-12 items-center p-3" />
        <LanguageSelector className="flex h-16 items-center p-3" />
      </div>
    </nav>
  );
}
