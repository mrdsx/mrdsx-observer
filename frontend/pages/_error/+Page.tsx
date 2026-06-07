import { usePageContext } from "vike-solid/usePageContext";

export default function Page() {
  const { is404 } = usePageContext();

  if (is404) {
    return (
      <>
        <h1>Error 404</h1>
        <p>Page does not exist.</p>
      </>
    );
  }

  return (
    <>
      <h1>Internal Error</h1>
      <p>Something went wrong.</p>
    </>
  );
}
