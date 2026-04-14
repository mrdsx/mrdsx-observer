import type { Metadata } from "next";
import { Geist } from "next/font/google";
import { AppProvider } from "@/components/AppProvider";
import { Body } from "@/components/Body";
import { Header } from "@/components/Header";
import { cn } from "@/lib/utils";
import "./globals.css";

const geist = Geist({ subsets: ["latin"], variable: "--font-sans" });

export const metadata: Metadata = {
  title: "mrdsx observer",
};

export default function RootLayout({ children }: React.PropsWithChildren) {
  return (
    <html lang="en" className={cn("font-sans", geist.variable)}>
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
