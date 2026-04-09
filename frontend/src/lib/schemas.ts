import { z } from "zod";

const projectSchema = z.object({
  id: z.string(),
  name: z.string(),
  status: z.enum(["operational", "degraded", "outage"]),
  uptime: z.number().min(0).max(100),
  dailyReports: z.array(
    z.object({
      worstStatus: z.enum(["operational", "degraded", "outage"]),
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
