import * as React from "react";
import { ShieldCheck } from "lucide-react";

export function Hero() {
  return (
    <section className="relative pt-8 pb-4 md:pt-12 md:pb-6 text-center">
      {/* Background subtle radial glow */}
      <div className="absolute inset-0 -z-10 flex items-center justify-center">
        <div className="h-[220px] w-[460px] rounded-full bg-blue-600/10 blur-[90px] pointer-events-none" />
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6">
        {/* Small product badge */}
        <div className="inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-950/40 px-3.5 py-1 text-xs font-medium text-blue-300 backdrop-blur-sm mb-4">
          <ShieldCheck className="h-3.5 w-3.5 text-blue-400" />
          <span>Evidence-Based Financial Scam & Trust Verification</span>
        </div>

        {/* Brand & Primary Message */}
        <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white mb-3">
          RakshaScan
          <span className="block mt-1.5 text-xl sm:text-3xl font-semibold bg-gradient-to-r from-blue-200 via-slate-100 to-blue-300 bg-clip-text text-transparent">
            &ldquo;Before you trust it, verify the story behind it.&rdquo;
          </span>
        </h1>

        {/* Short supporting statement */}
        <p className="text-sm sm:text-base text-slate-300 max-w-2xl mx-auto leading-relaxed mb-4">
          Trace the evidence behind financial claims, identities, websites, and regulatory registrations before transferring funds.
        </p>

        {/* Guardrail positioning notice */}
        <div className="inline-flex items-center justify-center gap-2 text-[11px] text-slate-400 px-3 py-1 rounded-md bg-slate-900/50 border border-slate-800/60 max-w-xl mx-auto">
          <span>Non-prejudicial evidence analysis • No speculative financial or investment advice</span>
        </div>
      </div>
    </section>
  );
}

