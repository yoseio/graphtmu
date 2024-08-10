import { ReactNode, Suspense } from "react";

export default function Layout(props: Readonly<{ children: ReactNode }>) {
  return (
    <Suspense>
      {props.children}
    </Suspense>
  )
}
