import { useRouter } from "next/router";
import { Menu } from "@headlessui/react";
import Link from "next/link";
import Image from "next/image";
import useTranslation from "next-translate/useTranslation";

export interface LanguageSelectorProps {
  className?: string;
}

export function LanguageSelector({ className }: LanguageSelectorProps) {
  const { asPath, locale: currentLocale, locales } = useRouter();
  const { t } = useTranslation();

  if (locales?.length === 0) return null;

  return (
    <Menu>
      <Menu.Button className={className}>
        <Image
          src={`/img/flags/${currentLocale}.png`}
          alt={t(`common:${currentLocale}`)}
          width={32}
          height={32}
        />
      </Menu.Button>
      <Menu.Items className="absolute top-[56px] right-0 mt-2 origin-top-right bg-gray-900">
        {locales!.map((locale, idx) => {
          const language = t(`common:${locale}`);
          const flagIcon = `/img/flags/${locale}.png`;

          return (
            <Menu.Item key={idx} as="div" className="p-2 hover:bg-gray-700">
              {({ close }) => (
                <Link
                  href={asPath}
                  locale={locale}
                  onClick={close}
                  className="flex space-x-2"
                >
                  <Image src={flagIcon} alt="-" width={32} height={32} />
                  <h1>{language}</h1>
                </Link>
              )}
            </Menu.Item>
          );
        })}
      </Menu.Items>
    </Menu>
  );
}
