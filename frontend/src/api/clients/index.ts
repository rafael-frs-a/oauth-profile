import { GetServerSidePropsContext } from "next";

export default class BaseClient {
  context?: GetServerSidePropsContext;

  constructor(context?: GetServerSidePropsContext) {
    this.context = context;
  }
}
