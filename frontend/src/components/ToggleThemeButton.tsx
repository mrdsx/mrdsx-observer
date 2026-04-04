"use client";

import { MoonOutlined, SunOutlined } from "@ant-design/icons";
import { Button } from "antd";
import { useThemeStore } from "@/stores/themeStore";

export function ToggleThemeButton() {
  const isDarkMode = useThemeStore((state) => state.isDarkMode);
  const toggleTheme = useThemeStore((state) => state.toggleTheme);

  return (
    <Button
      icon={isDarkMode ? <SunOutlined /> : <MoonOutlined />}
      onClick={toggleTheme}
    />
  );
}
