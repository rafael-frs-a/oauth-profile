import BaseClient from "..";
import { ProfileResponse, ProfileResponseSchema } from "./types";
import { getApiClient } from "@/api";
import { INVALID_SERVER_RESPONSE } from "@/utils/constants";
import AuthClient from "../auth";

export default class UserClient extends BaseClient {
  authClient: AuthClient;

  constructor(context?: any) {
    super(context);
    this.authClient = new AuthClient(context);
  }

  async getProfile(): Promise<ProfileResponse> {
    const inner = async () => {
      const api = getApiClient(this.context);
      const response = await api.get("/user/profile");
      const parseResult = ProfileResponseSchema.safeParse(response.data);

      if (!parseResult.success) return INVALID_SERVER_RESPONSE;

      const result: ProfileResponse = response.data;
      return result;
    };

    return await this.authClient.refreshTokenIfRejected(inner);
  }
}
