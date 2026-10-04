"use client";

import * as React from "react";
import { WebsiteAnalysisData, VerificationResult, RiskSignalItem } from "@/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { TrustChainVisualizer } from "@/components/trust-chain/TrustChainVisualizer";
import { ScamJourneyTimeline } from "@/components/scam-journey/ScamJourneyTimeline";
import { SafeResponseSection } from "@/components/analysis/SafeResponseSection";
import { TrustBreakpointCard } from "@/components/analysis/TrustBreakpointCard";
import { computeTrustBreakpoint } from "@/lib/trustBreakpoint";
import { useLanguage } from "@/lib/i18n";
import {
  Globe,
  FileText,
  ShieldAlert,
  CheckCircle2,
  AlertCircle,
  Clock,
  Award,
  Network,
  AlertTriangle,
  HelpCircle,
  ExternalLink,
  WifiOff,
  ChevronDown,
  ChevronUp,
  ShieldQuestion,
  ArrowRight,
  Sparkles,
  ShieldCheck,
  Compass,
  MessageSquare,
  Image as ImageIcon,
} from "lucide-react";

interface WebsiteAnalysisResultProps {
  data: WebsiteAnalysisData;
}

type TabType =
  | "overview"
  | "safe_response"
  | "trust_chain"
  | "scam_journey"
  | "signals"
  | "verification"
  | "claims"
  | "entities"
  | "regulatory"
  | "financial"
  | "relationships"
  | "evidence"
  | "links";


function getStatusBadge(status?: string, isDemo?: boolean) {

  const normStatus = (status || "UNKNOWN").toUpperCase();

  let bgClass = "bg-amber-950/80 text-amber-300 border-amber-700/60";
  let icon = <HelpCircle className="h-3.5 w-3.5 text-amber-400" />;

  if (normStatus === "VERIFIED") {
    bgClass = "bg-emerald-950/80 text-emerald-300 border-emerald-600/70";
    icon = <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" />;
  } else if (normStatus === "CONTRADICTORY") {
    bgClass = "bg-rose-950/80 text-rose-300 border-rose-600/70";
    icon = <AlertTriangle className="h-3.5 w-3.5 text-rose-400" />;
  } else if (normStatus === "NOT_FOUND") {
    bgClass = "bg-slate-900 text-slate-300 border-slate-700";
    icon = <AlertCircle className="h-3.5 w-3.5 text-slate-400" />;
  } else if (normStatus === "UNAVAILABLE") {
    bgClass = "bg-purple-950/80 text-purple-300 border-purple-700/60";
    icon = <WifiOff className="h-3.5 w-3.5 text-purple-400" />;
  }

  return (
    <div className="flex flex-wrap items-center gap-1.5">
      <span
        className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded text-xs font-mono font-bold border ${bgClass}`}
      >
        {icon}
        <span>VERIFICATION: {normStatus}</span>
      </span>
      {isDemo && (
        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-950/90 text-amber-300 border border-amber-600/80 uppercase">
          DEMO VERIFICATION
        </span>
      )}
    </div>
  );
}

function getConcernBadge(level?: string) {
  const norm = (level || "INSUFFICIENT_EVIDENCE").toUpperCase();
  if (norm === "HIGH_CONCERN") {
    return {
      title: "HIGH CONCERN",
      border: "border-rose-600/80",
      bg: "bg-rose-950/30",
      badgeClass: "bg-rose-950 text-rose-300 border-rose-600",
      icon: <ShieldAlert className="h-5 w-5 text-rose-400" />,
      sub: "Multiple significant evidence-backed concerns identified",
    };
  }
  if (norm === "MODERATE_CONCERN") {
    return {
      title: "MODERATE CONCERN",
      border: "border-amber-600/80",
      bg: "bg-amber-950/30",
      badgeClass: "bg-amber-950 text-amber-300 border-amber-600",
      icon: <AlertTriangle className="h-5 w-5 text-amber-400" />,
      sub: "Unverified regulatory claims or high-pressure language require validation",
    };
  }
  if (norm === "LOW_CONCERN") {
    return {
      title: "LOW CONCERN",
      border: "border-emerald-600/80",
      bg: "bg-emerald-950/30",
      badgeClass: "bg-emerald-950 text-emerald-300 border-emerald-600",
      icon: <CheckCircle2 className="h-5 w-5 text-emerald-400" />,
      sub: "No critical contradictions or high-pressure signals detected",
    };
  }
  return {
    title: "INSUFFICIENT EVIDENCE",
    border: "border-slate-700",
    bg: "bg-slate-900/60",
    badgeClass: "bg-slate-900 text-slate-300 border-slate-700",
    icon: <ShieldQuestion className="h-5 w-5 text-slate-400" />,
    sub: "Limited public evidence was available to evaluate concern level",
  };
}

export function WebsiteAnalysisResult({ data }: WebsiteAnalysisResultProps) {
  const { t } = useLanguage();
  const [activeTab, setActiveTab] = React.useState<TabType>("trust_chain");


  const [expandedSignals, setExpandedSignals] = React.useState<Record<string, boolean>>({});
  const [selectedClaimId, setSelectedClaimId] = React.useState<string | null>(null);

  const entities = data.entities || [];
  const claims = React.useMemo(() => data.claims || [], [data.claims]);
  const regulatoryRefs = data.regulatory_references || [];
  const financialClaims = data.financial_claims || [];
  const relationships = data.identity_relationships || [];
  const evidenceList = data.evidence || [];
  const verificationResults = data.verification_results || [];
  const riskSignals = data.risk_signals || data.assessment?.risk_signals || [];
  const assessment = data.assessment;
  const evSummary = data.evidence_summary;

  const concernInfo = getConcernBadge(assessment?.overall_level);

  const trustBreakpoint = React.useMemo(() => {
    return computeTrustBreakpoint(data);
  }, [data]);

  const activeSelectedClaim = React.useMemo(() => {
    if (selectedClaimId) {
      return claims.find((c) => c.id === selectedClaimId) || claims[0] || null;
    }
    return claims[0] || null;
  }, [claims, selectedClaimId]);

  const toggleSignal = (sigId: string) => {
    setExpandedSignals((prev) => ({ ...prev, [sigId]: !prev[sigId] }));
  };

  const inputMode = (data.input.input_type || "URL").toUpperCase();
  const isMessage = inputMode === "MESSAGE";
  const isScreenshot = inputMode === "SCREENSHOT";
  const titleText = isMessage
    ? "Financial Message Analysis"
    : isScreenshot
    ? "Screenshot OCR Analysis"
    : "Website Analysis";
  const sourceLabel = isMessage
    ? "Analysis Source: USER SUBMITTED MESSAGE"
    : isScreenshot
    ? "Analysis Source: SCREENSHOT OCR"
    : "Analysis Source: WEBSITE URL";
  const targetLabel = isMessage
    ? `Submitted Excerpt: "${(data.page.text_excerpt || "").slice(0, 80)}..."`
    : isScreenshot
    ? `OCR Target: "${(data.page.text_excerpt || "Screenshot Optical Text").slice(0, 80)}..."`
    : `Target: ${data.input.normalized_url}`;

  return (
    <section id="website-analysis" className="py-12 scroll-mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
        {/* Section Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-5 rounded-xl border border-blue-900/50 bg-slate-900/90 shadow-xl backdrop-blur-md">
          <div className="space-y-1">
            <div className="flex items-center gap-2.5">
              <div className="h-8 w-8 rounded-lg bg-blue-600/20 border border-blue-500/40 flex items-center justify-center text-blue-400">
                {isMessage ? (
                  <MessageSquare className="h-4 w-4" />
                ) : isScreenshot ? (
                  <ImageIcon className="h-4 w-4" />
                ) : (
                  <Globe className="h-4 w-4" />
                )}
              </div>
              <h3 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
                {titleText}
              </h3>
              <span className="px-2.5 py-0.5 rounded text-xs font-mono font-bold bg-blue-950 text-blue-300 border border-blue-600/50">
                {sourceLabel}
              </span>
            </div>
            <p className="text-xs text-slate-400 font-mono">
              <span className="text-slate-200">{targetLabel}</span>
            </p>
          </div>

          <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-emerald-950/70 border border-emerald-600/60 text-emerald-300 font-mono text-xs font-bold uppercase tracking-wider">
            <CheckCircle2 className="h-4 w-4 text-emerald-400" />
            <span>{data.analysis_metadata.status || "ANALYSIS COMPLETE"}</span>
          </div>
        </div>

        {/* OCR Uncertainty Alert Notice if present */}
        {data.analysis_metadata.ocr_uncertainty_note && (
          <div className="p-4 rounded-xl border border-amber-800/60 bg-amber-950/40 text-amber-200 text-xs font-mono flex items-start gap-3 shadow-lg">
            <AlertTriangle className="h-5 w-5 text-amber-400 shrink-0 mt-0.5" />
            <div className="space-y-1">
              <span className="font-bold text-amber-300 block uppercase tracking-wider">
                OCR Uncertainty Notice
              </span>
              <p>{data.analysis_metadata.ocr_uncertainty_note}</p>
            </div>
          </div>
        )}

        {/* PROMINENT PHASE 5 EVIDENCE-BACKED ASSESSMENT CARD */}
        {assessment && (
          <div
            className={`p-6 sm:p-7 rounded-2xl border ${concernInfo.border} ${concernInfo.bg} shadow-2xl space-y-6 backdrop-blur-md`}
          >
            {/* Top Level Summary Banner */}
            <div className="flex flex-col md:flex-row md:items-start justify-between gap-5 border-b border-slate-800/80 pb-5">
              <div className="space-y-2.5 max-w-2xl">
                <div className="flex items-center gap-3">
                  <span
                    className={`inline-flex items-center gap-2 px-3 py-1 rounded-lg font-mono text-xs font-bold uppercase tracking-wider border ${concernInfo.badgeClass}`}
                  >
                    {concernInfo.icon}
                    <span>{concernInfo.title}</span>
                  </span>
                  <span className="text-xs font-mono text-slate-400">
                    Evidence-Backed Synthesis
                  </span>
                </div>
                <h4 className="text-xl sm:text-2xl font-bold text-white tracking-tight leading-snug">
                  {assessment.summary}
                </h4>
                <p className="text-xs sm:text-sm text-slate-300">{concernInfo.sub}</p>

                {/* Detected Risk Signal Pills */}
                {riskSignals.length > 0 && (
                  <div className="flex flex-wrap gap-2 pt-2">
                    {riskSignals.map((sig: RiskSignalItem) => (
                      <span
                        key={sig.signal_id}
                        className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-mono font-semibold border ${
                          sig.severity === "HIGH"
                            ? "bg-rose-950/80 border-rose-800/80 text-rose-300"
                            : sig.severity === "MEDIUM"
                            ? "bg-amber-950/80 border-amber-800/80 text-amber-300"
                            : "bg-blue-950/80 border-blue-800/80 text-blue-300"
                        }`}
                      >
                        <span className={`h-1.5 w-1.5 rounded-full ${
                          sig.severity === "HIGH" ? "bg-rose-400" : sig.severity === "MEDIUM" ? "bg-amber-400" : "bg-blue-400"
                        }`} />
                        {sig.title}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {/* Evidence Metrics Pill */}
              <div className="flex items-center gap-4 bg-slate-950/80 p-4 rounded-xl border border-slate-800 text-xs font-mono shrink-0 self-start">
                <div>
                  <span className="text-slate-500 block text-[10px]">RISK SIGNALS</span>
                  <span className="text-rose-400 font-bold text-base">{riskSignals.length} Detected</span>
                </div>
                <div className="border-l border-slate-800 pl-4">
                  <span className="text-slate-500 block text-[10px]">EVIDENCE COUNT</span>
                  <span className="text-amber-400 font-bold text-base">
                    {evSummary ? evSummary.total_evidence_count : assessment.evidence_count} Objects
                  </span>
                </div>
              </div>
            </div>

            {/* Prominent 'WHY THIS WAS FLAGGED' Section */}
            {riskSignals.length > 0 && (
              <div className="space-y-3.5">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono uppercase tracking-wider text-slate-300 font-bold flex items-center gap-2">
                    <AlertTriangle className="h-4 w-4 text-rose-400" />
                    <span>WHY THIS WAS FLAGGED</span>
                  </span>
                  <span className="text-[11px] font-mono text-slate-400">
                    Concrete risk signals from observed content
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                  {riskSignals.map((sig: RiskSignalItem) => (
                    <div
                      key={sig.signal_id}
                      className={`p-4 rounded-xl bg-slate-950/90 border flex flex-col justify-between space-y-2.5 transition-all ${
                        sig.severity === "HIGH"
                          ? "border-rose-900/60 hover:border-rose-700/80"
                          : sig.severity === "MEDIUM"
                          ? "border-amber-900/60 hover:border-amber-700/80"
                          : "border-slate-800 hover:border-slate-700"
                      }`}
                    >
                      <div className="space-y-1.5">
                        <div className="flex items-center justify-between gap-2">
                          <span
                            className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border ${
                              sig.severity === "HIGH"
                                ? "bg-rose-950 text-rose-300 border-rose-700"
                                : sig.severity === "MEDIUM"
                                ? "bg-amber-950 text-amber-300 border-amber-700"
                                : "bg-blue-950 text-blue-300 border-blue-700"
                            }`}
                          >
                            {sig.severity} RISK • {sig.category}
                          </span>
                          <span className="text-[10px] font-mono text-slate-500">
                            Confidence: {sig.confidence}
                          </span>
                        </div>
                        <h5 className="text-sm font-bold text-white flex items-center gap-2">
                          <AlertTriangle className="h-3.5 w-3.5 text-rose-400 shrink-0" />
                          <span>{sig.title}</span>
                        </h5>
                        <p className="text-xs text-slate-300 leading-snug">
                          {sig.description}
                        </p>
                      </div>

                      {sig.explanation && (
                        <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800/80 text-[11px] text-slate-300">
                          <strong className="text-slate-400 block font-mono text-[10px] uppercase">Why flagged:</strong>
                          {sig.explanation}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Evidence Distinction Snapshot Bar (OBSERVED vs VERIFIED) */}
            <div className="space-y-2">
              <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-mono">
                <div>
                  <span className="text-slate-500 text-[10px] block">TOTAL EVIDENCE (OBSERVED)</span>
                  <span className="text-white font-bold text-sm">{evSummary?.total_evidence_count || assessment.evidence_count} Items</span>
                </div>
                <div>
                  <span className="text-slate-500 text-[10px] block">REGULATORY CLAIMS (VERIFIED)</span>
                  <span className="text-emerald-400 font-bold text-sm">{evSummary?.verified_claims ?? assessment.verified_claim_count}</span>
                </div>
                <div>
                  <span className="text-slate-500 text-[10px] block">CONTRADICTORY (MISMATCH)</span>
                  <span className="text-rose-400 font-bold text-sm">{evSummary?.contradictory_claims ?? assessment.contradictory_claim_count}</span>
                </div>
                <div>
                  <span className="text-slate-500 text-[10px] block">UNVERIFIED / UNKNOWN</span>
                  <span className="text-amber-400 font-bold text-sm">
                    {(evSummary?.unverified_claims ?? assessment.unverified_claim_count) + (evSummary?.unknown_claims ?? assessment.unknown_claim_count)}
                  </span>
                </div>
              </div>
              <p className="text-[10px] text-slate-500 italic pl-1">
                *Status Policy: NOT_FOUND does not imply deliberate fraud, and UNAVAILABLE denotes an unreachable registry endpoint rather than an absent record.
              </p>
            </div>

            {/* PHASE 6 & 7 DYNAMIC OVERVIEW INTEGRATION WIDGETS */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* TRUST CHAIN SUMMARY CARD */}
              <div className="p-4 rounded-xl bg-slate-950/80 border border-blue-900/60 space-y-2.5">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <ShieldCheck className="h-4 w-4 text-blue-400" />
                    <span className="text-xs font-mono font-bold text-white uppercase tracking-wider">
                      TRUST CHAIN SUMMARY
                    </span>
                  </div>
                  <button
                    type="button"
                    onClick={() => setActiveTab("trust_chain")}
                    className="text-[11px] font-mono text-blue-400 hover:text-blue-300 hover:underline flex items-center gap-1"
                  >
                    <span>View Chain</span>
                    <ArrowRight className="h-3 w-3" />
                  </button>
                </div>

                <div className="flex flex-wrap gap-2 text-xs font-mono">
                  <span className="px-2.5 py-1 rounded-lg bg-emerald-950/70 border border-emerald-800 text-emerald-300 font-semibold">
                    {data.trust_chain?.summary?.verified_count ?? (data.trust_chain?.relationships.filter(r => r.status === "VERIFIED").length || 0)} Verified
                  </span>
                  <span className="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-700 text-slate-300">
                    {data.trust_chain?.summary?.unknown_count ?? (data.trust_chain?.relationships.filter(r => r.status === "UNKNOWN").length || 0)} Unknown
                  </span>
                  <span className="px-2.5 py-1 rounded-lg bg-rose-950/70 border border-rose-800 text-rose-300 font-semibold">
                    {data.trust_chain?.summary?.contradictory_count ?? (data.trust_chain?.relationships.filter(r => r.status === "CONTRADICTORY").length || 0)} Contradictory
                  </span>
                  <span className="px-2.5 py-1 rounded-lg bg-slate-900/80 border border-slate-800 text-slate-400">
                    {data.trust_chain?.summary?.unobserved_count ?? (data.trust_chain?.relationships.filter(r => r.status === "NOT_OBSERVED").length || 0)} Unobserved
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 leading-snug">
                  Provenance chain rigorously evaluated across claimed identities, official regulatory registers, websites, and settlement vectors.
                </p>
              </div>

              {/* POSSIBLE SCAM JOURNEY RECONSTRUCTION CARD */}
              <div className="p-4 rounded-xl bg-slate-950/80 border border-indigo-900/60 space-y-2.5">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Compass className="h-4 w-4 text-indigo-400" />
                    <span className="text-xs font-mono font-bold text-white uppercase tracking-wider">
                      POSSIBLE JOURNEY
                    </span>
                  </div>
                  <button
                    type="button"
                    onClick={() => setActiveTab("scam_journey")}
                    className="text-[11px] font-mono text-indigo-400 hover:text-indigo-300 hover:underline flex items-center gap-1"
                  >
                    <span>View Journey</span>
                    <ArrowRight className="h-3 w-3" />
                  </button>
                </div>

                <div className="flex items-center gap-3">
                  <span className="text-sm font-bold text-indigo-300 font-mono">
                    {data.scam_journey
                      ? `${data.scam_journey.stages.filter(s => s.status === "OBSERVED" || s.status === "SUSPECTED").length} of ${data.scam_journey.stages.length} stages supported by available evidence.`
                      : "Evidence-backed multi-stage pattern reconstruction available."}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 leading-snug">
                  Behavioral pattern synthesizing observed claims, communication points, deposit mandates, and withdrawal restrictions.
                </p>
              </div>
            </div>


            {/* Safe Next Steps Box */}
            {assessment.safe_next_steps && assessment.safe_next_steps.length > 0 && (
              <div className="p-4 rounded-xl bg-slate-950/70 border border-blue-900/40 space-y-2">
                <div className="flex items-center gap-2 text-xs font-bold text-blue-300 font-mono uppercase tracking-wider">
                  <ArrowRight className="h-4 w-4 text-blue-400" />
                  <span>Recommended Safe Next Steps</span>
                </div>
                <ul className="space-y-1 text-xs text-slate-300">
                  {assessment.safe_next_steps.map((step, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-blue-400 font-bold">•</span>
                      <span>{step}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Mandatory Non-Prejudicial Legal Disclaimer */}
            <div className="text-[11px] text-slate-400 italic bg-slate-950/50 p-3 rounded-lg border border-slate-800/60">
              <strong>Assessment Disclaimer:</strong> This assessment highlights observable risk signals, linguistic patterns, and regulatory verification gaps. It does <strong>NOT</strong> constitute a legal determination that a person, company, website, or investment opportunity is fraudulent.
            </div>
          </div>
        )}

        {/* SIGNATURE TRACK A FEATURE: TRUST BREAKPOINT / WHERE SHOULD I STOP? */}
        <div id="trust-breakpoint-section">
          <TrustBreakpointCard
            breakpoint={trustBreakpoint}
            onViewEvidence={() => {
              setActiveTab("evidence");
              const el = document.getElementById("detailed-inspection-card");
              if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
            }}
          />
        </div>

        {/* PHASE 9 & 10 SAFE RESPONSE & RECOVERY GUIDANCE */}
        <SafeResponseSection
          safeResponse={data.safe_response}
          recoveryGuidance={data.recovery_guidance}
          targetArtifact={targetLabel}
        />

        {/* Tabbed Intelligence & Breakdown Card */}
        {data.fetch.success && (
          <Card id="detailed-inspection-card" className="border-slate-800 bg-slate-900/90 shadow-xl overflow-hidden scroll-mt-20">
            <CardHeader className="pb-3 border-b border-slate-800">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div className="flex items-center gap-2">
                  <FileText className="h-4 w-4 text-blue-400" />
                  <CardTitle className="text-base font-bold text-white">
                    Detailed Signal & Evidence Inspection
                  </CardTitle>
                </div>
                <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
                  <Clock className="h-3.5 w-3.5" />
                  <span>{data.fetch.response_time_ms ? `${data.fetch.response_time_ms} ms` : "Instant"}</span>
                  <span>•</span>
                  <span>{data.fetch.redirect_hops} hop(s)</span>
                </div>
              </div>
            </CardHeader>

            <CardContent className="p-5 space-y-5">
              {/* Tab Navigation */}
              <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-3">
                <button
                  type="button"
                  onClick={() => setActiveTab("safe_response")}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
                    activeTab === "safe_response"
                      ? "bg-amber-600 text-white shadow-md shadow-amber-600/30"
                      : "bg-slate-800/80 text-amber-300 hover:bg-slate-800 border border-amber-900/40"
                  }`}
                  id="tab-btn-safe-response"
                >
                  <ShieldAlert className="h-3.5 w-3.5" />
                  <span>{t.safeResponseTitle}</span>
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab("trust_chain")}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
                    activeTab === "trust_chain"
                      ? "bg-blue-600 text-white shadow-md shadow-blue-600/30"
                      : "bg-slate-800/80 text-blue-300 hover:bg-slate-800 border border-blue-900/40"
                  }`}
                >
                  <ShieldCheck className="h-3.5 w-3.5" />

                  <span>Financial Trust Chain</span>
                  <span className="px-1.5 py-0.2 rounded text-[10px] font-mono bg-blue-950 text-blue-200 border border-blue-700/60">
                    {data.trust_chain?.relationships.length || 7}
                  </span>
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab("scam_journey")}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
                    activeTab === "scam_journey"
                      ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/30"
                      : "bg-slate-800/80 text-indigo-300 hover:bg-slate-800 border border-indigo-900/40"
                  }`}
                >
                  <Sparkles className="h-3.5 w-3.5" />
                  <span>Scam Journey Pattern</span>
                  <span className="px-1.5 py-0.2 rounded text-[10px] font-mono bg-indigo-950 text-indigo-200 border border-indigo-700/60">
                    6 Stages
                  </span>
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab("signals")}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    activeTab === "signals"
                      ? "bg-rose-600 text-white shadow-sm"
                      : "bg-slate-800/60 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  Risk Signals ({riskSignals.length})
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab("verification")}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    activeTab === "verification"
                      ? "bg-emerald-600 text-white shadow-sm"
                      : "bg-slate-800/60 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  Verification ({verificationResults.length})
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab("claims")}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    activeTab === "claims"
                      ? "bg-blue-600 text-white shadow-sm"
                      : "bg-slate-800/60 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  Claims ({claims.length})
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab("entities")}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    activeTab === "entities"
                      ? "bg-blue-600 text-white shadow-sm"
                      : "bg-slate-800/60 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  Entities ({entities.length})
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab("regulatory")}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    activeTab === "regulatory"
                      ? "bg-blue-600 text-white shadow-sm"
                      : "bg-slate-800/60 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  Regulatory ({regulatoryRefs.length})
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab("financial")}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    activeTab === "financial"
                      ? "bg-blue-600 text-white shadow-sm"
                      : "bg-slate-800/60 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  Financial Language ({financialClaims.length})
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab("relationships")}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    activeTab === "relationships"
                      ? "bg-blue-600 text-white shadow-sm"
                      : "bg-slate-800/60 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  Relationships ({relationships.length})
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab("evidence")}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    activeTab === "evidence"
                      ? "bg-blue-600 text-white shadow-sm"
                      : "bg-slate-800/60 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  Evidence Objects ({evidenceList.length})
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab("links")}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    activeTab === "links"
                      ? "bg-blue-600 text-white shadow-sm"
                      : "bg-slate-800/60 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  Links ({data.links.length})
                </button>
              </div>

              {/* TAB: SAFE RESPONSE & RECOVERY (PHASE 9 & 10) */}
              {activeTab === "safe_response" && (
                <div className="space-y-4">
                  <SafeResponseSection
                    safeResponse={data.safe_response}
                    recoveryGuidance={data.recovery_guidance}
                    targetArtifact={targetLabel}
                  />
                </div>
              )}

              {/* TAB: FINANCIAL TRUST CHAIN (PHASE 6) */}
              {activeTab === "trust_chain" && (

                <div className="space-y-4">
                  <TrustChainVisualizer
                    graph={data.trust_chain}
                    evidenceList={evidenceList}
                    verificationResults={verificationResults}
                  />
                </div>
              )}

              {/* TAB: SCAM JOURNEY PATTERN (PHASE 7) */}
              {activeTab === "scam_journey" && (
                <div className="space-y-4">
                  <ScamJourneyTimeline
                    journey={data.scam_journey}
                    evidenceList={evidenceList}
                    riskSignals={riskSignals}
                  />
                </div>
              )}

              {/* TAB: RISK SIGNALS (EXPANDABLE WHY WAS THIS FLAGGED?) */}
              {activeTab === "signals" && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span>Evidence-Backed Deduplicated Risk Signals</span>
                    <span className="font-mono text-rose-400 text-[11px]">
                      {riskSignals.length} Signals Evaluated
                    </span>
                  </div>

                  {riskSignals.length === 0 ? (
                    <div className="p-6 rounded-xl bg-slate-950/60 border border-slate-800 text-center space-y-2">
                      <CheckCircle2 className="h-8 w-8 text-emerald-400 mx-auto" />
                      <p className="text-xs text-slate-300 font-medium">
                        No critical risk signals triggered by public webpage content.
                      </p>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {riskSignals.map((sig: RiskSignalItem) => {
                        const isExpanded = !!expandedSignals[sig.signal_id];
                        return (
                          <div
                            key={sig.signal_id}
                            className={`rounded-xl border transition-all ${
                              sig.severity === "HIGH"
                                ? "bg-slate-950/90 border-rose-900/60"
                                : sig.severity === "MEDIUM"
                                ? "bg-slate-950/80 border-amber-900/50"
                                : "bg-slate-950/70 border-slate-800"
                            }`}
                          >
                            {/* Signal Card Header / Collapsible trigger */}
                            <button
                              type="button"
                              onClick={() => toggleSignal(sig.signal_id)}
                              className="w-full p-4 flex items-start justify-between gap-3 text-left"
                            >
                              <div className="space-y-1.5">
                                <div className="flex flex-wrap items-center gap-2">
                                  <span
                                    className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border ${
                                      sig.severity === "HIGH"
                                        ? "bg-rose-950 text-rose-300 border-rose-700"
                                        : sig.severity === "MEDIUM"
                                        ? "bg-amber-950 text-amber-300 border-amber-700"
                                        : "bg-blue-950 text-blue-300 border-blue-700"
                                    }`}
                                  >
                                    {sig.category} • {sig.severity}
                                  </span>
                                  <span className="text-[10px] font-mono text-slate-500">
                                    Confidence: {sig.confidence}
                                  </span>
                                </div>
                                <h5 className="text-sm font-bold text-white">{sig.title}</h5>
                                <p className="text-xs text-slate-300">{sig.description}</p>
                              </div>

                              <div className="flex items-center gap-2 shrink-0 pt-1 text-slate-400">
                                <span className="text-[11px] font-mono hidden sm:inline">
                                  {isExpanded ? "Collapse" : "Why was this flagged?"}
                                </span>
                                {isExpanded ? (
                                  <ChevronUp className="h-4 w-4" />
                                ) : (
                                  <ChevronDown className="h-4 w-4" />
                                )}
                              </div>
                            </button>

                            {/* Expanded Details: Signal -> Why -> Evidence -> Source -> Uncertainty */}
                            {isExpanded && (
                              <div className="p-4 pt-0 border-t border-slate-800/60 space-y-3 text-xs">
                                {/* Why */}
                                <div className="space-y-1 bg-slate-900/70 p-3 rounded-lg border border-slate-800">
                                  <span className="text-slate-400 font-mono uppercase text-[10px] block font-bold">
                                    WHY WAS THIS FLAGGED?
                                  </span>
                                  <p className="text-slate-200 leading-relaxed">{sig.explanation}</p>
                                </div>

                                {/* Supporting Evidence */}
                                {sig.evidence_ids && sig.evidence_ids.length > 0 && (
                                  <div className="space-y-1 bg-slate-900/50 p-3 rounded-lg border border-slate-800">
                                    <span className="text-slate-400 font-mono uppercase text-[10px] block font-bold">
                                      LINKED EVIDENCE OBJECTS ({sig.evidence_ids.length})
                                    </span>
                                    <div className="flex flex-wrap gap-1.5 font-mono text-[11px] text-amber-300">
                                      {sig.evidence_ids.map((eid) => (
                                        <span key={eid} className="px-2 py-0.5 rounded bg-slate-950 border border-slate-800">
                                          {eid}
                                        </span>
                                      ))}
                                    </div>
                                  </div>
                                )}

                                {/* Uncertainty / Caveats */}
                                {sig.uncertainty && (
                                  <div className="space-y-1 bg-slate-900/40 p-3 rounded-lg border border-slate-800 text-slate-400 italic">
                                    <span className="text-slate-400 font-mono uppercase text-[10px] block font-bold not-italic">
                                      UNCERTAINTY & LIMITATIONS
                                    </span>
                                    <p>{sig.uncertainty}</p>
                                  </div>
                                )}

                                <div className="flex items-center justify-between text-[10px] font-mono text-slate-500 pt-1">
                                  <span>Signal ID: {sig.signal_id}</span>
                                  <span>Source: {sig.source}</span>
                                </div>
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>
              )}

              {/* TAB: AUTHORITATIVE VERIFICATION RESULTS */}
              {activeTab === "verification" && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span>Authoritative Registry Query Inquiries & Verification Outcomes</span>
                    <span className="font-mono text-emerald-400 text-[11px]">
                      {verificationResults.length} Inquiries Evaluated
                    </span>
                  </div>

                  {verificationResults.length === 0 ? (
                    <div className="p-6 rounded-xl bg-slate-950/60 border border-slate-800 text-center space-y-2">
                      <HelpCircle className="h-8 w-8 text-slate-500 mx-auto" />
                      <p className="text-xs text-slate-400 font-medium">
                        No statutory claims with verifiable registration numbers were present to query.
                      </p>
                    </div>
                  ) : (
                    <div className="space-y-3.5">
                      {verificationResults.map((vRes: VerificationResult) => (
                        <div
                          key={vRes.id}
                          className={`p-4 rounded-xl border space-y-3 ${
                            vRes.status === "VERIFIED"
                              ? "bg-slate-950/80 border-emerald-900/50"
                              : vRes.status === "CONTRADICTORY"
                              ? "bg-rose-950/20 border-rose-900/60"
                              : vRes.status === "UNAVAILABLE"
                              ? "bg-purple-950/20 border-purple-900/50"
                              : "bg-slate-950/70 border-slate-800"
                          }`}
                        >
                          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/70 pb-2.5">
                            <div className="flex items-center gap-2">
                              {getStatusBadge(vRes.status, vRes.is_demo)}
                            </div>
                            <span className="text-[11px] font-mono text-slate-400">
                              Checked: {new Date(vRes.checked_at).toLocaleTimeString()} UTC
                            </span>
                          </div>

                          {vRes.is_demo && (
                            <div className="p-2.5 rounded-lg bg-amber-950/30 border border-amber-800/50 text-[11px] text-amber-200/90 font-mono">
                              ⚠️ <strong>DEMO VERIFICATION:</strong> Derived from synthetic test database records for architectural evaluation. Does not represent a live regulator confirmation.
                            </div>
                          )}

                          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                            <div className="space-y-1">
                              <span className="text-slate-400 font-mono uppercase text-[10px] block">
                                Authoritative Source
                              </span>
                              <div className="flex items-center gap-1.5 text-white font-medium">
                                <span>{vRes.source_name}</span>
                                {vRes.source_url && (
                                  <a
                                    href={vRes.source_url}
                                    target="_blank"
                                    rel="noreferrer"
                                    className="text-blue-400 hover:text-blue-300 inline-flex items-center"
                                  >
                                    <ExternalLink className="h-3 w-3" />
                                  </a>
                                )}
                              </div>
                            </div>

                            <div className="space-y-1">
                              <span className="text-slate-400 font-mono uppercase text-[10px] block">
                                Matched Registry Record
                              </span>
                              <p className="text-slate-200 font-mono">
                                {vRes.matched_registration ? (
                                  <>
                                    <span className="text-amber-300 font-bold">{vRes.matched_registration}</span>
                                    {vRes.matched_entity && (
                                      <span className="text-slate-400 font-sans ml-1.5">({vRes.matched_entity})</span>
                                    )}
                                  </>
                                ) : (
                                  <span className="text-slate-500 italic">None matched</span>
                                )}
                              </p>
                            </div>
                          </div>

                          <div className="space-y-1 text-xs bg-slate-900/60 p-3 rounded-lg border border-slate-800/70">
                            <span className="text-slate-400 font-mono uppercase text-[10px] block font-bold">
                              Why This Status:
                            </span>
                            <p className="text-slate-200 leading-relaxed font-sans">{vRes.reason}</p>
                          </div>

                          <div className="space-y-1 text-xs bg-slate-900/40 p-3 rounded-lg border border-slate-800/50">
                            <span className="text-slate-400 font-mono uppercase text-[10px] block font-bold">
                              Verification Evidence:
                            </span>
                            <p className="text-slate-300 font-mono text-[11px] leading-relaxed">{vRes.evidence}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* TAB: CLAIMS */}
              {activeTab === "claims" && (
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span>Observed Claims with Verification Linkage</span>
                    <span className="font-mono text-slate-400 text-[11px]">{claims.length} Claims</span>
                  </div>

                  {/* CLAIM -> EVIDENCE SPOTLIGHT CARD */}
                  {activeSelectedClaim && (
                    <div className="p-5 rounded-2xl border border-cyan-500/40 bg-gradient-to-br from-cyan-950/30 via-slate-900/90 to-slate-950/95 space-y-4 shadow-xl shadow-cyan-950/20">
                      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-cyan-900/40 pb-3">
                        <div className="flex items-center gap-2">
                          <span className="h-2 w-2 rounded-full bg-cyan-400 animate-pulse" />
                          <span className="text-xs font-mono font-bold tracking-wider uppercase text-cyan-300">
                            {t.claimSpotlightTitle}
                          </span>
                        </div>
                        <span className="text-[11px] font-mono text-slate-400">
                          {t.claimSpotlightSelectPrompt}
                        </span>
                      </div>

                      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                        {/* Left: Claim & Source & Observation */}
                        <div className="space-y-3">
                          <div className="space-y-1">
                            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 font-bold">
                              CLAIM
                            </span>
                            <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-sm font-semibold text-white">
                              &ldquo;{activeSelectedClaim.claim_text}&rdquo;
                            </div>
                          </div>

                          <div className="grid grid-cols-2 gap-2 text-xs">
                            <div className="p-2.5 rounded-lg bg-slate-950/50 border border-slate-800/80 space-y-0.5">
                              <span className="text-[10px] font-mono text-slate-400 uppercase font-bold">
                                {t.claimSpotlightSource}
                              </span>
                              <p className="text-slate-300 font-mono text-[11px] truncate">
                                {isMessage ? "User-submitted message" : isScreenshot ? "Screenshot OCR" : "Website content"}
                              </p>
                            </div>

                            <div className="p-2.5 rounded-lg bg-slate-950/50 border border-slate-800/80 space-y-0.5">
                              <span className="text-[10px] font-mono text-slate-400 uppercase font-bold">
                                CLAIM TYPE
                              </span>
                              <p className="text-cyan-300 font-mono text-[11px]">
                                {activeSelectedClaim.claim_type}
                              </p>
                            </div>
                          </div>

                          <div className="space-y-1">
                            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 font-bold">
                              {t.claimSpotlightObservation}
                            </span>
                            <p className="text-xs text-slate-300 bg-slate-950/50 p-2.5 rounded-lg border border-slate-800/80 leading-relaxed">
                              {activeSelectedClaim.claim_type === "REGULATORY" || /sebi|rbi|mca/i.test(activeSelectedClaim.claim_text)
                                ? "The message claims regulatory approval. Regulatory authority claims should always be checked against authoritative sources before sending money."
                                : activeSelectedClaim.claim_type === "FINANCIAL" || /guarantee|25%|return/i.test(activeSelectedClaim.claim_text)
                                ? "The message promises specific high-yield or guaranteed returns with zero risk."
                                : activeSelectedClaim.evidence_text || "Observed directly in submitted input."}
                            </p>
                          </div>
                        </div>

                        {/* Right: Verification Status & Why It Matters */}
                        <div className="space-y-3 flex flex-col justify-between">
                          <div className="space-y-3">
                            <div className="space-y-1">
                              <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 font-bold">
                                {t.claimSpotlightVerification}
                              </span>
                              <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
                                {getStatusBadge(
                                  activeSelectedClaim.verification?.status || activeSelectedClaim.verification_status,
                                  activeSelectedClaim.verification?.is_demo
                                )}
                                {activeSelectedClaim.verification?.reason && (
                                  <p className="text-xs text-slate-300 leading-relaxed">
                                    {activeSelectedClaim.verification.reason}
                                  </p>
                                )}
                              </div>
                            </div>

                            <div className="space-y-1">
                              <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 font-bold">
                                {t.claimSpotlightWhyItMatters}
                              </span>
                              <p className="text-xs text-amber-200/90 bg-amber-950/20 p-2.5 rounded-lg border border-amber-900/40 leading-relaxed">
                                Regulatory authority claims should be verified against authoritative public records before sending money. RakshaScan separates observed claims from authoritative verification.
                              </p>
                            </div>
                          </div>

                          <div className="pt-2 flex items-center justify-end">
                            <button
                              type="button"
                              onClick={() => {
                                setActiveTab("evidence");
                                const el = document.getElementById("detailed-inspection-card");
                                if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
                              }}
                              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-cyan-950 hover:bg-cyan-900/80 text-cyan-300 text-xs font-semibold border border-cyan-700/60 transition-colors"
                            >
                              <span>{t.claimSpotlightViewEvidence}</span>
                              <ArrowRight className="h-3.5 w-3.5" />
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {claims.length === 0 ? (
                    <p className="text-xs text-slate-500 italic p-4 text-center">No explicit claims identified.</p>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                      {claims.map((claim) => {
                        const isSelected = activeSelectedClaim?.id === claim.id;
                        return (
                          <div
                            key={claim.id}
                            onClick={() => setSelectedClaimId(claim.id)}
                            className={`p-4 rounded-xl transition-all cursor-pointer space-y-3 flex flex-col justify-between ${
                              isSelected
                                ? "bg-slate-900 border-2 border-cyan-500/80 shadow-lg shadow-cyan-950/30 ring-1 ring-cyan-500/50"
                                : "bg-slate-950/70 border border-slate-800 hover:border-slate-700 hover:bg-slate-900/60"
                            }`}
                          >
                          <div className="space-y-2">
                            <div className="flex flex-wrap items-center justify-between gap-1.5">
                              <span className="text-[10px] font-mono uppercase tracking-wider px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800/40">
                                {claim.claim_type} CLAIM
                              </span>
                              {getStatusBadge(
                                claim.verification?.status || claim.verification_status,
                                claim.verification?.is_demo
                              )}
                            </div>

                            <div className="space-y-0.5">
                              <span className="text-[10px] font-mono uppercase text-slate-400">OBSERVED CLAIM:</span>
                              <h5 className="font-semibold text-white text-sm leading-snug">
                                &ldquo;{claim.claim_text}&rdquo;
                              </h5>
                            </div>
                          </div>

                          {claim.verification && (
                            <div className="space-y-1.5 p-3 rounded-lg bg-slate-900/80 border border-slate-800 text-xs">
                              <span className="text-[10px] font-mono text-slate-400 block">
                                SOURCE: {claim.verification.source_name}
                              </span>
                              <p className="text-slate-300 text-[11px]">
                                <strong className="text-slate-400">WHY:</strong> {claim.verification.reason}
                              </p>
                            </div>
                          )}

                          <div className="space-y-1 text-xs pt-2 border-t border-slate-800/60 text-slate-400">
                            {claim.registration_reference && (
                              <p>
                                <strong className="text-slate-300">Registration Code:</strong>{" "}
                                <span className="font-mono text-amber-300">{claim.registration_reference}</span>
                              </p>
                            )}
                            <p className="italic text-[11px] text-slate-400">
                              <strong className="text-slate-300 not-italic">Observed Text:</strong> &ldquo;{claim.evidence_text}&rdquo;
                            </p>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
                </div>
              )}

              {/* TAB: ENTITIES */}
              {activeTab === "entities" && (
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span>Observed Digital, Corporate & Personal Entities</span>
                    <span className="font-mono text-slate-400 text-[11px]">{entities.length} Found</span>
                  </div>

                  {entities.length === 0 ? (
                    <p className="text-xs text-slate-500 italic p-4 text-center">No entities identified.</p>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                      {entities.map((entity) => (
                        <div
                          key={entity.id}
                          className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 space-y-2 flex flex-col justify-between"
                        >
                          <div className="space-y-1">
                            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800/40">
                              {entity.entity_type}
                            </span>
                            <h5 className="font-semibold text-white text-sm">{entity.name}</h5>
                          </div>
                          <p className="text-[11px] text-slate-400 italic">
                            <strong className="text-slate-300 not-italic">Context:</strong> {entity.evidence.context}
                          </p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* TAB: REGULATORY REFERENCES */}
              {activeTab === "regulatory" && (
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span>Statutory & Regulatory Mentions</span>
                    <span className="font-mono text-slate-400 text-[11px]">{regulatoryRefs.length} References</span>
                  </div>

                  {regulatoryRefs.length === 0 ? (
                    <p className="text-xs text-slate-500 italic p-4 text-center">No regulatory references observed.</p>
                  ) : (
                    <div className="space-y-3">
                      {regulatoryRefs.map((reg) => (
                        <div
                          key={reg.id}
                          className="p-4 rounded-xl bg-slate-950/70 border border-amber-900/30 space-y-2"
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <Award className="h-4 w-4 text-amber-400" />
                              <span className="font-bold text-white text-sm">
                                {reg.authority} ({reg.claim_type})
                              </span>
                              {reg.registration_number && (
                                <span className="font-mono text-xs px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800/40">
                                  {reg.registration_number}
                                </span>
                              )}
                            </div>
                            {getStatusBadge(
                              reg.verification?.status || reg.verification_status,
                              reg.verification?.is_demo
                            )}
                          </div>
                          <p className="text-xs text-slate-300 italic bg-slate-900/50 p-2.5 rounded-lg border border-slate-800">
                            &ldquo;{reg.context}&rdquo;
                          </p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* TAB: FINANCIAL CLAIMS */}
              {activeTab === "financial" && (
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span>Linguistic Classification of Financial Promises & Urgency</span>
                    <span className="font-mono text-slate-500 text-[11px]">
                      Severity indicates linguistic pattern, NOT fraud determination
                    </span>
                  </div>

                  {financialClaims.length === 0 ? (
                    <p className="text-xs text-slate-500 italic p-4 text-center">No high-risk financial claim patterns detected.</p>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {financialClaims.map((fin) => (
                        <div
                          key={fin.id}
                          className="p-4 rounded-xl bg-slate-950/70 border border-rose-900/30 space-y-2 flex flex-col justify-between"
                        >
                          <div className="flex items-center justify-between">
                            <span className="text-[10px] font-mono uppercase tracking-wider px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800/40 font-bold">
                              {fin.claim_type.replace(/_/g, " ")}
                            </span>
                            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded border border-rose-800 text-rose-300">
                              Language: {fin.severity}
                            </span>
                          </div>
                          <h5 className="font-mono font-semibold text-rose-200 text-sm">
                            &ldquo;{fin.claim_text}&rdquo;
                          </h5>
                          <p className="text-[11px] text-slate-400 italic">
                            <strong className="text-slate-300 not-italic">Context:</strong> {fin.context}
                          </p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* TAB: RELATIONSHIPS */}
              {activeTab === "relationships" && (
                <div className="space-y-3">
                  {relationships.length === 0 ? (
                    <p className="text-xs text-slate-500 italic p-4 text-center">No relationships resolved.</p>
                  ) : (
                    <div className="space-y-2.5">
                      {relationships.map((rel) => (
                        <div
                          key={rel.id}
                          className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 flex items-center justify-between text-xs"
                        >
                          <div className="flex items-center gap-2">
                            <Network className="h-3.5 w-3.5 text-blue-400" />
                            <span className="font-mono text-[10px] uppercase px-2 py-0.5 rounded bg-slate-900 text-blue-300 border border-slate-800">
                              {rel.relationship_type.replace(/_/g, " ")}
                            </span>
                            <span className="text-slate-200">{rel.description}</span>
                          </div>
                          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800">
                            UNKNOWN
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* TAB: EVIDENCE OBJECTS */}
              {activeTab === "evidence" && (
                <div className="space-y-3">
                  <div className="max-h-96 overflow-y-auto space-y-2.5 pr-1">
                    {evidenceList.map((ev) => (
                      <div
                        key={ev.id}
                        className="p-3 rounded-lg bg-slate-950/60 border border-slate-800/80 space-y-1.5 text-xs font-mono"
                      >
                        <div className="flex items-center justify-between text-[11px]">
                          <span className="text-blue-400 font-bold">{ev.id}</span>
                          <span className="text-slate-500 text-[10px]">{ev.extraction_method}</span>
                        </div>
                        <p className="text-slate-200 font-semibold">{ev.extracted_text}</p>
                        <p className="text-[11px] text-slate-400 italic font-sans">{ev.context}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* TAB: LINKS */}
              {activeTab === "links" && (
                <div className="space-y-2 max-h-80 overflow-y-auto pr-1">
                  {data.links.map((link, idx) => (
                    <div
                      key={idx}
                      className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/60 border border-slate-800/80 text-xs"
                    >
                      <div className="min-w-0 pr-3">
                        <span className="font-medium text-slate-200 block truncate">{link.text || link.url}</span>
                        <span className="text-[11px] text-slate-500 font-mono block truncate">{link.url}</span>
                      </div>
                      <span className="shrink-0 px-2 py-0.5 rounded text-[10px] font-mono bg-slate-800 text-slate-400">
                        {link.internal ? "INTERNAL" : "EXTERNAL"}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        )}
      </div>
    </section>
  );
}
