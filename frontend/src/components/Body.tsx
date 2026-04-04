"use client";

import { theme } from "antd";

export function Body({ children }: React.PropsWithChildren) {
  const { token } = theme.useToken();

  return (
    <body
      className="min-h-full flex flex-col"
      style={{ background: token.colorBgContainer, color: token.colorText }}
    >
      {children}
    </body>
  );
}
