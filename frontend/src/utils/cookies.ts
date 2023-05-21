import nookies from "nookies";
import { GetServerSidePropsContext } from "next";

export default class Cookies {
  context?: GetServerSidePropsContext;
  defaultOptions = { path: "/", maxAge: 30 * 24 * 60 * 60 };

  constructor(context?: GetServerSidePropsContext) {
    this.context = context;
  }

  getCookie(key: string) {
    // Disabling security rules as argument is not user-provided input
    // eslint-disable-next-line security/detect-object-injection
    return nookies.get(this.context)[key];
  }

  setCookie(key: string, value: any, options = {}) {
    options = { ...this.defaultOptions, ...options };
    nookies.set(this.context, key, value, options);
  }

  deleteCookie(key: string, options = {}) {
    options = { ...this.defaultOptions, maxAge: 0, ...options };
    nookies.destroy(this.context, key, options);
  }
}
