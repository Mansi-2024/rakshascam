"use client";

import React, { createContext, useContext, useState } from "react";

import { Language, translations, Translations } from "./translations";

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  simpleMode: boolean;
  setSimpleMode: React.Dispatch<React.SetStateAction<boolean>>;
  t: Translations;
  simplifyText: (text: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguageState] = useState<Language>(() => {
    if (typeof window !== "undefined") {
      try {
        const savedLang = localStorage.getItem("rakshascan_lang") as Language;
        if (savedLang && (savedLang === "en" || savedLang === "hi" || savedLang === "mr")) {
          return savedLang;
        }
      } catch {
        // Storage access may be restricted
      }
    }
    return "en";
  });

  const [simpleMode, setSimpleMode] = useState<boolean>(() => {
    if (typeof window !== "undefined") {
      try {
        const savedSimple = localStorage.getItem("rakshascan_simple_mode");
        if (savedSimple !== null) {
          return savedSimple === "true";
        }
      } catch {
        // Storage access may be restricted
      }
    }
    return false;
  });


  const setLanguage = (lang: Language) => {
    setLanguageState(lang);
    try {
      localStorage.setItem("rakshascan_lang", lang);
    } catch {
      // Ignore storage errors
    }
  };

  const handleSetSimpleMode: React.Dispatch<React.SetStateAction<boolean>> = (value) => {
    setSimpleMode((prev) => {
      const next = typeof value === "function" ? value(prev) : value;
      try {
        localStorage.setItem("rakshascan_simple_mode", String(next));
      } catch {
        // Ignore storage errors
      }
      return next;
    });
  };

  /**
   * Plain-Language Simplifier:
   * Maps dense regulatory / legal jargon to conversational explanations
   * while strictly preserving epistemic uncertainty.
   */
  const simplifyText = (text: string): string => {
    if (!simpleMode || !text) return text;

    const lower = text.toLowerCase();

    if (language === "hi") {
      if (lower.includes("corroborat") || lower.includes("unverified") || lower.includes("अपुष्ट")) {
        return "हम आधिकारिक सरकारी रिकॉर्ड में इस दावे की पुष्टि नहीं कर पाए हैं।";
      }
      if (lower.includes("guaranteed") || lower.includes("गारंटीड")) {
        return "यह योजना बिना किसी जोखिम के निश्चित मुनाफ़े का वादा कर रही है, जो वित्तीय बाज़ार में संभव नहीं है।";
      }
      if (lower.includes("withdrawal fee") || lower.includes("निकासी शुल्क")) {
        return "अपने ही पैसे वापस निकालने के लिए अलग से शुल्क माँगना एक बड़ा ख़तरे का संकेत है।";
      }
      if (lower.includes("contradict") || lower.includes("असंगत")) {
        return "सरकारी रिकॉर्ड और इनके दावे में सीधा अंतर पाया गया है।";
      }
    } else if (language === "mr") {
      if (lower.includes("corroborat") || lower.includes("unverified") || lower.includes("अपुष्ट")) {
        return "अधिकृत सरकारी नोंदीमध्ये या दाव्याची पडताळणी होऊ शकलेली नाही.";
      }
      if (lower.includes("guaranteed") || lower.includes("हमी")) {
        return "ही योजना विनाधोका निश्चित नफ्याचे आमिष दाखवत आहे, जे बाजारात शक्य नसते.";
      }
      if (lower.includes("withdrawal fee") || lower.includes("शुल्क")) {
        return "स्वतःचे पैसे काढण्यासाठी आधी आणखी पैसे भरायला सांगणे हा फसवणुकीचा प्रकार असू शकतो.";
      }
    } else {
      // English simple mode
      if (lower.includes("authoritative corroboration was unavailable") || lower.includes("could not be independently corroborated")) {
        return "We could not confirm this claim using the available official source.";
      }
      if (lower.includes("unregistered intermediary")) {
        return "This entity is not listed as an approved advisor in the official registry.";
      }
      if (lower.includes("regulatory advertising norms")) {
        return "Official rules do not allow promising zero risk or guaranteed profits.";
      }
      if (lower.includes("advance fee deposits to withdraw your own principal")) {
        return "Real investment platforms never ask you to pay extra money just to get your own money back.";
      }
    }

    return text;
  };

  return (
    <LanguageContext.Provider
      value={{
        language,
        setLanguage,
        simpleMode,
        setSimpleMode: handleSetSimpleMode,
        t: translations[language],
        simplifyText,
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error("useLanguage must be used within a LanguageProvider");
  }
  return context;
}
