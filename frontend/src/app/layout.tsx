import type { Metadata } from "next";
import { AppProvider } from "@/components/AppProvider";
import "./globals.css";
import { Body } from "@/components/Body";
import { ToggleThemeButton } from "@/components/ToggleThemeButton";

export const metadata: Metadata = {
  title: "mrdsx observer",
};

export default function RootLayout({ children }: React.PropsWithChildren) {
  return (
    <html lang="en" className="h-full">
      <AppProvider>
        <Body>
          <header className="py-4 px-8 border-b flex  items-center justify-between">
            <h1 className="text-xl">mrdsx observer</h1>
            <ToggleThemeButton />
          </header>
          <main className="px-16 py-8 flex flex-col">{children}</main>
        </Body>
      </AppProvider>
    </html>
  );
}
