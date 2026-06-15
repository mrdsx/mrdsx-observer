import { createAsync } from "@solidjs/router";
import { ErrorBoundary, For } from "solid-js";
import { ErrorView } from "@/components/ErrorView";
import { ProjectCard } from "@/components/ProjectCard";
import { apiFetch } from "@/lib/api";
import { cached } from "@/lib/cache";
import { projectsReportsSchema } from "@/lib/schemas";

const getProjectsReports = async () => {
  "use server";

  const response = await apiFetch("/api/projects");
  const data = await response.json();

  const { data: projectsData, success } = projectsReportsSchema.safeParse(data);
  if (!success) {
    throw new Error("Inappropriate response from external server.");
  }

  return projectsData;
};

export default function ProjectsReportsPage() {
  const projectsReportsData = createAsync(() =>
    cached({
      fetchFn: getProjectsReports,
      fetchKey: "projectsReports",
    }),
  );

  return (
    <ErrorBoundary
      fallback={(error, reset) => <ErrorView error={error} reset={reset} />}
    >
      <ul class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <For each={projectsReportsData()?.projects}>
          {(project) => <ProjectCard project={project} />}
        </For>
      </ul>
    </ErrorBoundary>
  );
}
