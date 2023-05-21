export function trim(
  value: string,
  leadingChars?: string,
  trailingChars?: string
): string {
  if (!value) {
    return "";
  }

  if (!leadingChars && !trailingChars) {
    return value.trim();
  }

  if (!trailingChars) {
    trailingChars = leadingChars;
  }

  // Disabling security rules as arguments are not user-provided inputs
  // eslint-disable-next-line security/detect-non-literal-regexp
  const leadingPattern = new RegExp(`^(${leadingChars})+`);
  // eslint-disable-next-line security/detect-non-literal-regexp
  const trailingPattern = new RegExp(`(${trailingChars})+$`);
  let result = value;
  result = result.replace(leadingPattern, "");
  result = result.replace(trailingPattern, "");
  return result;
}
