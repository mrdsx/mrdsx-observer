import { z } from "zod";

const statusSchema = z.enum(["operational", "degraded", "outage"]);
const uptimeSchema = z.number().min(0).max(100);

const dailyReportSchema = z.object({
  date: z.iso.date(),
  worstStatus: statusSchema,
  uptime: uptimeSchema,
});

type DailyReport = z.infer<typeof dailyReportSchema>;

const projectSchema = z.object({
  id: z.string(),
  name: z.string(),
  currentStatus: statusSchema,
  uptime: uptimeSchema,
  dailyReports: z.array(dailyReportSchema),
});

const projectsReportsSchema = z.object({
  projects: z.array(projectSchema),
});

type Project = z.infer<typeof projectSchema>;
type ProjectsReports = z.infer<typeof projectsReportsSchema>;

const serviceSchema = z.object({
  name: z.string(),
  currentStatus: statusSchema,
  uptime: uptimeSchema,
  dailyReports: z.array(dailyReportSchema),
});

const servicesReportsSchema = z.object({
  projectName: z.string(),
  services: z.array(serviceSchema),
});

type ServicesReports = z.infer<typeof servicesReportsSchema>;

export {
  type DailyReport,
  type Project,
  type ProjectsReports,
  projectsReportsSchema,
  type ServicesReports,
  servicesReportsSchema,
};
