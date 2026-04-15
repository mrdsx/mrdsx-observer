import "../globals.css";
import { Body } from "../components/Body";
import { Header } from "../components/Header";

export default function RootLayout({ children }: React.PropsWithChildren) {
  return (
    <Body>
      <Header />
      <main className="flex w-full max-w-300 flex-col px-4 py-8">
        {children}
      </main>
    </Body>
  );
}
