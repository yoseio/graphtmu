import { forwardRef, HTMLAttributes } from "react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

const Logo = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => {
    return (
      <Avatar className={className} ref={ref} {...props}>
        <AvatarImage src="https://github.com/BrainoidHQ.png" alt="Brainoid" />
        <AvatarFallback>B</AvatarFallback>
      </Avatar>
    )
  }
)
Logo.displayName = "Logo"

export { Logo }
