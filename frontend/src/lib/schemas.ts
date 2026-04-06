import { z } from "zod";

const projectsSchema = z.object({
  projects: z.array(
    z.object({
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
    }),
  ),
});

type Project = z.infer<typeof projectsSchema>;

export { type Project, projectsSchema };
