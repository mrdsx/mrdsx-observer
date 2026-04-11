"use client";

import { theme } from "antd";
import { ToggleThemeButton } from "@/components/ToggleThemeButton";

export function Header() {
  const { token } = theme.useToken();

  return (
    <header
      className="flex w-full items-center justify-between border-b px-8 py-4"
      style={{ borderColor: token.colorBorder }}
    >
      <h1 className="text-xl">mrdsx observer</h1>
      <ToggleThemeButton />
    </header>
  );
}
