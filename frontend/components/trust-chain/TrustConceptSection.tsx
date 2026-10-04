"use client";

import * as React from "react";
import { StatusBadge } from "@/components/ui/Badge";
import {
  FileText,
  Building,
  Award,
  UserCheck,
  Globe,
  Smartphone,
  Share2,
  CreditCard,
  ArrowRight,
  ArrowDown,
  Info,
  ShieldCheck,
  AlertTriangle,
} from "lucide-react";
import { VerificationStatus } from "@/types";

interface ConceptNode {
  title: string;
  type: string;
  icon: React.ElementType;
  exampleStatus: VerificationStatus;
  description: string;
}

export function TrustConceptSection() {
  const chainNodes: ConceptNode[] = [
    {
      title: "Claim",
      type: "Promised Offering",
      icon: FileText,
      exampleStatus: "CONTRADICTORY",
      description: "Promises made in ads or chats (e.g., 'Guaranteed 40% monthly returns').",
    },
    {
      title: "Entity",
      type: "Claimed Company",
      icon: Building,
      exampleStatus: "UNVERIFIED",
      description: "The business entity claiming to manage funds or issue securities.",
    },
    {
      title: "Registration",
      type: "Regulatory License",
      icon: Award,
      exampleStatus: "CONTRADICTORY",
      description: "Statutory credentials (SEBI RIA/Research Analyst, RBI NBFC, MCA CIN).",
    },
    {
      title: "Official Identity",
      type: "Key Persons",
      icon: UserCheck,
      exampleStatus: "UNKNOWN",
      description: "Verifiable public identities of founders, directors, and officers.",
    },
    {
      title: "Website",
      type: "Digital Domain",
      icon: Globe,
      exampleStatus: "UNVERIFIED",
      description: "Domain age, WHOIS integrity, SSL ownership, and server origin.",
    },
    {
      title: "App",
      type: "Client Vector",
      icon: Smartphone,
      exampleStatus: "UNKNOWN",
      description: "Official store listing vs unverified sideloaded Android APKs.",
    },
    {
      title: "Social Account",
      type: "Comms Channel",
      icon: Share2,
      exampleStatus: "UNVERIFIED",
      description: "Anonymous Telegram channels, WhatsApp groups, or social profiles.",
    },
    {
      title: "Payment Identity",
      type: "Settlement Account",
      icon: CreditCard,
      exampleStatus: "VERIFIED",
      description: "Audited corporate escrow account vs personal mule UPI handles.",
    },
  ];

  return (
    <section id="trust-chain" className="py-16 border-t border-slate-800/80 bg-slate-950/60 scroll-mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Heading */}
        <div className="max-w-3xl mx-auto text-center space-y-4 mb-14">
          <div className="inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-950/30 px-3.5 py-1 text-xs font-medium text-blue-400">
            <ShieldCheck className="h-3.5 w-3.5" />
            <span>Foundational Trust Architecture</span>
          </div>
          <h2 className="text-2xl sm:text-4xl font-bold tracking-tight text-white">
            &ldquo;Don&apos;t just check the link. Check the trust chain.&rdquo;
          </h2>
          <p className="text-sm sm:text-base text-slate-300 leading-relaxed">
            Legitimate financial intermediaries maintain an unbroken, verifiable link from their marketing claims to their banking rails. Fraudulent operations break this chain at critical vectors.
          </p>
        </div>

        {/* Status Definition Legend */}
        <div className="mb-10 p-5 rounded-xl border border-slate-800 bg-slate-900/60 backdrop-blur-sm">
          <div className="flex items-center gap-2 mb-3 text-xs font-semibold uppercase tracking-wider text-slate-400">
            <Info className="h-4 w-4 text-blue-400" />
            <span>Four Neutral Verification States (Explained)</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
            <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800 space-y-1.5">
              <StatusBadge status="VERIFIED" />
              <p className="text-slate-400 leading-relaxed text-[11px]">
                Independently substantiated by authoritative institutional records (e.g. SEBI directory or MCA filing).
              </p>
            </div>
            <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800 space-y-1.5">
              <StatusBadge status="UNVERIFIED" />
              <p className="text-slate-400 leading-relaxed text-[11px]">
                Claimed in public promotion, but no independent public or regulatory directory confirmed it.
              </p>
            </div>
            <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800 space-y-1.5">
              <StatusBadge status="CONTRADICTORY" />
              <p className="text-slate-400 leading-relaxed text-[11px]">
                Explicit mismatch detected between the claim and official reality (e.g. license cloned or illegal guarantee).
              </p>
            </div>
            <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800 space-y-1.5">
              <StatusBadge status="UNKNOWN" />
              <p className="text-slate-400 leading-relaxed text-[11px]">
                Insufficient public evidence to substantiate without additional user-provided artifacts.
              </p>
            </div>
          </div>
        </div>

        {/* Visual Trust Chain Diagram */}
        <div className="relative">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {chainNodes.map((node, index) => {
              const Icon = node.icon;
              return (
                <div
                  key={node.title}
                  className="relative p-5 rounded-xl border border-slate-800/90 bg-slate-900/80 hover:border-slate-700 transition-all flex flex-col justify-between group"
                >
                  {/* Step order index */}
                  <div className="flex items-center justify-between mb-3">
                    <span className="font-mono text-xs text-slate-500 font-semibold">
                      STEP {index + 1}
                    </span>
                    <StatusBadge status={node.exampleStatus} size="sm" />
                  </div>

                  {/* Icon & Title */}
                  <div className="space-y-1.5 mb-3">
                    <div className="flex items-center gap-2.5">
                      <div className="h-8 w-8 rounded-lg bg-slate-800/80 border border-slate-700/60 flex items-center justify-center text-blue-400 group-hover:text-blue-300 transition-colors">
                        <Icon className="h-4 w-4" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-white text-sm">{node.title}</h4>
                        <span className="text-[11px] text-slate-400 font-mono block">
                          {node.type}
                        </span>
                      </div>
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed pt-1">
                      {node.description}
                    </p>
                  </div>

                  {/* Arrow Indicator for chain continuity */}
                  {index < chainNodes.length - 1 && (
                    <div className="hidden lg:block absolute -right-3.5 top-1/2 -translate-y-1/2 z-10 text-slate-600">
                      <div className="h-6 w-6 rounded-full bg-slate-950 border border-slate-800 flex items-center justify-center">
                        <ArrowRight className="h-3 w-3 text-slate-400" />
                      </div>
                    </div>
                  )}
                  {index < chainNodes.length - 1 && (
                    <div className="block lg:hidden text-center text-slate-600 py-1">
                      <ArrowDown className="h-3.5 w-3.5 mx-auto text-slate-500" />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Prototype Disclaimer Banner */}
        <div className="mt-8 rounded-xl border border-amber-900/30 bg-amber-950/20 p-4 text-xs text-amber-300/90 flex items-center gap-3">
          <AlertTriangle className="h-4 w-4 text-amber-400 shrink-0" />
          <span>
            <strong>Educational Demonstration Note:</strong> The statuses shown above represent educational status examples to illustrate how RakshaScan structures verification. The current frontend prototype does not imply actual verification of third-party domains.
          </span>
        </div>
      </div>
    </section>
  );
}
