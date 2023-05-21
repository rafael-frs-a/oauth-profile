import axios from "axios";
import getConfig from "next/config";
import { AxiosResponse } from "axios";
import { ApiResponse } from "./types";
import { STORE_KEYS } from "@/utils/constants";
import { GetServerSidePropsContext } from "next";
import Cookies from "@/utils/cookies";

const { publicRuntimeConfig: env } = getConfig();

export function getApiClient(context?: GetServerSidePropsContext) {
  const cookies = new Cookies(context);
  const api = axios.create({
    baseURL: env.API_BASE_URL,
  });

  api.interceptors.request.use((config) => {
    const accessToken = cookies.getCookie(STORE_KEYS.appAccessToken);

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    return config;
  });

  api.interceptors.response.use(
    (response) => {
      return response;
    },
    (err) => {
      const response: AxiosResponse = err.response || {};

      if (err.code === "ECONNREFUSED" || err.code === "ERR_NETWORK") {
        const data: ApiResponse = {
          success: false,
          data: null,
          errors: [
            {
              message: "common:serverUnavailable",
              status: 500,
              pointer: null,
              header: null,
            },
          ],
        };

        response.data = data;
      }

      return response;
    }
  );

  return api;
}
