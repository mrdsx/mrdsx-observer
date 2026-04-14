import type { Project } from "../lib/schemas";
import { Badge } from "./ui/badge";

type StatusBadgeProps = {
  status: Project["currentStatus"];
};

export function StatusBadge({ status }: StatusBadgeProps) {
  if (status === "outage") {
    return <Badge variant="destructive">Outage</Badge>;
  }

  if (status === "degraded") {
    return <Badge variant="warning">Degraded</Badge>;
  }

  return <Badge variant="success">Operational</Badge>;
}
