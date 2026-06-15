import { createAsync, useParams } from "@solidjs/router";
import { ArrowLeftIcon } from "lucide-solid";
import { ErrorBoundary, For } from "solid-js";
import { ErrorView } from "@/components/ErrorView";
import { ServiceCard } from "@/components/ServiceCard";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";
import { cached } from "@/lib/cache";
import { NotFoundError } from "@/lib/errors";
import { servicesReportsSchema } from "@/lib/schemas";
import { sortByName } from "@/lib/utils";

const getServicesReports = async (projectId: string) => {
  "use server";

  const response = await apiFetch(`/api/projects/${projectId}`);
  const data = await response.json();

  if (response.status === 404) {
    throw new NotFoundError("Services reports not found.");
  }

  const { data: servicesData, success } = servicesReportsSchema.safeParse(data);
  if (!success) {
    throw new Error("Inappropriate response from external server.");
  }

  return servicesData;
};

export default function ServicesReportsPage() {
  const params = useParams();
  const servicesReportsData = createAsync(() =>
    cached({
      fetchFn: () => {
        if (params.id === undefined) {
          return undefined;
        }
        return getServicesReports(params.id);
      },
      fetchKey: `projectsReports/${params.id}`,
    }),
  );

  return (
    <ErrorBoundary
      fallback={(error, reset) => <ErrorView error={error} reset={reset} />}
    >
      <div class="space-y-4">
        <Button as="a" href="/" variant="outline">
          <ArrowLeftIcon />
          Back
        </Button>
        <h1 class="text-2xl font-semibold">
          {servicesReportsData()?.projectName}
        </h1>
        <ul class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <For each={sortByName(servicesReportsData()?.services)}>
            {(service) => <ServiceCard service={service} />}
          </For>
        </ul>
      </div>
    </ErrorBoundary>
  );
}
