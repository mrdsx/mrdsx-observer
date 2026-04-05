from core.types import ServiceStatus


def worst_status(*statuses: ServiceStatus) -> ServiceStatus:
    statuses_set = set(statuses)
    if "outage" in statuses_set:
        return "outage"
    elif "degraded" in statuses_set:
        return "degraded"
    return "operational"
