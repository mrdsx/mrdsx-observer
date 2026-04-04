import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "mrdsx observer",
};

export default function RootLayout({ children }: React.PropsWithChildren) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
