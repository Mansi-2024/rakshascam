import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "RakshaScan — Evidence-Based Financial Scam & Trust Verification",
  description:
    "Before you trust it, verify the story behind it. Check financial websites, claims, messages and identities before they become a financial risk.",
  keywords: [
    "RakshaScan",
    "financial scam verification",
    "trust chain",
    "SEBI verification",
    "investor protection",
    "India cybercrime helpline 1930",
    "evidence based trust",
  ],
  authors: [{ name: "RakshaScan Team" }],
  openGraph: {
    title: "RakshaScan — Before you trust it, verify the story behind it.",
    description:
      "Evidence-based financial scam and trust-verification platform for Indian investors.",
    type: "website",
  },
};

import { LanguageProvider } from "@/lib/i18n";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased dark`}
    >
      <body className="min-h-full flex flex-col bg-[#090d16] text-slate-100 font-sans selection:bg-blue-600 selection:text-white">
        <LanguageProvider>
          {children}
        </LanguageProvider>
      </body>
    </html>
  );
}

