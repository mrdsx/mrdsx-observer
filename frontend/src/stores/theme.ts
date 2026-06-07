import { createSignal } from "solid-js";

const LOCAL_STORAGE_KEY = "darkMode";

const [isDarkMode, setIsDarkMode] = createSignal(false);

function initTheme(): void {
  const stored = localStorage.getItem(LOCAL_STORAGE_KEY);
  setIsDarkMode(stored === "true");
}

function toggleTheme(): void {
  const nextTheme = !isDarkMode();
  setIsDarkMode(nextTheme);
  localStorage.setItem(LOCAL_STORAGE_KEY, String(nextTheme));
}

export { initTheme, isDarkMode, toggleTheme };
