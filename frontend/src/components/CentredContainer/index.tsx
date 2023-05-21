import { ReactNode } from "react";

export interface CentredContainerProps {
  children: ReactNode;
}

export function CentredContainer({ children }: CentredContainerProps) {
  return (
    <div className="flex grow items-center justify-center">{children}</div>
  );
}
