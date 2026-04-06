import { Alert } from "antd";

export function StatusBadge({ status }: { status: string }) {
  if (status === "outage") {
    return <Alert title="Outage" type="error" />;
  }

  if (status === "degraded") {
    return <Alert title="Degraded" type="warning" />;
  }

  return <Alert title="Operational" type="success" />;
}
