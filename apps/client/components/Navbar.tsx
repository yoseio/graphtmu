import { ReactNode } from "react";
import Link from "next/link";

import { Container } from "@/components/Container";
import { Logo } from "@/components/Logo";

export interface NavbarProps {
  links: { contents: ReactNode; url: string }[];
}

export function Navbar(props: NavbarProps) {
  return (
    <header className="border-b">
      <Container className="h-14 flex items-center">
        <Link href="/" className="flex items-center justify-center">
          <Logo className="h-6 w-6" />
          <span className="sr-only">Brainoid</span>
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6">
          {props.links.map((link) => (
            <Link
              key={link.url}
              href={link.url}
              className="text-sm font-medium hover:underline underline-offset-4"
            >
              {link.contents}
            </Link>
          ))}
        </nav>
      </Container>
    </header>
  );
}
