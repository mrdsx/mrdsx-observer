import { ToggleThemeButton } from "./ToggleThemeButton";

export function Header() {
  return (
    <header class="flex w-full items-center justify-between border-b px-8 py-4">
      <h1 class="text-xl">
        <a href="/">mrdsx observer</a>
      </h1>
      <ToggleThemeButton />
    </header>
  );
}
