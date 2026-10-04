import * as React from "react";
import {
  Link2,
  FileSearch,
  Route,
  UserCheck2,
  ShieldCheck,
  CheckCircle,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card";

export function FeatureSection() {
  const features = [
    {
      id: "trust-chain",
      title: "1. Financial Trust Chain",
      subtitle: "Pinpointing Verification Breakdown",
      icon: Link2,
      accent: "text-blue-400 bg-blue-950/50 border-blue-800/40",
      description:
        "RakshaScan connects claims, entities, registrations, websites, and settlement vectors into an explicit chain. Rather than guessing legitimacy, it reveals precisely where the chain of evidence snaps.",
      points: [
        "Traces claimed company name to actual Ministry of Corporate Affairs (MCA) filings",
        "Cross-references declared advisory licenses against SEBI public registers",
        "Detects disconnected banking and payment rails (e.g. personal UPI VPAs)",
      ],
    },
    {
      id: "evidence-assessment",
      title: "2. Evidence-Based Assessment",
      subtitle: "No Black-Box Arbiters",
      icon: FileSearch,
      accent: "text-cyan-400 bg-cyan-950/50 border-cyan-800/40",
      description:
        "Warnings should never be opaque declarations. Every flag raised by RakshaScan is anchored by primary digital evidence, statutory regulations, and factual findings that any user can independently verify.",
      points: [
        "Explicitly states 'What We Found', 'What We Verified', and 'What Remains Uncertain'",
        "Quotes verbatim statutory rules (e.g. SEBI prohibition of guaranteed returns)",
        "Distinguishes between factual contradictions and missing public data",
      ],
    },
    {
      id: "scam-journey",
      title: "3. Scam Journey Reconstruction",
      subtitle: "Predictable Fraud Lifecycles",
      icon: Route,
      accent: "text-purple-400 bg-purple-950/50 border-purple-800/40",
      description:
        "Financial scams follow repeatable social-engineering playbooks. RakshaScan maps observed interactions against documented fraud lifecycles to project possible subsequent exploitation stages.",
      points: [
        "Maps unsolicited chat invites to institutional impersonation patterns",
        "Flags advance-fee withdrawal lockouts before funds are committed",
        "Provides situational awareness of upcoming psychological pressure tactics",
      ],
    },
    {
      id: "identity-detection",
      title: "4. Identity & Impersonation Detection",
      subtitle: "Comparing Claim vs Reality",
      icon: UserCheck2,
      accent: "text-emerald-400 bg-emerald-950/50 border-emerald-800/40",
      description:
        "Fraudulent operations frequently clone legitimate SEBI-registered advisors or corporate identities. RakshaScan contrasts claimed credentials with authoritative registry records to catch impostors.",
      points: [
        "Detects cloned registration numbers assigned to unrelated legitimate brokers",
        "Identifies synthetic corporate personas and commercial stock profile images",
        "Flags freshly registered typo-squatted domains spoofing established brands",
      ],
    },
    {
      id: "safe-steps",
      title: "5. Safe Next Steps",
      subtitle: "Defensive Protocols, Not Investment Advice",
      icon: ShieldCheck,
      accent: "text-amber-400 bg-amber-950/50 border-amber-800/40",
      description:
        "Users receive practical, defensive self-protection protocols rather than financial speculation or trading advice. Guidance directs users to official verification directories and emergency reporting rails.",
      points: [
        "Direct emergency routing to National Cyber Crime Helpline (1930)",
        "Direct search instructions for official SEBI and RBI database verification",
        "Actionable incident preservation steps if financial transfers already occurred",
      ],
    },
  ];

  return (
    <section id="features" className="py-16 bg-slate-900/40 border-t border-slate-800/80 scroll-mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="max-w-3xl mx-auto text-center space-y-3 mb-12">
          <div className="inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-950/30 px-3.5 py-1 text-xs font-medium text-blue-400">
            <span>Core Capabilities</span>
          </div>
          <h2 className="text-2xl sm:text-4xl font-bold tracking-tight text-white">
            How RakshaScan Protects Financial Decision-Making
          </h2>
          <p className="text-sm sm:text-base text-slate-300 leading-relaxed">
            Engineered around verifiable institutional evidence, defensive clarity, and explainable trust chains.
          </p>
        </div>

        {/* Feature Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, idx) => {
            const Icon = feature.icon;
            return (
              <Card
                key={feature.id}
                className={`border-slate-800 bg-slate-950/70 hover:border-slate-700/80 transition-all flex flex-col justify-between ${
                  idx === 0 || idx === 1 ? "lg:col-span-1" : ""
                }`}
              >
                <CardHeader>
                  <div className="flex items-center gap-3 mb-3">
                    <div
                      className={`h-10 w-10 rounded-lg flex items-center justify-center border ${feature.accent}`}
                    >
                      <Icon className="h-5 w-5" />
                    </div>
                    <div>
                      <span className="text-xs font-mono uppercase tracking-wider text-slate-400 block">
                        {feature.subtitle}
                      </span>
                      <CardTitle className="text-base font-bold text-white">
                        {feature.title}
                      </CardTitle>
                    </div>
                  </div>
                  <CardDescription className="text-xs text-slate-300 leading-relaxed">
                    {feature.description}
                  </CardDescription>
                </CardHeader>
                <CardContent className="pt-0">
                  <div className="space-y-2 pt-2 border-t border-slate-800/60">
                    {feature.points.map((pt) => (
                      <div key={pt} className="flex items-start gap-2 text-xs text-slate-400">
                        <CheckCircle className="h-3.5 w-3.5 text-blue-400/80 shrink-0 mt-0.5" />
                        <span>{pt}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </section>
  );
}
