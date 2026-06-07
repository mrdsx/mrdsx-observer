import { CircleAlertIcon } from "lucide-solid";

export function ErrorView(props: { content: string }) {
  return (
    <div class="flex self-center gap-2 rounded-lg py-20 text-red-600 dark:text-red-400">
      <CircleAlertIcon class="text-xl" />
      <p>{props.content}</p>
    </div>
  );
}
