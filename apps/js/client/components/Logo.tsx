import { forwardRef, ElementRef, ComponentPropsWithoutRef } from "react";
import { Root } from "@radix-ui/react-avatar";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

const Logo = forwardRef<
  ElementRef<typeof Root>,
  ComponentPropsWithoutRef<typeof Root>
>(({ className, ...props }, ref) => {
  return (
    <Avatar className={className} ref={ref} {...props}>
      <AvatarImage src="https://github.com/BrainoidHQ.png" alt="Brainoid" />
      <AvatarFallback>B</AvatarFallback>
    </Avatar>
  );
});
Logo.displayName = "Logo";

export { Logo };
