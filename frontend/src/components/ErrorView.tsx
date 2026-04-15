import { AlertCircleIcon } from "lucide-react";
import { Button } from "./ui/button";

type ErrorViewProps = {
  content: string;
  refetch: () => void;
};

export function ErrorView({ content, refetch }: ErrorViewProps) {
  return (
    <div className="flex flex-col items-center gap-4 rounded-lg py-20 text-red-600 dark:text-red-400">
      <div className="flex gap-2">
        <AlertCircleIcon className="text-xl" />
        <p>{content}</p>
      </div>
      <Button onClick={refetch}>Retry</Button>
    </div>
  );
}
