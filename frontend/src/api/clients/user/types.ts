import { z } from "zod";
import { ApiResponseSchema } from "@/api/types";

export const UserProfileSchema = z.object({
  email: z.string().email(),
  compiledProfile: z.record(z.any()),
  history: z.array(z.any()),
  createdAt: z.string().datetime(),
  updatedAt: z.string().datetime(),
});

export type UserProfile = z.infer<typeof UserProfileSchema>;

export const ProfileResponseSchema =
  ApiResponseSchema(UserProfileSchema);

export type ProfileResponse = z.infer<typeof ProfileResponseSchema>;
