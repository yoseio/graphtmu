import { ReactNode } from "react"
import { Manrope } from "next/font/google"

import { Navbar } from "@/components/Navbar"
import { Container } from "@/components/Container"
import { GitHubIcon } from "@/components/GitHubIcon"
import { cn } from "@/lib/utils"

import "./globals.css"

const fontHeading = Manrope({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-heading",
})

const fontBody = Manrope({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-body",
})

const links = [
  { contents: "Syllabus", url: "/syllabus" },
  { contents: "Teacher", url: "/teacher" },
  { contents: <GitHubIcon />, url: "https://github.com/yoseio/graphtmu" }
]

export default function Layout(props: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="en">
      <body
        className={cn(
          "antialiased",
          fontHeading.variable,
          fontBody.variable
        )}
      >
        <div className="flex flex-col min-h-screen">
          <Navbar links={links} />
          <main>
            <Container className="py-8">
              {props.children}
            </Container>
          </main>
        </div>
      </body>
    </html>
  );
}
