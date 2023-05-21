import { z } from "zod";

export const ApiErrorSchema = z.object({
  message: z.string(),
  pointer: z.string().nullable(),
  header: z.string().nullable(),
  status: z.number().int(),
});

export type ApiError = z.infer<typeof ApiErrorSchema>;

export const ApiResponseSchema = (dataSchema: z.ZodType = z.any()) =>
  z.object({
    success: z.boolean(),
    data: dataSchema.nullable(),
    errors: z.array(ApiErrorSchema).nullable(),
  });

const ApiResponseSchemaType = ApiResponseSchema();

export type ApiResponse = z.infer<typeof ApiResponseSchemaType>;

export class ApiException extends Error {
  constructor(public errors: ApiError[]) {
    super("Invalid API response");
  }
}
