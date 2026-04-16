import type { VercelRequest, VercelResponse } from "@vercel/node";
import { renderPage } from "vike/server";

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.url === undefined) throw new Error("req.url is undefined");

  const { httpResponse } = await renderPage({ urlOriginal: req.url });
  if (!httpResponse) return;

  res.statusCode = httpResponse.statusCode;
  httpResponse.headers.forEach(([name, value]) => {
    res.setHeader(name, value);
  });
  httpResponse.pipe(res);
}
