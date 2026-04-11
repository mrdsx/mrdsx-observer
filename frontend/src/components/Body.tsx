"use client";

import { theme } from "antd";

export function Body({ children }: React.PropsWithChildren) {
  const { token } = theme.useToken();

  return (
    <body
      className="flex min-h-screen flex-col items-center"
      style={{
        background: token.colorBgContainer,
        color: token.colorText,
      }}
    >
      {children}
    </body>
  );
}
