import { z } from "zod";

const statusSchema = z.enum(["operational", "degraded", "outage"]);

const projectSchema = z.object({
  id: z.string(),
  name: z.string(),
  currentStatus: statusSchema,
  uptime: z.number().min(0).max(100),
  dailyReports: z.array(
    z.object({
      worstStatus: statusSchema,
      uptime: z.number().min(0).max(100),
      date: z.iso.date(),
    }),
  ),
});

const projectsReportsSchema = z.object({
  projects: z.array(projectSchema),
});

type Project = z.infer<typeof projectSchema>;

export { type Project, projectsReportsSchema };
