import * as React from "react";
import { Shield, ExternalLink, CheckCircle2 } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-slate-800/80 bg-slate-950 text-slate-400 text-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-10">
        {/* Top Disclaimer Banner */}
        <div className="rounded-xl border border-blue-900/40 bg-blue-950/20 p-5 flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
          <div className="flex items-start gap-3">
            <Shield className="h-5 w-5 text-blue-400 shrink-0 mt-0.5" />
            <div className="space-y-1">
              <h4 className="text-white font-semibold text-sm">
                Mandatory Platform Disclaimer & Positioning
              </h4>
              <p className="text-xs text-slate-300 leading-relaxed max-w-3xl">
                RakshaScan is an evidence-based financial scam and trust-verification research platform.
                RakshaScan is <strong>NOT</strong> an investment advisor, stock recommendation tool, trading platform,
                or a definitive judicial scam detector. It maps public digital and regulatory artifacts to highlight
                verifiable evidence, missing trust links, and defensive precautions.
              </p>
            </div>
          </div>
          <div className="shrink-0 flex items-center gap-2">
            <span className="text-xs bg-slate-900 text-blue-300 px-3 py-1.5 rounded-lg border border-blue-800/50 font-mono flex items-center gap-1.5">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
              Verification Engine Active
            </span>
          </div>
        </div>

        {/* Links and Institutional Verification Directories */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-3 md:col-span-1">
            <div className="flex items-center gap-2 text-white font-bold text-base">
              <Shield className="h-5 w-5 text-blue-400" />
              <span>RakshaScan</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              &ldquo;Before you trust it, verify the story behind it.&rdquo;
              Empowering Indian retail investors with explainable trust verification.
            </p>
            <div className="pt-2 text-xs text-slate-400">
              SANGYAN 2026 Hackathon Initiative
            </div>
          </div>

          <div>
            <h5 className="text-xs font-semibold text-white uppercase tracking-wider mb-3">
              Official Indian Regulators
            </h5>
            <ul className="space-y-2 text-xs">
              <li>
                <a
                  href="https://www.sebi.gov.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1.5 text-slate-300 hover:text-blue-400 transition-colors"
                >
                  SEBI Intermediary Registry
                  <ExternalLink className="h-3 w-3 text-slate-400" />
                </a>
              </li>
              <li>
                <a
                  href="https://www.rbi.org.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1.5 text-slate-300 hover:text-blue-400 transition-colors"
                >
                  RBI Alert List & NBFC Directory
                  <ExternalLink className="h-3 w-3 text-slate-400" />
                </a>
              </li>
              <li>
                <a
                  href="https://www.mca.gov.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1.5 text-slate-300 hover:text-blue-400 transition-colors"
                >
                  MCA Company Master Data
                  <ExternalLink className="h-3 w-3 text-slate-400" />
                </a>
              </li>
              <li>
                <a
                  href="https://scores.sebi.gov.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1.5 text-slate-300 hover:text-blue-400 transition-colors"
                >
                  SEBI SCORES Grievance Portal
                  <ExternalLink className="h-3 w-3 text-slate-400" />
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h5 className="text-xs font-semibold text-white uppercase tracking-wider mb-3">
              Emergency & Cyber Reporting
            </h5>
            <ul className="space-y-2 text-xs">
              <li>
                <a
                  href="https://cybercrime.gov.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1.5 text-amber-300 hover:text-amber-200 transition-colors font-medium"
                >
                  National Cyber Crime Portal (1930)
                  <ExternalLink className="h-3 w-3" />
                </a>
              </li>
              <li>
                <a
                  href="https://sachet.rbi.org.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1.5 text-slate-300 hover:text-blue-400 transition-colors"
                >
                  RBI Sachet Fraud Reporting
                  <ExternalLink className="h-3 w-3 text-slate-400" />
                </a>
              </li>
              <li>
                <a
                  href="https://chakshe.sancharsaathi.gov.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1.5 text-slate-300 hover:text-blue-400 transition-colors"
                >
                  DoT Chakshu Malicious SMS Tool
                  <ExternalLink className="h-3 w-3 text-slate-400" />
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h5 className="text-xs font-semibold text-white uppercase tracking-wider mb-3">
              Trust Verification Principles
            </h5>
            <ul className="space-y-2 text-xs text-slate-400">
              <li className="flex items-start gap-2">
                <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400 shrink-0 mt-0.5" />
                <span>Multi-vector trust chain analysis</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400 shrink-0 mt-0.5" />
                <span>Transparent evidence citations</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400 shrink-0 mt-0.5" />
                <span>Explicit uncertainty indicators</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400 shrink-0 mt-0.5" />
                <span>Defensive safety recommendations</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom copyright & attribution */}
        <div className="pt-8 border-t border-slate-900 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-400">
          <p>© {new Date().getFullYear()} RakshaScan. Evidence-based financial scam & trust-verification platform.</p>
          <p className="text-center sm:text-right">
            Built for Indian consumer protection & retail investor awareness.
          </p>
        </div>
      </div>
    </footer>
  );
}
