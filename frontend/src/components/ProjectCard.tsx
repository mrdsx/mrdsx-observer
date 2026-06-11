import { ExternalLinkIcon } from "lucide-solid";
import { Button } from "@/components/ui/button";
import type { Project } from "@/lib/schemas";
import { DailyReports } from "./DailyReports";
import { StatusBadge } from "./StatusBadge";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";

export function ProjectCard(props: { project: Project }) {
  const project = props.project;

  return (
    <Card class="max-w-125">
      <CardHeader class="border-b">
        <CardTitle class="flex items-center gap-2">
          {project.name}
          <Button size="icon-sm" variant="ghost" as="a" href={`/${project.id}`}>
            <ExternalLinkIcon />
          </Button>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div class="mb-4 flex flex-wrap justify-between gap-2">
          <StatusBadge status={project.currentStatus} />
          <span class="text-[16px]">Uptime: {project.uptime}%</span>
        </div>

        <DailyReports dailyReports={project.dailyReports} />
      </CardContent>
    </Card>
  );
}
