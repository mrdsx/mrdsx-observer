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
    <html lang="en">
      <AppProvider>
        <Body>
          <header className="py-4 px-8 border-gray-200 border-b flex items-center justify-between w-full">
            <h1 className="text-xl">mrdsx observer</h1>
            <ToggleThemeButton />
          </header>
          <main className="max-w-300 px-4 w-full py-8 flex flex-col">
            {children}
          </main>
        </Body>
      </AppProvider>
    </html>
  );
}
