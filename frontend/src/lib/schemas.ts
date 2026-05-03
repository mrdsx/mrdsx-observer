import { z } from "zod";

const statusSchema = z.enum(["operational", "degraded", "outage"]);

const dailyReportSchema = z.object({
  worstStatus: statusSchema,
  uptime: z.number().min(0).max(100),
  date: z.iso.date(),
});

const projectSchema = z.object({
  id: z.string(),
  name: z.string(),
  currentStatus: statusSchema,
  uptime: z.number().min(0).max(100),
  dailyReports: z.array(dailyReportSchema),
});

const projectsReportsSchema = z.object({
  projects: z.array(projectSchema),
});

type DailyReport = z.infer<typeof dailyReportSchema>;
type Project = z.infer<typeof projectSchema>;
type ProjectsReports = z.infer<typeof projectsReportsSchema>;

export {
  type DailyReport,
  type Project,
  type ProjectsReports,
  projectsReportsSchema,
};
