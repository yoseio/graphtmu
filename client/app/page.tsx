"use client";

import { callMenuSuggestionFlow } from "@/app/genkit";
import { useState } from "react";

export default function Home() {
  const [menuItem, setMenu] = useState<string>("");

  async function getMenuItem(formData: FormData) {
    const theme = formData.get("theme")?.toString() ?? "";
    const suggestion = await callMenuSuggestionFlow(theme);
    setMenu(suggestion);
  }

  return (
    <main>
      <form action={getMenuItem}>
        <label>
          Suggest a menu item for a restaurant with this theme:{" "}
        </label>
        <input type="text" name="theme" />
        <button type="submit">Generate</button>
      </form>
      <br />
      <pre>{menuItem}</pre>
    </main>
  );
}
