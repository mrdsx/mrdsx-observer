import { useData } from "vike-react/useData";
import { ProjectReports } from "@/components/ProjectReports";
import { StatusBadge } from "@/components/StatusBadge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ErrorView } from "../../src/components/ErrorView";
import type { Data } from "./+data";

export default function HomePage() {
  const { data: projectsData, success, code } = useData<Data>();

  if (code === "INVALID_RESPONSE") {
    return <ErrorView content="Inappropriate response from server" />;
  }

  if (!success || projectsData === undefined) {
    return <ErrorView content="Something went wrong while fetching data" />;
  }

  return (
    <ul className="grid grid-cols-1 gap-4 sm:grid-cols-2">
      {projectsData.projects
        .sort((a, b) => a.name.localeCompare(b.name))
        .map((project) => (
          <Card className="max-w-125" key={project.id}>
            <CardHeader className="border-b">
              <CardTitle>{project.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="mb-4 flex flex-wrap justify-between gap-2">
                <StatusBadge status={project.currentStatus} />
                <span className="text-[16px]">Uptime: {project.uptime}%</span>
              </div>

              <ProjectReports dailyReports={project.dailyReports} />
            </CardContent>
          </Card>
        ))}
    </ul>
  );
}
