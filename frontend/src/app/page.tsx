"use client";

import { LoadingOutlined } from "@ant-design/icons";
import { useQuery } from "@tanstack/react-query";
import { Card } from "antd";
import { ZodError } from "zod";
import { ProjectReportsView } from "@/components/ProjectReportsView";
import { StatusBadge } from "@/components/StatusAlert";
import { apiFetch } from "@/lib/api";
import { projectsReportsSchema } from "@/lib/schemas";
import { ErrorView } from "../components/ErrorView";

export default function Home() {
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
    return <LoadingOutlined className="self-center py-10 text-3xl" />;
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
    <ul className="grid grid-cols-1 gap-2 sm:grid-cols-2">
      {projectsData.projects
        .sort((a, b) => a.name.localeCompare(b.name))
        .map((project) => (
          <Card
            className="max-w-125 flex-wrap"
            title={
              <div className="inline-flex items-center gap-4">
                <span>{project.name}</span>
              </div>
            }
            size="small"
            key={project.id}
          >
            <div className="mb-4 flex flex-wrap justify-between gap-2">
              <StatusBadge status={project.currentStatus} />
              <span className="text-[16px]">Uptime: {project.uptime}%</span>
            </div>
            <ProjectReportsView project={project} />
          </Card>
        ))}
    </ul>
  );
}
