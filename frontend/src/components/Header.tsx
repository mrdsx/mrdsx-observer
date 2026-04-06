"use client";

import { theme } from "antd";
import { ToggleThemeButton } from "@/components/ToggleThemeButton";

export function Header() {
  const { token } = theme.useToken();

  return (
    <header
      className="py-4 px-8 border-b flex items-center justify-between w-full"
      style={{ borderColor: token.colorBorder }}
    >
      <h1 className="text-xl">mrdsx observer</h1>
      <ToggleThemeButton />
    </header>
  );
}
