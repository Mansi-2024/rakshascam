"use client";

import * as React from "react";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { Hero } from "@/components/analysis/Hero";
import { AnalysisInputCard } from "@/components/analysis/AnalysisInputCard";
import { WebsiteAnalysisResult } from "@/components/analysis/WebsiteAnalysisResult";
import { TrustConceptSection } from "@/components/trust-chain/TrustConceptSection";
import { FeatureSection } from "@/components/features/FeatureSection";
import { AnalysisResultPreview } from "@/components/analysis/AnalysisResultPreview";
import { MOCK_ANALYSIS_RESULT } from "@/lib/mockData";
import { analyzeMessageApi, analyzeScreenshotApi, analyzeUrlApi } from "@/lib/api";
import { AnalysisInputMode, AnalysisResult, WebsiteAnalysisData } from "@/types";

export default function Home() {
  const [isAnalyzing, setIsAnalyzing] = React.useState(false);
  const [analysisError, setAnalysisError] = React.useState<string | null>(null);
  const [websiteAnalysis, setWebsiteAnalysis] = React.useState<WebsiteAnalysisData | null>(null);
  const [activeResult, setActiveResult] = React.useState<AnalysisResult>(MOCK_ANALYSIS_RESULT);
  const resultRef = React.useRef<HTMLDivElement>(null);

  const handleAnalyze = async (
    inputVal: string,
    mode: AnalysisInputMode = "message",
    file?: File | null
  ) => {
    setIsAnalyzing(true);
    setAnalysisError(null);

    if (mode === "website" || mode === "message" || mode === "screenshot") {
      try {
        let liveResult: WebsiteAnalysisData;
        if (mode === "website") {
          liveResult = await analyzeUrlApi(inputVal);
        } else if (mode === "message") {
          liveResult = await analyzeMessageApi(inputVal);
        } else {
          if (!file) {
            throw new Error("No image file provided for screenshot analysis.");
          }
          liveResult = await analyzeScreenshotApi(file);
        }

        setWebsiteAnalysis(liveResult);

        // Update target artifact label on mock example dossier for visual continuity
        setActiveResult((prev) => ({
          ...prev,
          targetArtifact:
            liveResult.input.normalized_url ||
            (mode === "message"
              ? "User Submitted Message"
              : mode === "screenshot"
              ? `Screenshot OCR: ${file?.name || "Image"}`
              : inputVal),
        }));

        // Smooth scroll to the newly generated Analysis section
        setTimeout(() => {
          const analysisEl = document.getElementById("website-analysis");
          if (analysisEl) {
            analysisEl.scrollIntoView({ behavior: "smooth" });
          }
        }, 100);
      } catch (err: unknown) {
        const errMsg =
          err instanceof Error
            ? err.message
            : `Failed to analyze ${mode}. Please check inputs or backend connection.`;
        setAnalysisError(errMsg);
      } finally {
        setIsAnalyzing(false);
      }
    } else {
      // Simulate mock registry verification latency for entity queries
      setTimeout(() => {
        setIsAnalyzing(false);
        setActiveResult({
          ...MOCK_ANALYSIS_RESULT,
          targetArtifact: `Entity Query: '${inputVal}'`,
        });

        // Smooth scroll to example assessment preview
        const previewEl = document.getElementById("example-assessment");
        if (previewEl) {
          previewEl.scrollIntoView({ behavior: "smooth" });
        }
      }, 1000);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#090d16] text-slate-100">
      <Navbar />

      <main className="flex-1">
        {/* Hero Section */}
        <Hero />

        {/* Central Analysis Input Card */}
        <div className="mb-12">
          <AnalysisInputCard
            onAnalyze={handleAnalyze}
            isAnalyzing={isAnalyzing}
            externalError={analysisError}
          />
        </div>

        {/* Real Phase 2 Live Website Analysis Result */}
        {websiteAnalysis && (
          <div className="mb-16">
            <WebsiteAnalysisResult data={websiteAnalysis} />
          </div>
        )}

        {/* Core Concept: Trust Chain Section */}
        <TrustConceptSection />

        {/* Features Section */}
        <FeatureSection />

        {/* Analysis Result Preview (Always clearly labeled as Example Assessment) */}
        <div ref={resultRef}>
          <AnalysisResultPreview result={activeResult} />
        </div>
      </main>

      <Footer />
    </div>
  );
}
