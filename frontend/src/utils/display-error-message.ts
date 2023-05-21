import toast from "react-hot-toast";
import { Translate } from "next-translate";
import { ApiError } from "@/api/types";

export function displayServerError(t: Translate, errors: ApiError[]): void {
  const defaultError = "common:invalidServerResponse";
  const errorMessages: string[] = [];

  errors.forEach((error) => {
    if (error.pointer) return;
    const message = t(error.message, {}, t(defaultError));
    if (!message) return;

    if (!errorMessages.includes(message)) {
      errorMessages.push(message);
    }
  });

  if (errorMessages.length === 0) {
    errorMessages.push(t("common:invalidServerResponse"));
  }

  toast.dismiss();
  errorMessages.forEach((message) => {
    toast.error(message);
  });
}
