"use client";

import React from "react";
import { OctagonAlert, CheckCircle2, ShieldAlert, ArrowRight, HelpCircle } from "lucide-react";
import { TrustBreakpointData } from "@/types";
import { useLanguage } from "@/lib/i18n";

interface TrustBreakpointCardProps {
  breakpoint: TrustBreakpointData;
  onViewEvidence?: (evidenceIds: string[]) => void;
}

export function TrustBreakpointCard({
  breakpoint,
  onViewEvidence,
}: TrustBreakpointCardProps) {
  const { t, simpleMode } = useLanguage();

  const isStopRecommended = breakpoint.status === "RECOMMENDED_STOP";
  const isNoExplicitStop = breakpoint.status === "NO_EXPLICIT_STOP";

  const handleScrollToEvidence = () => {
    if (onViewEvidence && breakpoint.evidence_ids.length > 0) {
      onViewEvidence(breakpoint.evidence_ids);
    } else {
      const el = document.getElementById("evidence-section") || document.getElementById("tabs-evidence");
      if (el) {
        el.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }
  };

  return (
    <section
      id="trust-breakpoint-card"
      aria-label="Trust Breakpoint"
      className={`relative overflow-hidden rounded-2xl border transition-all duration-300 ${
        isStopRecommended
          ? "border-red-500/40 bg-gradient-to-br from-red-950/40 via-slate-900/90 to-slate-950/95 shadow-xl shadow-red-950/30"
          : isNoExplicitStop
          ? "border-amber-500/30 bg-gradient-to-br from-amber-950/20 via-slate-900/90 to-slate-950/95 shadow-lg shadow-amber-950/20"
          : "border-slate-800 bg-slate-900/70"
      }`}
    >
      {/* Decorative top accent line */}
      <div
        className={`h-1.5 w-full ${
          isStopRecommended
            ? "bg-gradient-to-r from-red-600 via-rose-500 to-amber-500 animate-pulse"
            : isNoExplicitStop
            ? "bg-gradient-to-r from-amber-600 to-yellow-500"
            : "bg-slate-700"
        }`}
      />

      <div className="p-5 sm:p-6 lg:p-7 space-y-6">
        {/* Header Badge & Meta */}
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <span
              className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold tracking-wider uppercase ${
                isStopRecommended
                  ? "bg-red-500/20 border border-red-500/40 text-red-300"
                  : isNoExplicitStop
                  ? "bg-amber-500/20 border border-amber-500/40 text-amber-300"
                  : "bg-slate-800 border border-slate-700 text-slate-300"
              }`}
            >
              <OctagonAlert className={`h-3.5 w-3.5 ${isStopRecommended ? "text-red-400 animate-bounce" : "text-amber-400"}`} />
              {t.trustBreakpointBadge}
            </span>
            <span className="text-[11px] font-mono uppercase tracking-widest text-slate-400">
              Track A • Decision Interception
            </span>
          </div>

          {breakpoint.source_stage && (
            <span className="text-[11px] font-mono px-2.5 py-0.5 rounded-md bg-slate-950/80 border border-slate-800 text-slate-400">
              Stage: {breakpoint.source_stage}
            </span>
          )}
        </div>

        {/* Primary Interception Banner */}
        <div className="space-y-3">
          <h3 className="text-sm font-semibold tracking-wide text-slate-400 uppercase flex items-center gap-2">
            <span>🔴</span> {t.trustBreakpointTitle}
          </h3>

          {isStopRecommended ? (
            <div className="rounded-xl border border-red-500/50 bg-red-950/50 p-4 sm:p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="text-xl sm:text-2xl lg:text-3xl font-black tracking-tight text-white flex flex-wrap items-baseline gap-2">
                  <span className="text-red-400">{t.trustBreakpointStopPrefix}</span>
                  {breakpoint.amount ? (
                    <span className="text-amber-300 underline decoration-red-500 underline-offset-4 font-mono font-extrabold">
                      {breakpoint.amount}
                    </span>
                  ) : (
                    <span className="text-white">{t.trustBreakpointStopGeneric}</span>
                  )}
                </div>
                <p className="text-sm text-slate-300 max-w-2xl leading-relaxed pt-1">
                  {simpleMode
                    ? t.trustBreakpointSimpleModeExplanation
                    : breakpoint.reason}
                </p>
              </div>

              <div className="shrink-0">
                <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-red-900/60 border border-red-500/40 text-xs font-bold text-red-200">
                  <ShieldAlert className="h-4 w-4 text-red-400" />
                  {t.trustBreakpointRecommendedStop}
                </div>
              </div>
            </div>
          ) : isNoExplicitStop ? (
            <div className="rounded-xl border border-amber-500/40 bg-amber-950/30 p-4 sm:p-5 space-y-2">
              <div className="text-lg sm:text-xl font-bold tracking-tight text-amber-200 flex items-center gap-2">
                <HelpCircle className="h-5 w-5 text-amber-400 shrink-0" />
                <span>{t.trustBreakpointNoExplicitPayment}</span>
              </div>
              <p className="text-sm text-slate-300 leading-relaxed">
                {simpleMode
                  ? "रक्षास्कैन ने जोखिम संकेत पाए हैं, लेकिन दिए गए संदेश में किसी विशिष्ट खाते या राशि को ट्रांसफर करने का सीधा अनुरोध नहीं दिखा। सतर्क रहें और आधिकारिक पुष्टि के बिना कुछ भी साझा न करें।"
                  : t.trustBreakpointNoExplicitPaymentDesc}
              </p>
            </div>
          ) : (
            <div className="rounded-xl border border-slate-800 bg-slate-950/50 p-4 space-y-2">
              <div className="text-base font-bold text-slate-200">
                {t.trustBreakpointInsufficientEvidence}
              </div>
              <p className="text-sm text-slate-400 leading-relaxed">
                {breakpoint.reason}
              </p>
            </div>
          )}
        </div>

        {/* Why? Section with Supporting Signals */}
        {breakpoint.supporting_signals.length > 0 && (
          <div className="rounded-xl border border-slate-800/80 bg-slate-950/60 p-4 sm:p-5 space-y-3">
            <h4 className="text-xs font-bold tracking-wider uppercase text-slate-300 flex items-center gap-1.5">
              <span>{t.trustBreakpointWhy}</span>
              <span className="text-[11px] font-normal text-slate-400 lowercase">
                ({t.trustBreakpointSupportingSignals})
              </span>
            </h4>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              {breakpoint.supporting_signals.map((sig, sIdx) => (
                <div
                  key={sIdx}
                  className="flex items-start gap-2.5 p-2.5 rounded-lg bg-slate-900/70 border border-slate-800 text-xs text-slate-200"
                >
                  <CheckCircle2
                    className={`h-4 w-4 shrink-0 mt-0.5 ${
                      isStopRecommended ? "text-red-400" : "text-amber-400"
                    }`}
                  />
                  <span className="leading-snug">{sig}</span>
                </div>
              ))}
            </div>

            {/* Action buttons / link to evidence */}
            <div className="pt-2 flex flex-wrap items-center justify-between gap-3 border-t border-slate-800/80 mt-4">
              <span className="text-[11px] text-slate-400">
                {breakpoint.evidence_ids.length > 0
                  ? `${breakpoint.evidence_ids.length} supporting evidence records`
                  : "Observable signals extracted from input"}
              </span>

              <button
                type="button"
                onClick={handleScrollToEvidence}
                className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-cyan-300 hover:text-cyan-200 text-xs font-semibold border border-slate-700 hover:border-cyan-500/50 transition-all shadow-sm group"
              >
                <span>{t.trustBreakpointViewEvidence}</span>
                <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" />
              </button>
            </div>
          </div>
        )}

        {/* Epistemic disclaimer */}
        <div className="text-[11px] text-slate-400 italic bg-slate-950/40 p-2.5 rounded-lg border border-slate-800/50">
          ⚠️ {breakpoint.disclaimer}
        </div>
      </div>
    </section>
  );
}
