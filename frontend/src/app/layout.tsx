import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Ash Loves Files — Universal File Converter",
  description:
    "Convert any file to any format. Images, documents, audio, video, ebooks, archives, data files, fonts and more — all free, no sign-up required.",
  keywords: [
    "file converter",
    "format converter",
    "image converter",
    "video converter",
    "audio converter",
    "document converter",
    "free converter",
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-screen">{children}</body>
    </html>
  );
}
