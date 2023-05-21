import {
  ActionContainer,
  ActionContainerProps,
} from "@/components/ActionContainer";

export interface NavListAction extends Omit<ActionContainerProps, "children"> {
  label: string;
}

export interface NavListProps {
  actions: NavListAction[];
  className?: string;
}

export function NavList({ actions, className }: NavListProps) {
  return (
    <div
      className={`flex w-1/2 min-w-fit max-w-xs flex-col justify-center space-y-2 p-4 ${
        className || ""
      }`}
    >
      {actions?.map((action, idx) => {
        const { href, onClick, label, className } = action;

        return (
          <ActionContainer
            key={idx}
            href={href}
            onClick={onClick}
            className={`flex h-10 items-center justify-center rounded-md border-2 border-gray-400 hover:bg-gray-400 hover:text-white dark:border-gray-900 dark:hover:bg-gray-900 ${
              className || ""
            }`}
          >
            {label}
          </ActionContainer>
        );
      })}
    </div>
  );
}
