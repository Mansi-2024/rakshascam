"use client";

import * as React from "react";
import { ShieldAlert, ShieldCheck, Menu, X, Globe, Sparkles, PhoneCall } from "lucide-react";
import { useLanguage, Language } from "@/lib/i18n";

export function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);
  const { language, setLanguage, simpleMode, setSimpleMode, t } = useLanguage();

  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-800/80 bg-slate-950/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <a href="#" className="flex items-center gap-3 group">
            <div className="relative flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-blue-600/20 to-blue-500/10 border border-blue-500/40 text-blue-400 group-hover:border-blue-400/70 transition-all shadow-sm shadow-blue-900/20">
              <ShieldCheck className="h-5 w-5 text-blue-400 group-hover:scale-105 transition-transform" />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-lg tracking-tight text-white">{t.brandName}</span>
              <span className="text-[11px] text-slate-400 tracking-tight hidden sm:inline">
                {t.brandTagline}
              </span>
            </div>
          </a>
        </div>

        {/* Desktop Controls & Navigation */}
        <div className="hidden lg:flex items-center gap-7">
          <nav className="flex items-center gap-6 text-sm font-medium text-slate-300">
            <a
              href="#analyze"
              className="hover:text-blue-400 transition-colors focus-visible:outline-none focus-visible:text-blue-400 py-1"
            >
              {t.navAnalyze}
            </a>
            <a
              href="#trust-chain"
              className="hover:text-blue-400 transition-colors focus-visible:outline-none focus-visible:text-blue-400 py-1"
            >
              {t.trustChainTitle}
            </a>
            <a
              href="#safe-response"
              className="hover:text-blue-400 transition-colors focus-visible:outline-none focus-visible:text-blue-400 py-1"
            >
              Take Action
            </a>
          </nav>

          <div className="h-4 w-px bg-slate-800" />

          {/* Simple Mode Toggle */}
          <button
            type="button"
            onClick={() => setSimpleMode((prev) => !prev)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border transition-all ${
              simpleMode
                ? "bg-amber-500/15 border-amber-500/40 text-amber-300 shadow-sm shadow-amber-950/50"
                : "bg-slate-900 border-slate-700/60 text-slate-400 hover:text-slate-200 hover:border-slate-600"
            }`}
            title={t.simpleModeTooltip}
            id="simple-explanation-toggle"
          >
            <Sparkles className="h-3.5 w-3.5 text-amber-400" />
            <span>{t.simpleModeLabel}</span>
            <span className={`w-2 h-2 rounded-full ${simpleMode ? "bg-amber-400 animate-pulse" : "bg-slate-600"}`} />
          </button>

          {/* Language Switcher */}
          <div className="flex items-center bg-slate-900/90 border border-slate-800 rounded-lg p-0.5" id="language-switcher">
            <Globe className="h-3.5 w-3.5 text-slate-400 ml-2 mr-1" />
            {(
              [
                { code: "en", label: "English" },
                { code: "hi", label: "हिन्दी" },
                { code: "mr", label: "मराठी" },
              ] as const
            ).map((lang) => (
              <button
                key={lang.code}
                type="button"
                onClick={() => setLanguage(lang.code as Language)}
                className={`px-2.5 py-1 text-xs font-medium rounded-md transition-colors ${
                  language === lang.code
                    ? "bg-blue-600 text-white shadow-sm"
                    : "text-slate-400 hover:text-slate-200"
                }`}
                id={`lang-btn-${lang.code}`}
              >
                {lang.label}
              </button>
            ))}
          </div>
        </div>

        {/* Emergency Helpline */}
        <div className="hidden sm:flex items-center gap-3">
          <a
            href="tel:1930"
            className="flex items-center gap-2 rounded-lg border border-amber-900/50 bg-amber-950/30 hover:bg-amber-950/50 hover:border-amber-700/60 px-3 py-1.5 text-xs text-amber-300 transition-colors group"
            title="National Cyber Crime Reporting Helpline"
          >
            <ShieldAlert className="h-3.5 w-3.5 text-amber-400 shrink-0 group-hover:scale-110 transition-transform" />
            <span>Helpline: <strong className="text-white font-mono">1930</strong></span>
          </a>
        </div>

        {/* Mobile menu button */}
        <div className="flex lg:hidden items-center gap-2">
          {/* Simple Mode Toggle on mobile */}
          <button
            type="button"
            onClick={() => setSimpleMode((prev) => !prev)}
            className={`p-1.5 rounded-lg border text-xs ${
              simpleMode
                ? "bg-amber-500/20 border-amber-500/50 text-amber-300"
                : "bg-slate-900 border-slate-800 text-slate-400"
            }`}
            title={t.simpleModeLabel}
          >
            <Sparkles className="h-4 w-4" />
          </button>

          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 focus:outline-none"
            aria-expanded={mobileMenuOpen}
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-b border-slate-800 bg-slate-950 px-4 py-4 space-y-3 animate-fadeIn">
          <nav className="flex flex-col space-y-1 text-sm font-medium">
            <a
              href="#analyze"
              onClick={() => setMobileMenuOpen(false)}
              className="px-3 py-2 rounded-md hover:bg-slate-800 text-slate-200"
            >
              {t.navAnalyze}
            </a>
            <a
              href="#trust-chain"
              onClick={() => setMobileMenuOpen(false)}
              className="px-3 py-2 rounded-md hover:bg-slate-800 text-slate-200"
            >
              {t.trustChainTitle}
            </a>
            <a
              href="#safe-response"
              onClick={() => setMobileMenuOpen(false)}
              className="px-3 py-2 rounded-md hover:bg-slate-800 text-slate-200"
            >
              Take Action
            </a>
          </nav>
          <div className="pt-3 border-t border-slate-800/80 flex flex-col gap-2.5">
            <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-900 border border-slate-800">
              <span className="text-xs text-slate-400 flex items-center gap-1.5">
                <Globe className="h-3.5 w-3.5" /> {t.languageSelector}
              </span>
              <div className="flex gap-1">
                {(
                  [
                    { code: "en", label: "EN" },
                    { code: "hi", label: "हिन्दी" },
                    { code: "mr", label: "मराठी" },
                  ] as const
                ).map((lang) => (
                  <button
                    key={lang.code}
                    type="button"
                    onClick={() => {
                      setLanguage(lang.code as Language);
                      setMobileMenuOpen(false);
                    }}
                    className={`px-2.5 py-1 text-xs font-medium rounded ${
                      language === lang.code
                        ? "bg-blue-600 text-white"
                        : "text-slate-400 hover:text-white"
                    }`}
                  >
                    {lang.label}
                  </button>
                ))}
              </div>
            </div>
            <a
              href="tel:1930"
              className="flex items-center justify-between gap-2 rounded-lg border border-amber-900/60 bg-amber-950/40 p-2.5 text-xs text-amber-300"
            >
              <div className="flex items-center gap-2">
                <ShieldAlert className="h-4 w-4 text-amber-400 shrink-0" />
                <span>Cybercrime Helpline</span>
              </div>
              <span className="font-mono font-bold text-white flex items-center gap-1">
                <PhoneCall className="h-3 w-3" /> 1930
              </span>
            </a>
          </div>
        </div>
      )}
    </header>
  );
}
