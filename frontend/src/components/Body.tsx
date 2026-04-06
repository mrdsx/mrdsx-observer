"use client";

import { theme } from "antd";

export function Body({ children }: React.PropsWithChildren) {
  const { token } = theme.useToken();

  return (
    <body
      className="min-h-screen flex flex-col items-center"
      style={{
        background: token.colorBgContainer,
        color: token.colorText,
      }}
    >
      {children}
    </body>
  );
}
