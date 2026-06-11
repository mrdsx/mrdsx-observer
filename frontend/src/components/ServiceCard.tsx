import type { Service } from "@/lib/schemas";
import { DailyReports } from "./DailyReports";
import { StatusBadge } from "./StatusBadge";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";

export function ServiceCard(props: { service: Service }) {
  const service = props.service;

  return (
    <Card class="max-w-125">
      <CardHeader class="border-b">
        <CardTitle>{service.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="mb-4 flex flex-wrap justify-between gap-2">
          <StatusBadge status={service.currentStatus} />
          <span class="text-[16px]">Uptime: {service.uptime}%</span>
        </div>

        <DailyReports dailyReports={service.dailyReports} />
      </CardContent>
    </Card>
  );
}
