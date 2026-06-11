import { CircleAlertIcon } from "lucide-solid";
import { NOT_FOUND, type NotFoundError } from "@/lib/errors";
import { NotFoundView } from "./NotFoundView";
import { Button } from "./ui/button";

type ErrorViewProps = {
  error: unknown;
  reset: () => void;
};

export function ErrorView(props: ErrorViewProps) {
  if ((props.error as NotFoundError).code === NOT_FOUND) {
    return <NotFoundView />;
  }

  return (
    <div class="self-center py-20 flex flex-col gap-8 items-center">
      <span class="flex self-center gap-2 rounded-lg text-red-600 dark:text-red-400">
        <CircleAlertIcon class="text-xl" />
        <p>{(props.error as Error)?.message ?? "Internal server error."}</p>
      </span>
      <Button onClick={props.reset} variant="outline">
        Try again
      </Button>
    </div>
  );
}
