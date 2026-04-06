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
          <main className="max-w-300 px-4 w-full py-8 flex flex-col">
            {children}
          </main>
        </Body>
      </AppProvider>
    </html>
  );
}
