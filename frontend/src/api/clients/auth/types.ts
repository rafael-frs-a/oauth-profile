import { z } from "zod";
import { ApiResponseSchema } from "@/api/types";

export const AuthorizeRequestSchema = z.object({
  callbackUrl: z.string().url(),
  redirectAfterLogoutUrl: z.string().url().nullable(),
});

export type AuthorizeRequest = z.infer<typeof AuthorizeRequestSchema>;

export const AuthorizationSchema = z.object({
  authorizationUrl: z.string().url(),
  logoutUrl: z.string().url(),
  nonce: z.string(),
});

export type Authorization = z.infer<typeof AuthorizationSchema>;

export const AuthorizeResponseSchema = ApiResponseSchema(
  AuthorizationSchema
);

export type AuthorizeResponse = z.infer<typeof AuthorizeResponseSchema>;

export const LoginRequestSchema = z.object({
  code: z.string(),
  callbackUrl: z.string().url(),
  nonce: z.string(),
});

export type LoginRequest = z.infer<typeof LoginRequestSchema>;

export const AuthenticationCredentialsSchema = z.object({
  accessToken: z.string(),
  refreshToken: z.string(),
});

export type AuthorizationToken = z.infer<
  typeof AuthenticationCredentialsSchema
>;

export const LoginResponseSchema = ApiResponseSchema(
  AuthenticationCredentialsSchema
);

export type LoginResponse = z.infer<typeof LoginResponseSchema>;

export const RefreshTokenRequestSchema = z.object({
  refreshToken: z.string(),
});

export type RefreshTokenRequest = z.infer<typeof RefreshTokenRequestSchema>;

export const RefreshTokenResponseSchema = ApiResponseSchema(
  AuthenticationCredentialsSchema
);

export type RefreshTokenResponse = z.infer<
  typeof RefreshTokenResponseSchema
>;
