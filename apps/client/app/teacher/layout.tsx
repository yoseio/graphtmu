import { ReactNode, Suspense } from "react";
import { Metadata } from "next"

export const metadata: Metadata = {
  title: "Search Teacher - GraphTMU",
}

export default function Layout(props: Readonly<{ children: ReactNode }>) {
  return (
    <Suspense>
      {props.children}
    </Suspense>
  )
}
