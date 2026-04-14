"use client";

import { ToggleThemeButton } from "./ToggleThemeButton";

export function Header() {
  return (
    <header className="flex w-full items-center justify-between border-b px-8 py-4">
      <h1 className="text-xl">mrdsx observer</h1>
      <ToggleThemeButton />
    </header>
  );
}
