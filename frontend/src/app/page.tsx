"use client";

import { ExclamationCircleOutlined, LoadingOutlined } from "@ant-design/icons";
import { useQuery } from "@tanstack/react-query";
import { Button, Card } from "antd";
import { ReportItem } from "@/components/ReportItem";
import { StatusBadge } from "@/components/StatusAlert";
import { apiFetch } from "@/lib/api";
import { projectsSchema } from "@/lib/schemas";

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
      const parsedData = projectsSchema.parse(data);

      return parsedData;
    },
    retry: false,
  });

  if (isPending) {
    return (
      <div className="flex justify-center py-30 text-3xl">
        <LoadingOutlined />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="rounded-lg flex flex-col gap-4 items-center py-30 text-red-600">
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
            <div className="flex flex-wrap gap-0.5">
              {Array(30 - project.dailyReports.length)
                .fill(null)
                .map((_, index) => {
                  // we're ok with index as key because list is static
                  // biome-ignore lint/suspicious/noArrayIndexKey: .
                  return <ReportItem key={index} />;
                })}
              {project.dailyReports.map((report) => {
                return (
                  <ReportItem
                    date={report.date}
                    worstStatus={report.worstStatus}
                    uptime={report.uptime}
                    key={report.date}
                  />
                );
              })}
            </div>
          </Card>
        ))}
    </ul>
  );
}
