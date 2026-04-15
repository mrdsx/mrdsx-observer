import { useQuery } from "@tanstack/react-query";
import { LoaderCircleIcon } from "lucide-react";
import { ZodError } from "zod";
import { ErrorView } from "../components/ErrorView";
import { ProjectReports } from "../components/ProjectReports";
import { StatusBadge } from "../components/StatusBadge";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../components/ui/card";
import { apiFetch } from "../lib/api";
import { projectsReportsSchema } from "../lib/schemas";

export default function HomePage() {
  const {
    data: projectsData,
    isPending,
    isError,
    error,
    refetch,
  } = useQuery({
    queryKey: ["projects"],
    queryFn: async () => {
      const response = await apiFetch("/api/projects");
      const data = await response.json();
      const parsedData = projectsReportsSchema.parse(data);

      return parsedData;
    },
    retry: false,
    refetchOnWindowFocus: false,
  });

  if (isPending) {
    return <LoaderCircleIcon className="animate-spin self-center" />;
  }

  if (error instanceof ZodError) {
    return (
      <ErrorView
        content="Inappropriate response from server"
        refetch={refetch}
      />
    );
  }

  if (isError) {
    return (
      <ErrorView
        content="Something went wrong while fetching data"
        refetch={refetch}
      />
    );
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

              <ProjectReports project={project} />
            </CardContent>
          </Card>
        ))}
    </ul>
  );
}
