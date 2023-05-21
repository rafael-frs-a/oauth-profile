import UserClient from "@/api/clients/user";
import useSWR, { SWRResponse } from "swr";
import { STORE_KEYS } from "@/utils/constants";
import { UserProfile } from "@/api/clients/user/types";
import { ApiException } from "@/api/types";

type FetchUserProfileHook = Pick<
  SWRResponse<UserProfile>,
  "data" | "error"
>;

export default function useFetchUserProfile(): FetchUserProfileHook {
  const userClient = new UserClient();

  const fetchUserProfile = async (): Promise<UserProfile> => {
    const result = await userClient.getProfile();

    if (result.errors) {
      throw new ApiException(result.errors);
    }

    return result.data;
  };

  const { data, error } = useSWR<UserProfile, ApiException>(
    STORE_KEYS.userProfile,
    fetchUserProfile,
    {
      shouldRetryOnError: false,
    }
  );

  const defaultProfile: UserProfile = {
    email: "",
    compiledProfile: {},
    history: [],
    createdAt: "",
    updatedAt: "",
  };

  const userProfile: UserProfile = data || defaultProfile;
  return { data: userProfile, error };
}
