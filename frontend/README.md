# About

The frontend uses, among others, the following technologies:
- Next.js: a popular open-source framework for React with server-side rendering;
- TypeScript: for type-safety;
- Tailwind CSS: for styling;
- Next-translate: to support multiple languages;
- Next-themes: used with Tailwind to support dark mode (very important feature!);
- Nookies: for cookies management;
- SWR: for helping with data fetching/revalidation and acting as a React Context API to share states across the application;
- Axios: for HTTP requests;
- Zod: for object parsing;
- Eslint-plugin-security: to check the code for potential security vulnerabilities.

The `/bin` folder contains bash files meant to be used with CI/CD pipelines. It consists of:
- `check_linting_and_security.sh`: runs `eslint` and `eslint-plugin-security`;
- `check_types.sh`: uses TypeScript to check type-safety on files;
- `start.sh`: starts frontend server.

# Considerations

Since TypeScript doesn't have a built-in way of checking/validating an generic object against an interface or type, I had two options when deciding how to represent backend types on the frontend:
1. Use `openapi-typescript` to autogenerate TypeScript interfaces out of the backend's OpenAPI schema and trust the backend returned responses would correctly follow their schemas;
2. Use a form-validation package like `zod` to manually implement the expected backend schemas on frontend and use its built-in parsing methods to validate backend responses.

After seeing the "trust" part on option #1, I opted for #2.
