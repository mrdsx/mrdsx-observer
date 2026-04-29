import { AlertCircleIcon } from "lucide-react";

type ErrorViewProps = {
  content: string;
};

export function ErrorView({ content }: ErrorViewProps) {
  return (
    <div className="flex self-center gap-2 rounded-lg py-20 text-red-600 dark:text-red-400">
      <AlertCircleIcon className="text-xl" />
      <p>{content}</p>
    </div>
  );
}
