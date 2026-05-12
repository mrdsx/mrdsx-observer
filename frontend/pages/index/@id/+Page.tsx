import { ArrowLeft } from "lucide-react";
import { useData } from "vike-react/useData";
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
    <div className="space-y-4">
      <Button
        render={
          <a href="/">
            <ArrowLeft /> Back
          </a>
        }
        variant="outline"
      />
      <h1 className="text-2xl font-semibold">{dataResult.data.projectName}</h1>
      <ul className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        {dataResult.data.services
          .sort((a, b) => a.name.localeCompare(b.name))
          .map((service) => (
            <Card className="max-w-125" key={service.name}>
              <CardHeader className="border-b">
                <CardTitle>{service.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="mb-4 flex flex-wrap justify-between gap-2">
                  <StatusBadge status={service.currentStatus} />
                  <span className="text-[16px]">Uptime: {service.uptime}%</span>
                </div>

                <DailyReports dailyReports={service.dailyReports} />
              </CardContent>
            </Card>
          ))}
      </ul>
    </div>
  );
}
