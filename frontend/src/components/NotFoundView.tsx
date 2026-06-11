import { Title } from "@solidjs/meta";
import { HttpStatusCode } from "@solidjs/start";
import { Button } from "@/components/ui/button";

export function NotFoundView() {
  return (
    <div class="self-center py-20 flex flex-col items-center gap-8">
      <Title>Not Found</Title>
      <HttpStatusCode code={404} />
      <span class="flex flex-col gap-2 items-center">
        <p class="font-semibold text-xl">404</p>
        <h1 class="text-xl">Page Not Found</h1>
      </span>
      <Button as="a" href="/" variant="outline">
        Go Home
      </Button>
    </div>
  );
}
