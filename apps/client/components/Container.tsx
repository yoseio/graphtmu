import { forwardRef, HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

export interface ContainerProps extends HTMLAttributes<HTMLDivElement> {}

const Container = forwardRef<HTMLDivElement, ContainerProps>(
  ({ className, ...props }, ref) => {
    return (
      <div
        className={cn("max-w-3xl w-full mx-auto px-4", className)}
        ref={ref}
        {...props}
      />
    );
  },
);
Container.displayName = "Container";

export { Container };
