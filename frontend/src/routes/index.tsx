import { createAsync, query } from "@solidjs/router";
import { ErrorBoundary, For, Suspense } from "solid-js";
import { ErrorView } from "@/components/ErrorView";
import { ProjectCard } from "@/components/ProjectCard";
import { Spinner } from "@/components/ui/spinner";
import { apiFetch } from "@/lib/api";
import { projectsReportsSchema } from "@/lib/schemas";

const getProjectsReportsQuery = query(async () => {
  "use server";

  const response = await apiFetch("/api/projects");
  const data = await response.json();

  const { data: projectsData, success } = projectsReportsSchema.safeParse(data);
  if (!success) {
    throw new Error("Inappropriate response from external server.");
  }

  return projectsData;
}, "projectsReports");

export default function ProjectsReportsPage() {
  const projectsReportsData = createAsync(() => getProjectsReportsQuery());

  return (
    <ErrorBoundary
      fallback={(error, reset) => <ErrorView error={error} reset={reset} />}
    >
      <Suspense fallback={<Spinner />}>
        <ul class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <For each={projectsReportsData()?.projects}>
            {(project) => <ProjectCard project={project} />}
          </For>
        </ul>
      </Suspense>
    </ErrorBoundary>
  );
}
