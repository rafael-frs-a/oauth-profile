import { ReactNode } from "react";
import { Header } from "../Header";
import { Toaster } from "react-hot-toast";

export interface LayoutProps {
  children: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  return (
    <>
      <Header />
      <Toaster
        toastOptions={{
          className: "bg-gray-200 text-black dark:bg-gray-700 dark:text-white",
          duration: 8000,
        }}
      />
      <main className="flex min-h-[calc(100vh-64px)] flex-col bg-gray-200 text-black dark:bg-gray-800 dark:text-white">
        {children}
      </main>
    </>
  );
}
