import { ExternalLink } from "lucide-react";
import { useData } from "vike-react/useData";
import { DailyReports } from "@/components/DailyReports";
import { ErrorView } from "@/components/ErrorView";
import { StatusBadge } from "@/components/StatusBadge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { STATUS_CODES } from "@/lib/constants";
import type { Data } from "./+data";

export default function HomePage() {
  const dataResult = useData<Data>();

  if (dataResult.code === STATUS_CODES.INVALID_RESPONSE) {
    return <ErrorView content="Inappropriate response from external server." />;
  }

  if (!dataResult.success) {
    return <ErrorView content="Something went wrong. Try again later." />;
  }

  return (
    <ul className="grid grid-cols-1 gap-4 sm:grid-cols-2">
      {dataResult.data.projects
        .sort((a, b) => a.name.localeCompare(b.name))
        .map((project) => (
          <Card className="max-w-125" key={project.id}>
            <CardHeader className="border-b">
              <CardTitle className="flex items-center gap-2">
                {project.name}
                <Button
                  size="icon-sm"
                  variant="ghost"
                  render={
                    <a href={`/${project.id}`}>
                      <ExternalLink />
                    </a>
                  }
                />
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="mb-4 flex flex-wrap justify-between gap-2">
                <StatusBadge status={project.currentStatus} />
                <span className="text-[16px]">Uptime: {project.uptime}%</span>
              </div>

              <DailyReports dailyReports={project.dailyReports} />
            </CardContent>
          </Card>
        ))}
    </ul>
  );
}
