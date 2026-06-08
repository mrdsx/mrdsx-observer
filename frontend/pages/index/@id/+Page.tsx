import { ArrowLeftIcon } from "lucide-solid";
import { For } from "solid-js";
import { useData } from "vike-solid/useData";
import { DailyReports } from "@/components/DailyReports";
import { ErrorView } from "@/components/ErrorView";
import { StatusBadge } from "@/components/StatusBadge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { STATUS_CODES } from "@/lib/constants";
import type { Data } from "./+data";

export default function ServicesReportsPage() {
  const dataResult = useData<Data>();

  if (dataResult.code === STATUS_CODES.NOT_FOUND) {
    return <ErrorView content="Project not found." />;
  }

  if (dataResult.code === STATUS_CODES.INVALID_RESPONSE) {
    return <ErrorView content="Inappropriate response from external server." />;
  }

  if (!dataResult.success) {
    return <ErrorView content="Something went wrong. Try again later." />;
  }

  return (
    <div class="space-y-4">
      <Button as="a" href="/" variant="outline">
        <ArrowLeftIcon />
        Back
      </Button>
      <h1 class="text-2xl font-semibold">{dataResult.data.projectName}</h1>
      <ul class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <For each={dataResult.data.services}>
          {(service) => (
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
          )}
        </For>
      </ul>
    </div>
  );
}
