import { createAsync, query, useParams } from "@solidjs/router";
import { ArrowLeftIcon } from "lucide-solid";
import { ErrorBoundary, For } from "solid-js";
import { ErrorView } from "@/components/ErrorView";
import { ServiceCard } from "@/components/ServiceCard";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";
import { NotFoundError } from "@/lib/errors";
import { servicesReportsSchema } from "@/lib/schemas";

const getServicesReportsQuery = query(async (projectId: string) => {
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
}, "servicesReports");

export default function ServicesReportsPage() {
  const params = useParams();
  const servicesReportsData = createAsync(() =>
    getServicesReportsQuery(params.id as string),
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
          <For each={servicesReportsData()?.services}>
            {(service) => <ServiceCard service={service} />}
          </For>
        </ul>
      </div>
    </ErrorBoundary>
  );
}
