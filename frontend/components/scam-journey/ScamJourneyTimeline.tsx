"use client";

import * as React from "react";
import {
  ScamJourneyData,
  ScamJourneyStageData,
  ScamJourneyStage,
  EvidenceItem,
  RiskSignalItem,
} from "@/types";
import {
  MessageSquare,
  TrendingUp,
  Globe,
  Users,
  Wallet,
  Lock,
  ChevronDown,
  ChevronUp,
  AlertTriangle,
  Info,
  CheckCircle2,
  HelpCircle,
  EyeOff,
  Sparkles,
} from "lucide-react";

interface ScamJourneyTimelineProps {
  journey?: ScamJourneyData;
  stages?: ScamJourneyStage[];
  evidenceList?: EvidenceItem[];
  riskSignals?: RiskSignalItem[];
}

function renderStageIcon(order: number, className: string = "h-4 w-4") {
  switch (order) {
    case 1:
      return <MessageSquare className={className} />;
    case 2:
      return <TrendingUp className={className} />;
    case 3:
      return <Globe className={className} />;
    case 4:
      return <Users className={className} />;
    case 5:
      return <Wallet className={className} />;
    case 6:
      return <Lock className={className} />;
    default:
      return <AlertTriangle className={className} />;
  }
}

export function ScamJourneyTimeline({
  journey,
  stages: legacyStages,
  evidenceList = [],
  riskSignals = [],
}: ScamJourneyTimelineProps) {
  // Normalize stages
  const stages: ScamJourneyStageData[] = React.useMemo(() => {
    if (journey && journey.stages && journey.stages.length > 0) {
      return journey.stages;
    }
    if (legacyStages && legacyStages.length > 0) {
      return legacyStages.map((s, idx) => ({
        stage_id: s.id,
        order: s.order || idx + 1,
        stage_type: (
          ["INITIAL_CONTACT", "FINANCIAL_CLAIM", "WEBSITE", "COMMUNICATION_CHANNEL", "DEPOSIT_REQUEST", "WITHDRAWAL_ISSUE"][idx] || "STAGE"
        ),
        title: s.stageName,
        description: s.description,
        status: s.status === "NOT_DETECTED" ? "NOT_OBSERVED" : s.status,
        evidence_ids: [],
        signal_ids: s.observedSignals || [],
        confidence: "MEDIUM",
        why_present: s.description,
        uncertainty: null,
      }));
    }
    return [];
  }, [journey, legacyStages]);

  const [expandedStageId, setExpandedStageId] = React.useState<string | null>(
    stages.length > 0 ? stages[1]?.stage_id || stages[0]?.stage_id || null : null
  );


  const getStatusBadge = (status: string) => {
    const s = status.toUpperCase();
    if (s === "OBSERVED") {
      return {
        label: "OBSERVED",
        border: "border-rose-500/70",
        bg: "bg-rose-950/80 text-rose-300",
        icon: <CheckCircle2 className="h-3 w-3 text-rose-400" />,
      };
    }
    if (s === "SUSPECTED") {
      return {
        label: "SUSPECTED",
        border: "border-amber-500/70",
        bg: "bg-amber-950/80 text-amber-300",
        icon: <AlertTriangle className="h-3 w-3 text-amber-400" />,
      };
    }
    if (s === "NOT_OBSERVED") {
      return {
        label: "NOT OBSERVED",
        border: "border-slate-800",
        bg: "bg-slate-900/60 text-slate-500",
        icon: <EyeOff className="h-3 w-3 text-slate-500" />,
      };
    }
    return {
      label: "UNKNOWN",
      border: "border-slate-700",
      bg: "bg-slate-900 text-slate-400",
      icon: <HelpCircle className="h-3 w-3 text-slate-400" />,
    };
  };

  const supportedCount = stages.filter(
    (s) => s.status.toUpperCase() === "OBSERVED" || s.status.toUpperCase() === "SUSPECTED"
  ).length;

  const journeyConfidence = journey?.confidence || (supportedCount >= 4 ? "HIGH" : supportedCount >= 2 ? "MEDIUM" : "LOW");

  const getConfidenceBadge = (conf: string) => {
    const c = conf.toUpperCase();
    if (c === "HIGH") {
      return {
        label: "HIGH EVIDENCE COMPLETENESS",
        sub: "Substantial observable evidence maps to the multi-stage behavioral model",
        color: "text-amber-400 bg-amber-950/80 border-amber-600/70",
      };
    }
    if (c === "MEDIUM") {
      return {
        label: "MEDIUM EVIDENCE COMPLETENESS",
        sub: "Several observable interaction patterns detected; others unobserved",
        color: "text-blue-300 bg-blue-950/80 border-blue-600/70",
      };
    }
    return {
      label: "LOW EVIDENCE COMPLETENESS",
      sub: "Limited on-page signals available to reconstruct interaction pattern",
      color: "text-slate-400 bg-slate-900 border-slate-700",
    };
  };

  const confInfo = getConfidenceBadge(journeyConfidence);

  return (
    <div className="space-y-6">
      {/* HEADER WITH PATTERN DESCRIPTION & EVIDENCE CONFIDENCE */}
      <div className="p-5 rounded-2xl border border-slate-800 bg-slate-950/90 shadow-xl space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800/80 pb-3">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-indigo-400" />
              <h3 className="text-base sm:text-lg font-bold text-white tracking-wide uppercase">
                Possible Scam Journey Pattern
              </h3>
            </div>
            <p className="text-xs text-slate-400">
              Reconstructed interaction pattern analyzing observable on-page stages against documented deceptive lifecycles.
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs font-mono">
            <span className="px-3 py-1.5 rounded-lg bg-indigo-950/70 border border-indigo-700/60 text-indigo-300 font-bold">
              {supportedCount} of {stages.length} Stages Supported
            </span>
          </div>
        </div>

        {/* Confidence & Meaning Banner (Not a fraud score) */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-xs">
          <div className="space-y-0.5">
            <span className="text-slate-400 text-[10px] font-mono block">
              PATTERN RECONSTRUCTION CONFIDENCE
            </span>
            <span className={`inline-block font-mono font-bold px-2 py-0.5 rounded border text-xs ${confInfo.color}`}>
              {confInfo.label}
            </span>
            <p className="text-[11px] text-slate-400 mt-1">{confInfo.sub}</p>
          </div>
          <div className="text-[10px] text-slate-400 font-mono italic max-w-xs self-start sm:self-center">
            *Confidence reflects evidence completeness in matching an analytical model, NOT a probability of fraud.
          </div>
        </div>

        {/* MANDATORY PROMINENT DISCLAIMER */}
        <div className="rounded-xl border border-blue-900/60 bg-blue-950/20 p-3.5 text-xs text-slate-300 flex items-start gap-3">
          <Info className="h-5 w-5 text-blue-400 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <p className="font-semibold text-white">
              &ldquo;This represents a reconstructed pattern, not a determination that a specific case is fraudulent.&rdquo;
            </p>
            <p className="text-[11px] text-slate-400">
              This model organizes observed assertions, urgency triggers, and withdrawal preconditions into a sequential reference timeline for consumer awareness.
            </p>
          </div>
        </div>
      </div>

      {/* 6-STAGE TIMELINE (DESKTOP & TABLET / MOBILE) */}
      <div className="space-y-4">
        {/* DESKTOP TIMELINE (6 Columns) */}
        <div className="hidden lg:grid lg:grid-cols-6 gap-3">
          {stages.map((stage) => {
            const badge = getStatusBadge(stage.status);
            const isExpanded = expandedStageId === stage.stage_id;

            return (
              <div
                key={stage.stage_id}
                onClick={() => setExpandedStageId(isExpanded ? null : stage.stage_id)}
                className={`p-4 rounded-xl border transition-all cursor-pointer flex flex-col justify-between ${
                  isExpanded
                    ? "ring-2 ring-indigo-500 border-indigo-400 bg-slate-900 shadow-xl"
                    : `${badge.border} bg-slate-900/70 hover:bg-slate-800/80`
                }`}
              >
                <div className="space-y-3">
                  {/* Top Order & Status */}
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] font-mono font-bold text-slate-500">
                      0{stage.order}
                    </span>
                    <span
                      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${badge.bg} ${badge.border}`}
                    >
                      {badge.icon}
                      <span>{badge.label}</span>
                    </span>
                  </div>

                  {/* Icon & Title */}
                  <div className="space-y-1.5">
                    <div className="p-2 w-fit rounded-lg bg-slate-800 text-indigo-400 border border-slate-700/60">
                      {renderStageIcon(stage.order, "h-4 w-4")}
                    </div>
                    <h5 className="text-xs font-bold text-white leading-tight">
                      {stage.title}
                    </h5>
                  </div>

                  {/* Summary Metric Chips */}
                  <div className="pt-2 border-t border-slate-800 text-[10px] font-mono text-slate-400 flex items-center justify-between">
                    <span>{stage.evidence_ids.length} Evidence</span>
                    <span>{stage.signal_ids.length} Signals</span>
                  </div>
                </div>

                <div className="mt-3 text-[10px] text-center font-mono text-indigo-400 hover:underline">
                  {isExpanded ? "Collapse Details" : "Expand Details"}
                </div>
              </div>
            );
          })}
        </div>

        {/* MOBILE / TABLET TIMELINE (Vertical List) */}
        <div className="block lg:hidden space-y-3">
          {stages.map((stage) => {
            const badge = getStatusBadge(stage.status);
            const isExpanded = expandedStageId === stage.stage_id;

            return (
              <div
                key={stage.stage_id}
                className={`rounded-xl border transition-all ${
                  isExpanded
                    ? "ring-2 ring-indigo-500 border-indigo-400 bg-slate-900"
                    : `${badge.border} bg-slate-900/80`
                }`}
              >
                <button
                  type="button"
                  onClick={() => setExpandedStageId(isExpanded ? null : stage.stage_id)}
                  className="w-full p-4 flex items-center justify-between text-left focus:outline-none"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-xs font-mono font-bold text-slate-500">
                      0{stage.order}
                    </span>
                    <div className="p-2 rounded-lg bg-slate-800 text-indigo-400 border border-slate-700">
                      {renderStageIcon(stage.order, "h-4 w-4")}
                    </div>
                    <div>
                      <h5 className="text-xs font-bold text-white">{stage.title}</h5>
                      <span className="text-[10px] font-mono text-slate-400">
                        {stage.evidence_ids.length} Evidence • {stage.signal_ids.length} Signals
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <span
                      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${badge.bg} ${badge.border}`}
                    >
                      {badge.icon}
                      <span>{badge.label}</span>
                    </span>
                    {isExpanded ? (
                      <ChevronUp className="h-4 w-4 text-slate-400" />
                    ) : (
                      <ChevronDown className="h-4 w-4 text-slate-400" />
                    )}
                  </div>
                </button>
              </div>
            );
          })}
        </div>
      </div>

      {/* EXPANDABLE STAGE EVIDENCE & DETAILS PANEL */}
      {(() => {
        const activeStage = stages.find((s) => s.stage_id === expandedStageId);
        if (!activeStage) return null;
        const badge = getStatusBadge(activeStage.status);

        return (
          <div className="p-5 rounded-2xl border border-indigo-900/70 bg-slate-950/95 shadow-2xl space-y-5 animate-in fade-in duration-200">
            {/* Header of Active Stage */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
              <div className="flex items-center gap-3">
                <div className="p-2.5 rounded-xl bg-indigo-950/80 border border-indigo-700/60 text-indigo-400">
                  {renderStageIcon(activeStage.order, "h-5 w-5")}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono text-slate-400">STAGE 0{activeStage.order}</span>
                    <span
                      className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-[10px] font-mono font-bold border ${badge.bg} ${badge.border}`}
                    >
                      {badge.icon}
                      <span>{badge.label}</span>
                    </span>
                  </div>
                  <h4 className="text-base font-bold text-white">{activeStage.title}</h4>
                </div>
              </div>

              <div className="flex items-center gap-2 text-xs font-mono">
                <span className="text-slate-400">CONFIDENCE:</span>
                <span className="font-bold text-white px-2 py-0.5 rounded bg-slate-900 border border-slate-800">
                  {activeStage.confidence}
                </span>
              </div>
            </div>


            {/* Why This Stage Appears */}
            <div>
              <span className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider block mb-1">
                WHY THIS STAGE APPEARS
              </span>
              <p className="text-xs text-slate-200 leading-relaxed p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                {activeStage.why_present || activeStage.description}
              </p>
            </div>

            {/* Pattern Description */}
            <div>
              <span className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider block mb-1">
                BEHAVIORAL LIFECYCLE PATTERN
              </span>
              <p className="text-xs text-slate-400 leading-relaxed font-sans">
                {activeStage.description}
              </p>
            </div>

            {/* Evidence Traceability */}
            {activeStage.evidence_ids.length > 0 && (
              <div>
                <span className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider block mb-2">
                  TRACEABLE SUPPORTING EVIDENCE ({activeStage.evidence_ids.length})
                </span>
                <div className="space-y-2">
                  {activeStage.evidence_ids.map((eid) => {
                    const evObj = evidenceList.find((e) => e.id === eid);
                    return (
                      <div
                        key={eid}
                        className="p-3.5 rounded-xl bg-slate-900/70 border border-slate-800 space-y-1 font-mono text-xs"
                      >
                        <div className="flex items-center justify-between text-[10px] text-slate-400">
                          <span className="text-indigo-400 font-bold">{eid}</span>
                          <span>{evObj?.source_type || "PAGE_TEXT"}</span>
                        </div>
                        <p className="text-slate-200 font-sans text-xs italic">
                          &ldquo;{evObj?.extracted_text || "Observed text captured during ingestion."}&rdquo;
                        </p>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Associated Risk Signals */}
            {activeStage.signal_ids.length > 0 && (
              <div>
                <span className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider block mb-1.5">
                  ASSOCIATED RISK SIGNALS ({activeStage.signal_ids.length})
                </span>
                <div className="flex flex-wrap gap-2 font-mono text-xs">
                  {activeStage.signal_ids.map((sid) => {
                    const fullSig = riskSignals.find((rs) => rs.signal_id === sid);
                    return (
                      <span
                        key={sid}
                        className="px-2.5 py-1 rounded-lg bg-rose-950/40 text-rose-300 border border-rose-800/60 text-[10px]"
                        title={fullSig?.description || sid}
                      >
                        {fullSig ? `${sid} (${fullSig.title})` : sid}
                      </span>
                    );
                  })}
                </div>

              </div>
            )}

            {/* Uncertainty Notes */}
            {activeStage.uncertainty && (
              <div className="p-3 rounded-xl bg-slate-900/40 border border-slate-800/70 text-[11px] text-slate-400 flex items-start gap-2">
                <Info className="h-4 w-4 text-slate-400 shrink-0 mt-0.5" />
                <span>
                  <strong>Uncertainty Note:</strong> {activeStage.uncertainty}
                </span>
              </div>
            )}
          </div>
        );
      })()}
    </div>
  );
}
