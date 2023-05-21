import {
  ActionContainer,
  ActionContainerProps,
} from "@/components/ActionContainer";

export interface MoonProps extends Omit<ActionContainerProps, "children"> {}

export function Moon({ className, href, onClick, ...props }: MoonProps) {
  return (
    <ActionContainer onClick={onClick} href={href} className={className}>
      <svg
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 448 448.045"
        {...props}
      >
        <g>
          <path
            d="M224.023 448.031c85.715.903 164.012-48.488 200.118-126.23a171.044 171.044 0 0 1-72.118 14.23c-97.156-.11-175.89-78.844-176-176 .973-65.719 37.235-125.832 94.91-157.351A334.474 334.474 0 0 0 224.024.03c-123.714 0-224 100.29-224 224 0 123.715 100.286 224 224 224zm0 0"
            fill="#ffffff"
            data-original="#000000"
          ></path>
        </g>
      </svg>
    </ActionContainer>
  );
}
