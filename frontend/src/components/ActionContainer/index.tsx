import { ReactNode } from "react";
import Link from "next/link";

export interface ActionContainerProps {
  className?: string;
  children: ReactNode;
  href?: string;
  onClick?: () => void;
}

export function ActionContainer({
  className,
  children,
  href,
  onClick,
}: ActionContainerProps) {
  if (href) {
    return (
      <Link href={href} className={className}>
        {children}
      </Link>
    );
  }

  return (
    <button onClick={onClick} className={className}>
      {children}
    </button>
  );
}
