"use client";

import * as React from "react";
import { AnalysisResult } from "@/types";
import { SeverityBadge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { TrustChainVisualizer } from "@/components/trust-chain/TrustChainVisualizer";
import { ScamJourneyTimeline } from "@/components/scam-journey/ScamJourneyTimeline";
import {
  AlertTriangle,
  CheckCircle2,
  HelpCircle,
  ShieldCheck,
  ExternalLink,
  PhoneCall,
  Search,
  Eye,
} from "lucide-react";

interface AnalysisResultPreviewProps {
  result: AnalysisResult;
}

export function AnalysisResultPreview({ result }: AnalysisResultPreviewProps) {
  const [activeTab, setActiveTab] = React.useState<"findings" | "trust-chain" | "journey" | "safety">("findings");

  return (
    <section id="example-assessment" className="py-16 scroll-mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        {/* Prominent Demo/Mock Banner Warning */}
        <div className="rounded-xl border-2 border-dashed border-amber-600/70 bg-amber-950/20 p-4 sm:p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-lg bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400 shrink-0">
              <Eye className="h-5 w-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-white text-sm sm:text-base">
                  Example assessment
                </span>
                <span className="rounded bg-amber-500/20 px-2 py-0.5 text-[11px] font-mono font-bold text-amber-300 border border-amber-500/40 uppercase">
                  DEMONSTRATION PREVIEW
                </span>
              </div>
              <p className="text-xs text-amber-200/80 leading-relaxed mt-0.5">
                This is a mock sample illustrating RakshaScan&apos;s evidence-based reporting format. It does not represent a real analysis or a judicial determination of an actual entity.
              </p>
            </div>
          </div>
          <div className="shrink-0 text-xs font-mono text-slate-400 bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800">
            Target: <span className="text-blue-400 font-semibold">{result.targetArtifact}</span>
          </div>
        </div>

        {/* Primary Assessment Header Card */}
        <Card className="border-slate-800 bg-slate-900/90 shadow-xl overflow-hidden">
          <div className="p-6 sm:p-8 space-y-6">
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-6 border-b border-slate-800">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-xs font-mono uppercase tracking-wider text-slate-400">
                    Trust Signal Synthesis
                  </span>
                </div>
                <h3 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
                  Analysis Dossier: {result.targetArtifact}
                </h3>
              </div>

              {/* High Concern Badge */}
              <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
                <SeverityBadge severity={result.overallConcern} />
              </div>
            </div>

            {/* Core Primary Reasons Block */}
            <div className="p-5 rounded-xl border border-rose-900/40 bg-rose-950/20 space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-rose-300 font-mono flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-rose-400" />
                <span>Primary Signals of Concern</span>
              </h4>
              <ul className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {result.primaryReasons.map((reason, idx) => (
                  <li
                    key={idx}
                    className="flex items-start gap-2.5 p-3 rounded-lg bg-slate-950/70 border border-rose-900/30 text-xs text-rose-200 font-medium"
                  >
                    <span className="h-1.5 w-1.5 rounded-full bg-rose-400 shrink-0 mt-1.5" />
                    <span>{reason}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* View Navigation Tabs */}
            <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-3">
              <button
                type="button"
                onClick={() => setActiveTab("findings")}
                className={`px-4 py-2 rounded-lg text-xs sm:text-sm font-semibold transition-all ${
                  activeTab === "findings"
                    ? "bg-blue-600 text-white shadow-sm"
                    : "bg-slate-800/60 text-slate-400 hover:text-slate-200"
                }`}
              >
                Factual Evidence Breakdown
              </button>
              <button
                type="button"
                onClick={() => setActiveTab("trust-chain")}
                className={`px-4 py-2 rounded-lg text-xs sm:text-sm font-semibold transition-all ${
                  activeTab === "trust-chain"
                    ? "bg-blue-600 text-white shadow-sm"
                    : "bg-slate-800/60 text-slate-400 hover:text-slate-200"
                }`}
              >
                Visual Trust Chain ({result.trustChainNodes.length})
              </button>
              <button
                type="button"
                onClick={() => setActiveTab("journey")}
                className={`px-4 py-2 rounded-lg text-xs sm:text-sm font-semibold transition-all ${
                  activeTab === "journey"
                    ? "bg-blue-600 text-white shadow-sm"
                    : "bg-slate-800/60 text-slate-400 hover:text-slate-200"
                }`}
              >
                Scam Journey Pattern ({result.scamJourneyStages.length})
              </button>
              <button
                type="button"
                onClick={() => setActiveTab("safety")}
                className={`px-4 py-2 rounded-lg text-xs sm:text-sm font-semibold transition-all ${
                  activeTab === "safety"
                    ? "bg-blue-600 text-white shadow-sm"
                    : "bg-slate-800/60 text-slate-400 hover:text-slate-200"
                }`}
              >
                Safe Next Steps
              </button>
            </div>

            {/* TAB 1: 4-Quadrant Evidence Breakdown */}
            {activeTab === "findings" && (
              <div className="space-y-6 animate-fadeIn">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                  {/* 1. What We Found */}
                  <div className="p-5 rounded-xl border border-slate-800 bg-slate-950/60 space-y-3">
                    <div className="flex items-center gap-2 text-xs font-bold font-mono uppercase tracking-wider text-slate-300">
                      <Search className="h-4 w-4 text-blue-400" />
                      <span>What we found</span>
                    </div>
                    <ul className="space-y-2.5 text-xs text-slate-300">
                      {result.findings.whatWeFound.map((item, i) => (
                        <li key={i} className="flex items-start gap-2.5 leading-relaxed">
                          <span className="h-1.5 w-1.5 rounded-full bg-blue-400 shrink-0 mt-1.5" />
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* 2. What We Verified */}
                  <div className="p-5 rounded-xl border border-slate-800 bg-slate-950/60 space-y-3">
                    <div className="flex items-center gap-2 text-xs font-bold font-mono uppercase tracking-wider text-emerald-400">
                      <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                      <span>What we verified</span>
                    </div>
                    <ul className="space-y-2.5 text-xs text-slate-300">
                      {result.findings.whatWeVerified.map((item, i) => (
                        <li key={i} className="flex items-start gap-2.5 leading-relaxed">
                          <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 shrink-0 mt-1.5" />
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* 3. What Remains Uncertain */}
                  <div className="p-5 rounded-xl border border-slate-800 bg-slate-950/60 space-y-3">
                    <div className="flex items-center gap-2 text-xs font-bold font-mono uppercase tracking-wider text-amber-400">
                      <HelpCircle className="h-4 w-4 text-amber-400" />
                      <span>What remains uncertain</span>
                    </div>
                    <ul className="space-y-2.5 text-xs text-slate-300">
                      {result.findings.whatRemainsUncertain.map((item, i) => (
                        <li key={i} className="flex items-start gap-2.5 leading-relaxed">
                          <span className="h-1.5 w-1.5 rounded-full bg-amber-400 shrink-0 mt-1.5" />
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* 4. Why This Was Flagged */}
                  <div className="p-5 rounded-xl border border-slate-800 bg-slate-950/60 space-y-3">
                    <div className="flex items-center gap-2 text-xs font-bold font-mono uppercase tracking-wider text-rose-400">
                      <AlertTriangle className="h-4 w-4 text-rose-400" />
                      <span>Why this was flagged</span>
                    </div>
                    <ul className="space-y-2.5 text-xs text-slate-300">
                      {result.findings.whyFlagged.map((item, i) => (
                        <li key={i} className="flex items-start gap-2.5 leading-relaxed">
                          <span className="h-1.5 w-1.5 rounded-full bg-rose-400 shrink-0 mt-1.5" />
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            )}

            {/* TAB 2: Visual Trust Chain */}
            {activeTab === "trust-chain" && (
              <div className="animate-fadeIn">
                <TrustChainVisualizer
                  nodes={result.trustChainNodes}
                  relationships={result.trustChainRelationships}
                />
              </div>
            )}

            {/* TAB 3: Scam Journey Pattern */}
            {activeTab === "journey" && (
              <div className="animate-fadeIn">
                <ScamJourneyTimeline stages={result.scamJourneyStages} />
              </div>
            )}

            {/* TAB 4: Safe Next Steps */}
            {activeTab === "safety" && (
              <div id="safe-steps" className="space-y-6 animate-fadeIn">
                <div className="p-5 rounded-xl border border-blue-900/40 bg-blue-950/20">
                  <h4 className="text-sm font-bold text-white flex items-center gap-2 mb-2">
                    <ShieldCheck className="h-4 w-4 text-blue-400" />
                    <span>Defensive Guidance & Verification Protocols</span>
                  </h4>
                  <p className="text-xs text-slate-300 leading-relaxed mb-4">
                    RakshaScan provides defensive safety checklists. We do not provide financial or legal advice. If you suspect an unauthorized offering, follow these institutional steps:
                  </p>
                  <ul className="space-y-3">
                    {result.safeNextSteps.map((step, idx) => (
                      <li
                        key={idx}
                        className="flex items-start gap-3 p-3 rounded-lg bg-slate-950/60 border border-slate-800 text-xs text-slate-200"
                      >
                        <span className="h-5 w-5 rounded-full bg-blue-600/20 border border-blue-500/40 text-blue-300 flex items-center justify-center font-mono text-[10px] shrink-0 font-bold">
                          {idx + 1}
                        </span>
                        <span className="leading-relaxed">{step}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Emergency Hotline callout */}
                <div className="rounded-xl border border-amber-900/60 bg-amber-950/30 p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 text-amber-300 font-semibold text-sm">
                      <PhoneCall className="h-4 w-4" />
                      <span>Transferred Money Already? Act Within The Golden Hour</span>
                    </div>
                    <p className="text-xs text-amber-200/80">
                      Call <strong>1930</strong> immediately to request banking rail lien-marking and freeze suspect UPI accounts before cash-out.
                    </p>
                  </div>
                  <a
                    href="https://cybercrime.gov.in"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 bg-amber-600 hover:bg-amber-500 text-white text-xs font-semibold px-4 py-2.5 rounded-lg transition-colors shrink-0"
                  >
                    <span>File at cybercrime.gov.in</span>
                    <ExternalLink className="h-3.5 w-3.5" />
                  </a>
                </div>
              </div>
            )}
          </div>
        </Card>
      </div>
    </section>
  );
}
