"use client";

import { ExclamationCircleOutlined, LoadingOutlined } from "@ant-design/icons";
import { useQuery } from "@tanstack/react-query";
import { Button, Card } from "antd";
import { ProjectReportsView } from "@/components/ProjectReportsView";
import { StatusBadge } from "@/components/StatusAlert";
import { apiFetch } from "@/lib/api";
import { projectsReportsSchema } from "@/lib/schemas";

export default function Home() {
  const {
    data: projectsData,
    isPending,
    isError,
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

  if (isError) {
    return (
      <div className="rounded-lg flex flex-col gap-4 items-center py-20 text-red-600 dark:text-red-400">
        <div className="inline-flex gap-2">
          <ExclamationCircleOutlined className="text-xl" />
          <p className="text">Something went wrong while fetching data</p>
        </div>
        <Button onClick={() => refetch()}>Retry</Button>
      </div>
    );
  }

  return (
    <ul className="grid gap-2 grid-cols-1 sm:grid-cols-2">
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
            <div className="flex flex-wrap gap-2 justify-between mb-4">
              <StatusBadge status={project.status} />
              <span className="text-[16px]">Uptime: {project.uptime}%</span>
            </div>
            <ProjectReportsView project={project} />
          </Card>
        ))}
    </ul>
  );
}
