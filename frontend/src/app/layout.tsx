import type { Metadata } from "next";
import { AppProvider } from "@/components/AppProvider";
import "./globals.css";
import { Body } from "@/components/Body";
import { Header } from "@/components/Header";

export const metadata: Metadata = {
  title: "mrdsx observer",
};

export default function RootLayout({ children }: React.PropsWithChildren) {
  return (
    <html lang="en">
      <AppProvider>
        <Body>
          <Header />
          <main className="flex w-full max-w-300 flex-col px-4 py-8">
            {children}
          </main>
        </Body>
      </AppProvider>
    </html>
  );
}
