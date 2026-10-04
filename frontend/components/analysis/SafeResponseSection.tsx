"use client";

import React, { useState } from "react";
import {
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  FileText,
  Clock,
  ExternalLink,
  Lock,
  PhoneCall,
  CheckCircle2,
  HelpCircle,
  Sparkles,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import {
  SafeResponseData,
  RecoveryGuidanceData,
  SafeActionType,
  ActionState,
} from "@/types";
import { useLanguage } from "@/lib/i18n";

interface SafeResponseSectionProps {
  safeResponse?: SafeResponseData;
  recoveryGuidance?: RecoveryGuidanceData;
  targetArtifact?: string;
}

export function SafeResponseSection({
  safeResponse,
  recoveryGuidance,
  targetArtifact,
}: SafeResponseSectionProps) {
  const { t, simpleMode, simplifyText } = useLanguage();

  // User-provided facts (Interactive control)
  const [userSentMoney, setUserSentMoney] = useState<"YES" | "NO" | "NOT_SURE" | null>(null);
  const [userSharedCreds, setUserSharedCreds] = useState<"YES" | "NO" | "NOT_SURE" | null>(null);
  const [expandedActionIndex, setExpandedActionIndex] = useState<number | null>(0);
  const [showTimeline, setShowTimeline] = useState<boolean>(true);

  if (!safeResponse) return null;

  // Determine if recovery guidance is activated (from engine or dynamic user toggle)
  const isRecoveryActive =
    recoveryGuidance?.is_activated ||
    safeResponse.recovery_guidance?.is_activated ||
    userSentMoney === "YES" ||
    userSentMoney === "NOT_SURE" ||
    userSharedCreds === "YES";

  // State-specific visual styling
  const getActionStateBadge = (state: ActionState) => {
    switch (state) {
      case "HIGH_CAUTION":
        return {
          label: t.actionStateCaution,
          color: "border-red-500/50 bg-red-950/30 text-red-300",
          icon: <ShieldAlert className="h-4 w-4 text-red-400" />,
        };
      case "POST_INCIDENT_GUIDANCE":
        return {
          label: t.actionStatePostIncident,
          color: "border-amber-500/50 bg-amber-950/40 text-amber-200",
          icon: <AlertTriangle className="h-4 w-4 text-amber-400" />,
        };
      case "PAUSE_AND_VERIFY":
        return {
          label: t.actionStatePause,
          color: "border-yellow-500/50 bg-yellow-950/30 text-yellow-300",
          icon: <AlertTriangle className="h-4 w-4 text-yellow-400" />,
        };
      case "SAFE_TO_CONTINUE_WITH_VERIFICATION":
        return {
          label: t.actionStateSafe,
          color: "border-emerald-500/50 bg-emerald-950/30 text-emerald-300",
          icon: <ShieldCheck className="h-4 w-4 text-emerald-400" />,
        };
      default:
        return {
          label: t.actionStateInsufficient,
          color: "border-slate-600/50 bg-slate-900/50 text-slate-300",
          icon: <HelpCircle className="h-4 w-4 text-slate-400" />,
        };
    }
  };

  const getActionIcon = (action: SafeActionType) => {
    switch (action) {
      case "PAUSE":
        return <AlertTriangle className="h-5 w-5 text-amber-400" />;
      case "VERIFY":
        return <ShieldCheck className="h-5 w-5 text-blue-400" />;
      case "DO_NOT_SEND_ADDITIONAL_MONEY":
        return <ShieldAlert className="h-5 w-5 text-red-400" />;
      case "DO_NOT_SHARE_CREDENTIALS":
        return <Lock className="h-5 w-5 text-purple-400" />;
      case "PRESERVE_EVIDENCE":
        return <FileText className="h-5 w-5 text-teal-400" />;
      case "CONTACT_BANK_OR_PAYMENT_PROVIDER":
        return <PhoneCall className="h-5 w-5 text-amber-400" />;
      case "REPORT":
        return <ExternalLink className="h-5 w-5 text-indigo-400" />;
      default:
        return <ShieldCheck className="h-5 w-5 text-slate-400" />;
    }
  };

  const activeGuidance = recoveryGuidance || safeResponse.recovery_guidance;
  const currentActionState =
    isRecoveryActive && safeResponse.action_state !== "POST_INCIDENT_GUIDANCE"
      ? ("POST_INCIDENT_GUIDANCE" as ActionState)
      : safeResponse.action_state;

  const stateBadge = getActionStateBadge(currentActionState);

  return (
    <section id="safe-response" className="space-y-6 pt-4 scroll-mt-20">
      {/* Section Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2.5">
            <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-white flex items-center gap-2">
              <ShieldAlert className="h-5 w-5 text-blue-400" />
              <span>WHAT SHOULD YOU DO NOW?</span>
            </h2>
            {simpleMode && (
              <span className="flex items-center gap-1 text-[11px] font-medium bg-amber-500/20 text-amber-300 border border-amber-500/30 px-2 py-0.5 rounded-full">
                <Sparkles className="h-3 w-3" /> {t.plainLanguageActiveNotice}
              </span>
            )}
          </div>
          <p className="text-xs text-slate-300 mt-1">
            {t.safeResponseSubtitle}
            {targetArtifact && (
              <span className="ml-2 font-mono text-[11px] text-slate-400">• {targetArtifact}</span>
            )}
          </p>
        </div>

        {/* Action State Status Badge */}
        <div className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-semibold ${stateBadge.color}`}>
          {stateBadge.icon}
          <span>{stateBadge.label}</span>
        </div>
      </div>

      {/* Interactive User Control Card */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4 space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold tracking-wider uppercase text-slate-300">
            Tell RakshaScan your situation for tailored recovery guidance:
          </span>
          <span className="text-[11px] text-slate-400 italic">Optional • Never saved to database</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Question 1: Sent Money */}
          <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
            <p className="text-xs font-semibold text-slate-200">{t.userQuestionMoney}</p>
            <div className="flex gap-2">
              {(["NO", "YES", "NOT_SURE"] as const).map((opt) => (
                <button
                  key={opt}
                  type="button"
                  onClick={() => setUserSentMoney(opt)}
                  className={`flex-1 py-1.5 px-2 text-xs font-medium rounded-lg border transition-all ${
                    userSentMoney === opt
                      ? opt === "YES"
                        ? "bg-red-500/20 border-red-500/60 text-red-200 font-bold"
                        : opt === "NO"
                        ? "bg-emerald-500/20 border-emerald-500/60 text-emerald-200 font-bold"
                        : "bg-amber-500/20 border-amber-500/60 text-amber-200 font-bold"
                      : "bg-slate-900/80 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800"
                  }`}
                  id={`btn-money-${opt.toLowerCase()}`}
                >
                  {opt === "YES" ? t.optionYes : opt === "NO" ? t.optionNo : t.optionNotSure}
                </button>
              ))}
            </div>
          </div>

          {/* Question 2: Shared Credentials */}
          <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
            <p className="text-xs font-semibold text-slate-200">{t.userQuestionCreds}</p>
            <div className="flex gap-2">
              {(["NO", "YES", "NOT_SURE"] as const).map((opt) => (
                <button
                  key={opt}
                  type="button"
                  onClick={() => setUserSharedCreds(opt)}
                  className={`flex-1 py-1.5 px-2 text-xs font-medium rounded-lg border transition-all ${
                    userSharedCreds === opt
                      ? opt === "YES"
                        ? "bg-red-500/20 border-red-500/60 text-red-200 font-bold"
                        : opt === "NO"
                        ? "bg-emerald-500/20 border-emerald-500/60 text-emerald-200 font-bold"
                        : "bg-amber-500/20 border-amber-500/60 text-amber-200 font-bold"
                      : "bg-slate-900/80 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800"
                  }`}
                  id={`btn-creds-${opt.toLowerCase()}`}
                >
                  {opt === "YES" ? t.optionYes : opt === "NO" ? t.optionNo : t.optionNotSure}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Recommended Action Cards */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-300">
            Immediate Safety Steps ({safeResponse.recommended_actions.length})
          </h3>
          <span className="text-[11px] font-mono text-slate-400">
            Actionable guidance derived from evidence findings
          </span>
        </div>

        <div className="grid grid-cols-1 gap-3">
          {safeResponse.recommended_actions.map((rec, idx) => {
            const isExpanded = expandedActionIndex === idx;
            return (
              <div
                key={`${rec.action}-${idx}`}
                className="rounded-xl border border-slate-800 bg-slate-900/80 overflow-hidden transition-all hover:border-slate-700"
              >
                <div
                  onClick={() => setExpandedActionIndex(isExpanded ? null : idx)}
                  className="flex items-start justify-between gap-3 p-4 cursor-pointer"
                >
                  <div className="flex items-start gap-3">
                    <div className="p-2 rounded-lg bg-slate-950 border border-slate-800 shrink-0 mt-0.5">
                      {getActionIcon(rec.action)}
                    </div>
                    <div>
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="text-xs font-mono font-semibold px-2 py-0.5 rounded bg-blue-950/60 text-blue-300 border border-blue-800/50">
                          STEP {idx + 1}: {rec.action}
                        </span>
                        <h4 className="text-sm font-semibold text-white">{rec.title}</h4>
                      </div>
                      <p className="text-xs text-slate-300 mt-1.5 leading-relaxed">
                        {simplifyText(rec.explanation)}
                      </p>
                    </div>
                  </div>

                  <button
                    type="button"
                    className="text-slate-400 hover:text-slate-200 p-1"
                    aria-label="Toggle details"
                  >
                    {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                  </button>
                </div>

                {/* Expanded Details Drawer */}
                {isExpanded && (
                  <div className="border-t border-slate-800/80 bg-slate-950/60 p-4 space-y-3 text-xs">
                    <div className="flex items-start gap-2">
                      <span className="font-semibold text-slate-400 shrink-0">Why RakshaScan recommends this:</span>
                      <span className="text-slate-300">{simplifyText(rec.reason)}</span>
                    </div>

                    {/* Traceability: Evidence & Verification IDs */}
                    {(rec.evidence_ids.length > 0 || rec.verification_ids.length > 0) && (
                      <div className="flex items-center gap-2 pt-2 border-t border-slate-800/60 flex-wrap">
                        <span className="text-[11px] text-slate-400">Traceable Provenance:</span>
                        {rec.evidence_ids.map((eid) => (
                          <span
                            key={eid}
                            className="font-mono text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700"
                          >
                            {eid}
                          </span>
                        ))}
                        {rec.verification_ids.map((vid) => (
                          <span
                            key={vid}
                            className="font-mono text-[10px] px-1.5 py-0.5 rounded bg-blue-900/40 text-blue-300 border border-blue-800/50"
                          >
                            {vid}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Recovery Guidance Section (Visible when activated) */}
      {isRecoveryActive && activeGuidance && (
        <div
          id="recovery-guidance-panel"
          className="rounded-xl border border-amber-500/40 bg-gradient-to-b from-amber-950/20 to-slate-950 p-5 space-y-5"
        >
          <div className="flex items-start justify-between gap-3 border-b border-amber-500/20 pb-3">
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-lg bg-amber-500/20 border border-amber-500/40 text-amber-300">
                <AlertTriangle className="h-5 w-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-amber-200 flex items-center gap-2">
                  {t.recoveryTitle}
                </h3>
                <p className="text-xs text-amber-300/80 mt-0.5">
                  {activeGuidance.activation_reason || t.recoverySubtitle}
                </p>
              </div>
            </div>
            <span className="text-[10px] font-mono uppercase px-2 py-1 rounded bg-amber-500/10 text-amber-300 border border-amber-500/30">
              RECOVERY MODE ACTIVE
            </span>
          </div>

          {/* Recovery Steps List */}
          <div className="space-y-4">
            {activeGuidance.steps.map((step, idx) => (
              <div
                key={step.category || idx}
                className="p-3.5 rounded-lg bg-slate-900/90 border border-slate-800/90 space-y-2"
              >
                <div className="flex items-center justify-between">
                  <h4 className="text-xs font-bold text-slate-100 uppercase tracking-wide flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-amber-400" />
                    {step.title}
                  </h4>
                  <span className="text-[10px] font-mono text-slate-400">{step.category}</span>
                </div>
                <ul className="space-y-1.5 pl-6 list-disc text-xs text-slate-300 leading-relaxed">
                  {step.instructions.map((inst, iIdx) => (
                    <li key={iIdx}>{simplifyText(inst)}</li>
                  ))}
                </ul>
                {step.disclaimer && (
                  <p className="text-[11px] text-amber-300/70 italic pl-6 pt-1 border-t border-slate-800/60">
                    {step.disclaimer}
                  </p>
                )}
              </div>
            ))}
          </div>

          {/* Official Jurisdictional Notice */}
          <div className="p-3 rounded-lg bg-blue-950/30 border border-blue-800/40 text-xs text-blue-200 flex items-start gap-2.5">
            <PhoneCall className="h-4 w-4 text-blue-400 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-blue-100">National Cyber Crime Reporting Portal (India)</p>
              <p className="mt-0.5 text-blue-300/90">
                Call helpline <strong>1930</strong> or file online at <strong>cybercrime.gov.in</strong>. Prepare your bank transaction references (UTR/RRN) and communication screenshots.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Incident Timeline Reconstruction */}
      {safeResponse.incident_timeline && safeResponse.incident_timeline.events.length > 0 && (
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4 space-y-3">
          <div
            onClick={() => setShowTimeline(!showTimeline)}
            className="flex items-center justify-between cursor-pointer"
          >
            <div className="flex items-center gap-2">
              <Clock className="h-4 w-4 text-blue-400" />
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300">
                {t.timelineTitle} ({safeResponse.incident_timeline.events.length} Milestones)
              </h4>
            </div>
            <button type="button" className="text-slate-400 hover:text-slate-200 text-xs flex items-center gap-1">
              <span>{showTimeline ? "Collapse" : "Expand"}</span>
              {showTimeline ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
            </button>
          </div>

          {showTimeline && (
            <div className="space-y-3 pt-2">
              <p className="text-[11px] text-slate-400 italic">
                {safeResponse.incident_timeline.summary}
              </p>

              <div className="relative pl-6 space-y-4 border-l-2 border-slate-800 ml-2">
                {safeResponse.incident_timeline.events.map((ev, eIdx) => (
                  <div key={eIdx} className="relative">
                    <div className="absolute -left-[31px] top-1 h-3 w-3 rounded-full bg-blue-500 ring-4 ring-slate-950" />
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-semibold text-white">{ev.title}</span>
                        <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">
                          {ev.source}
                        </span>
                      </div>
                      <p className="text-xs text-slate-300 mt-0.5">{simplifyText(ev.description)}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Disclaimers & Trust Statement */}
      <div className="p-3.5 rounded-lg bg-slate-950/80 border border-slate-800 text-[11px] text-slate-400 space-y-1">
        <p className="leading-relaxed">{t.disclaimerText}</p>
        <p className="leading-relaxed">{t.recoveryDisclaimerText}</p>
      </div>
    </section>
  );
}
