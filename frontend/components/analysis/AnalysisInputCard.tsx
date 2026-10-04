"use client";

import * as React from "react";
import {
  Globe,
  Image as ImageIcon,
  MessageSquare,
  Building2,
  Sparkles,
  AlertCircle,
  Shield,
  Upload,
  X,
  FileCheck,
  Lock,
  ArrowRight,
  ShieldCheck,
} from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card, CardContent } from "@/components/ui/Card";
import { AnalysisInputMode } from "@/types";
import { useLanguage } from "@/lib/i18n";

interface AnalysisInputCardProps {
  onAnalyze: (inputVal: string, mode?: AnalysisInputMode, file?: File | null) => void;
  isAnalyzing: boolean;
  externalError?: string | null;
}

export function AnalysisInputCard({ onAnalyze, isAnalyzing, externalError }: AnalysisInputCardProps) {
  const { t } = useLanguage();
  // Default to Message Analysis as requested for strongest Bharat-first hackathon demo
  const [activeTab, setActiveTab] = React.useState<AnalysisInputMode>("message");

  const [urlInput, setUrlInput] = React.useState("");
  const [messageInput, setMessageInput] = React.useState("");
  const [entityInput, setEntityInput] = React.useState("");
  const [selectedFile, setSelectedFile] = React.useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = React.useState<string | null>(null);
  const [isDragging, setIsDragging] = React.useState(false);
  const [inputError, setInputError] = React.useState<string | null>(null);

  const fileInputRef = React.useRef<HTMLInputElement>(null);

  // Clear preview URL on unmount
  React.useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  const handleFileSelection = (file: File) => {
    setInputError(null);
    const validTypes = ["image/png", "image/jpeg", "image/jpg", "image/webp"];
    if (!validTypes.includes(file.type.toLowerCase())) {
      setInputError("Unsupported file type. Please upload a PNG, JPEG, or WEBP image.");
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setInputError("File size exceeds 10MB limit. Please upload a smaller image.");
      return;
    }

    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }

    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelection(e.target.files[0]);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelection(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleClearFile = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setSelectedFile(null);
    setPreviewUrl(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleGenerateFictionalScreenshot = () => {
    const canvas = document.createElement("canvas");
    canvas.width = 720;
    canvas.height = 380;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Background gradient
    const gradient = ctx.createLinearGradient(0, 0, 720, 380);
    gradient.addColorStop(0, "#0f172a");
    gradient.addColorStop(1, "#1e293b");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 720, 380);

    // Accent line
    ctx.fillStyle = "#3b82f6";
    ctx.fillRect(0, 0, 720, 6);

    // Header badge
    ctx.fillStyle = "#1e3a8a";
    ctx.fillRect(40, 30, 260, 28);
    ctx.fillStyle = "#93c5fd";
    ctx.font = "bold 13px sans-serif";
    ctx.fillText("FICTIONAL PROMOTIONAL OFFER", 50, 49);

    // Text items
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 22px sans-serif";
    ctx.fillText("Example Wealth Advisors Pvt Ltd", 40, 95);

    ctx.fillStyle = "#38bdf8";
    ctx.font = "15px monospace";
    ctx.fillText("SEBI Registration Claim: INA000099999", 40, 130);

    ctx.fillStyle = "#facc15";
    ctx.font = "bold 18px sans-serif";
    ctx.fillText("Guaranteed 35% Monthly Returns with Zero Risk", 40, 175);

    ctx.fillStyle = "#cbd5e1";
    ctx.font = "14px sans-serif";
    ctx.fillText("Institutional allocation quota: Only 5 investor slots remaining.", 40, 215);

    ctx.fillStyle = "#f87171";
    ctx.font = "bold 15px sans-serif";
    ctx.fillText("Deposit ₹50,000 today to activate your high-yield account.", 40, 255);

    ctx.fillStyle = "#94a3b8";
    ctx.font = "13px sans-serif";
    ctx.fillText("Standard withdrawal policy: account subject to tax clearance fee.", 40, 290);

    ctx.fillStyle = "#64748b";
    ctx.font = "11px sans-serif";
    ctx.fillText("Portal: https://example-finance.test | Contact: support@example-finance.test", 40, 345);

    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], "fictional_demo_screenshot.png", { type: "image/png" });
        handleFileSelection(file);
      }
    }, "image/png");
  };

  const handleUseDemo = () => {
    if (activeTab === "message") {
      const demoMessage =
        "URGENT: SEBI approved guaranteed investment opportunity.\n" +
        "Earn 25% monthly with zero risk.\n" +
        "Only 10 investor slots remaining.\n" +
        "Deposit ₹20,000 today to activate your account.\n" +
        "To withdraw your profit, pay a refundable processing tax.\n" +
        "Official portal: https://example-finance.test";
      setMessageInput(demoMessage);
      setInputError(null);
      onAnalyze(demoMessage, "message");
    } else if (activeTab === "screenshot") {
      handleGenerateFictionalScreenshot();
    } else if (activeTab === "website") {
      const demoUrl = "https://example-finance.test";
      setUrlInput(demoUrl);
      setInputError(null);
      onAnalyze(demoUrl, "website");
    } else {
      const demoEntity = "Example Wealth Advisors Private Limited";
      setEntityInput(demoEntity);
      setInputError(null);
      onAnalyze(demoEntity, "entity");
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setInputError(null);

    if (activeTab === "message") {
      const trimmed = messageInput.trim();
      if (!trimmed) {
        setInputError("Please paste or type message content to analyze.");
        return;
      }
      if (trimmed.length > 15000) {
        setInputError("Message exceeds 15,000 characters maximum limit.");
        return;
      }
      onAnalyze(trimmed, "message");
    } else if (activeTab === "screenshot") {
      if (!selectedFile) {
        setInputError("Please select or drop a screenshot image file to analyze.");
        return;
      }
      onAnalyze(selectedFile.name, "screenshot", selectedFile);
    } else if (activeTab === "website") {
      const trimmed = urlInput.trim();
      if (!trimmed) {
        setInputError("Please enter a valid website URL or try the demo link below.");
        return;
      }
      onAnalyze(trimmed, "website");
    } else {
      const trimmed = entityInput.trim();
      if (!trimmed) {
        setInputError("Please enter an entity name or registration code.");
        return;
      }
      onAnalyze(trimmed, "entity");
    }
  };

  return (
    <div id="analyze" className="w-full max-w-4xl mx-auto px-4 sm:px-6 scroll-mt-20">
      <Card className="border-slate-800 bg-slate-900/95 shadow-2xl relative overflow-hidden backdrop-blur-xl">
        {/* Accent top gradient bar */}
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-600 via-cyan-400 to-blue-600" />

        <CardContent className="p-6 sm:p-8">
          {/* Card Header */}
          <div className="mb-6 space-y-1">
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-5 w-5 text-blue-400" />
              <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-white">
                What do you want to verify?
              </h2>
            </div>
            <p className="text-xs sm:text-sm text-slate-300">
              Submit a financial message, screenshot, website, or entity to trace the evidence behind the claim.
            </p>
          </div>

          {/* Unified 4-Mode Segmented Control */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-1.5 p-1 rounded-xl bg-slate-950/80 border border-slate-800/90">
            <button
              type="button"
              onClick={() => {
                setActiveTab("message");
                setInputError(null);
              }}
              className={`flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg text-xs sm:text-sm font-medium transition-all ${
                activeTab === "message"
                  ? "bg-blue-600 text-white shadow-md shadow-blue-900/40 font-semibold"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/70"
              }`}
            >
              <MessageSquare className="h-4 w-4 shrink-0" />
              <span>{t.tabMessage}</span>
            </button>

            <button
              type="button"
              onClick={() => {
                setActiveTab("screenshot");
                setInputError(null);
              }}
              className={`flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg text-xs sm:text-sm font-medium transition-all ${
                activeTab === "screenshot"
                  ? "bg-blue-600 text-white shadow-md shadow-blue-900/40 font-semibold"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/70"
              }`}
            >
              <ImageIcon className="h-4 w-4 shrink-0" />
              <span>{t.tabScreenshot}</span>
            </button>

            <button
              type="button"
              onClick={() => {
                setActiveTab("website");
                setInputError(null);
              }}
              className={`flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg text-xs sm:text-sm font-medium transition-all ${
                activeTab === "website"
                  ? "bg-blue-600 text-white shadow-md shadow-blue-900/40 font-semibold"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/70"
              }`}
            >
              <Globe className="h-4 w-4 shrink-0" />
              <span>{t.tabUrl}</span>
            </button>

            <button
              type="button"
              onClick={() => {
                setActiveTab("entity");
                setInputError(null);
              }}
              className={`flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg text-xs sm:text-sm font-medium transition-all ${
                activeTab === "entity"
                  ? "bg-blue-600 text-white shadow-md shadow-blue-900/40 font-semibold"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/70"
              }`}
            >
              <Building2 className="h-4 w-4 shrink-0" />
              <span>Entity / License</span>
            </button>
          </div>

          {/* TAB 1: COPIED MESSAGE (DEFAULT ACTIVE) */}
          {activeTab === "message" && (
            <form onSubmit={handleSubmit} className="mt-6 space-y-4">
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <label htmlFor="message-input" className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
                    Paste Suspicious Chat Message, SMS, or Promotion
                  </label>
                  <span className="text-[11px] text-slate-400 font-mono">
                    {messageInput.length.toLocaleString()} / 15,000 characters
                  </span>
                </div>

                <textarea
                  id="message-input"
                  rows={5}
                  value={messageInput}
                  maxLength={15000}
                  onChange={(e) => {
                    setMessageInput(e.target.value);
                    if (inputError) setInputError(null);
                  }}
                  placeholder="Paste promotional chat message from WhatsApp, Telegram, or SMS... (e.g. 'URGENT: SEBI approved guaranteed investment opportunity. Earn 25% monthly with zero risk. Deposit ₹20,000 today to activate your account...')"
                  className="w-full px-4 py-3.5 rounded-xl bg-slate-950 border border-slate-700/80 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all font-sans leading-relaxed"
                />
              </div>

              <div className="flex flex-wrap items-center justify-between gap-3 pt-1">
                <button
                  type="button"
                  onClick={handleUseDemo}
                  className="inline-flex items-center gap-1.5 text-xs text-slate-300 hover:text-white bg-slate-800/80 hover:bg-slate-700 px-3.5 py-2 rounded-lg border border-slate-700 transition-colors"
                >
                  <Sparkles className="h-3.5 w-3.5 text-amber-400" />
                  <span>Try demo message</span>
                </button>

                <Button
                  type="submit"
                  variant="primary"
                  size="lg"
                  isLoading={isAnalyzing}
                  className="h-11 px-6 shadow-lg shadow-blue-900/30"
                >
                  {!isAnalyzing && <ArrowRight className="h-4 w-4 mr-2" />}
                  Analyze with RakshaScan →
                </Button>
              </div>

              {/* Privacy/Safety Note */}
              <div className="pt-2 text-[11px] text-slate-400 flex items-center gap-2 border-t border-slate-800/60">
                <Lock className="h-3.5 w-3.5 text-slate-500 shrink-0" />
                <span>Your submitted content is processed for analysis and is not used to collect passwords, OTPs, PINs or CVVs.</span>
              </div>
            </form>
          )}

          {/* TAB 2: SCREENSHOT / LOCAL OCR */}
          {activeTab === "screenshot" && (
            <form onSubmit={handleSubmit} className="mt-6 space-y-4">
              <div className="flex items-center justify-between">
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
                  Upload Screenshot of Claim, Promotion, or Chat
                </label>
                <span className="text-[11px] text-emerald-400 font-mono bg-emerald-950/60 px-2.5 py-0.5 rounded border border-emerald-700/50 flex items-center gap-1.5">
                  <Lock className="h-3 w-3" />
                  100% Local & Offline OCR
                </span>
              </div>

              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                accept="image/png,image/jpeg,image/webp"
                className="hidden"
                id="screenshot-file-picker"
              />

              {!selectedFile ? (
                <div
                  onDrop={handleDrop}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onClick={() => fileInputRef.current?.click()}
                  className={`border-2 border-dashed rounded-xl p-8 text-center transition-all cursor-pointer group ${
                    isDragging
                      ? "border-blue-500 bg-blue-950/30 scale-[1.01]"
                      : "border-slate-700/80 hover:border-slate-500 bg-slate-950/40"
                  }`}
                >
                  <div className="mx-auto h-12 w-12 rounded-full bg-slate-800 flex items-center justify-center text-slate-400 group-hover:text-blue-400 transition-colors mb-3">
                    <Upload className="h-6 w-6" />
                  </div>
                  <p className="text-sm font-medium text-slate-200">
                    Drag and drop screenshot here, or <span className="text-blue-400 underline">browse files</span>
                  </p>
                  <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
                    Supports PNG, JPEG, or WEBP up to 10MB. Images are analyzed in-memory and never stored on disk or cloud vision servers.
                  </p>
                </div>
              ) : (
                <div className="p-4 rounded-xl border border-slate-700 bg-slate-950/80 flex flex-col sm:flex-row items-center justify-between gap-4">
                  <div className="flex items-center gap-3 w-full sm:w-auto">
                    {previewUrl ? (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img
                        src={previewUrl}
                        alt="Screenshot Preview"
                        className="h-16 w-20 object-cover rounded-lg border border-slate-700 shrink-0 bg-slate-900"
                      />
                    ) : (
                      <div className="h-16 w-20 rounded-lg bg-slate-800 flex items-center justify-center text-slate-400">
                        <ImageIcon className="h-8 w-8" />
                      </div>
                    )}
                    <div className="space-y-1 min-w-0">
                      <p className="text-sm font-semibold text-white truncate max-w-xs sm:max-w-md">
                        {selectedFile.name}
                      </p>
                      <p className="text-xs text-slate-400 font-mono">
                        {(selectedFile.size / 1024).toFixed(1)} KB • {selectedFile.type || "image/png"}
                      </p>
                      <span className="inline-flex items-center gap-1 text-[10px] text-emerald-400 font-mono">
                        <FileCheck className="h-3 w-3" /> Ready for Local OCR
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0 w-full sm:w-auto justify-end">
                    <button
                      type="button"
                      onClick={() => fileInputRef.current?.click()}
                      className="text-xs text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 px-3 py-2 rounded-lg border border-slate-700 transition-colors"
                    >
                      Replace
                    </button>
                    <button
                      type="button"
                      onClick={handleClearFile}
                      className="text-xs text-rose-300 hover:text-rose-200 bg-rose-950/60 hover:bg-rose-900/80 px-3 py-2 rounded-lg border border-rose-800/60 transition-colors flex items-center gap-1"
                    >
                      <X className="h-3.5 w-3.5" /> Remove
                    </button>
                  </div>
                </div>
              )}

              {/* Safety notice disclaimer */}
              <div className="p-3 rounded-lg border border-amber-900/60 bg-amber-950/30 text-amber-300/90 text-xs flex items-start gap-2.5">
                <AlertCircle className="h-4 w-4 shrink-0 mt-0.5 text-amber-400" />
                <p>
                  <strong>Safety Notice:</strong> Do not upload OTPs, passwords, banking credentials, card details, or other sensitive authentication information.
                </p>
              </div>

              <div className="flex flex-wrap items-center justify-between gap-3 pt-1">
                <button
                  type="button"
                  onClick={handleGenerateFictionalScreenshot}
                  className="inline-flex items-center gap-1.5 text-xs text-slate-300 hover:text-white bg-slate-800/80 hover:bg-slate-700 px-3.5 py-2 rounded-lg border border-slate-700 transition-colors"
                >
                  <Sparkles className="h-3.5 w-3.5 text-amber-400" />
                  <span>Try demo screenshot</span>
                </button>

                <Button
                  type="submit"
                  variant="primary"
                  size="lg"
                  isLoading={isAnalyzing}
                  disabled={!selectedFile}
                  className="h-11 px-6 shadow-lg shadow-blue-900/30"
                >
                  {!isAnalyzing && <ArrowRight className="h-4 w-4 mr-2" />}
                  Analyze with RakshaScan →
                </Button>
              </div>

              {/* Privacy/Safety Note */}
              <div className="pt-2 text-[11px] text-slate-400 flex items-center gap-2 border-t border-slate-800/60">
                <Lock className="h-3.5 w-3.5 text-slate-500 shrink-0" />
                <span>Images are analyzed locally in-memory and are never stored or used to extract confidential credentials.</span>
              </div>
            </form>
          )}

          {/* TAB 3: WEBSITE URL */}
          {activeTab === "website" && (
            <form onSubmit={handleSubmit} className="mt-6 space-y-4">
              <div className="space-y-1.5">
                <label htmlFor="url-input" className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
                  Target Website or Investment Portal URL
                </label>
                <div className="relative flex flex-col sm:flex-row gap-3">
                  <div className="relative flex-1">
                    <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                      <Globe className="h-5 w-5" />
                    </div>
                    <input
                      id="url-input"
                      type="text"
                      value={urlInput}
                      onChange={(e) => {
                        setUrlInput(e.target.value);
                        if (inputError) setInputError(null);
                      }}
                      placeholder="Paste a financial website URL... (e.g., https://example-finance.test)"
                      className="w-full pl-11 pr-4 py-3.5 rounded-xl bg-slate-950 border border-slate-700/80 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                      aria-label="Financial website URL"
                    />
                  </div>
                  <Button
                    type="submit"
                    variant="primary"
                    size="lg"
                    isLoading={isAnalyzing}
                    className="shrink-0 h-12 px-6 shadow-lg shadow-blue-900/30"
                  >
                    {!isAnalyzing && <ArrowRight className="h-4 w-4 mr-2" />}
                    Analyze with RakshaScan →
                  </Button>
                </div>
              </div>

              {/* Demo Helper Prompt */}
              <div className="flex flex-wrap items-center justify-between gap-3 pt-1 text-xs text-slate-400">
                <div className="flex items-center gap-2">
                  <span className="text-slate-500">Fictional demonstration target:</span>
                  <button
                    type="button"
                    onClick={handleUseDemo}
                    className="font-mono text-blue-400 hover:text-blue-300 underline decoration-blue-500/50 hover:decoration-blue-300 transition-colors"
                  >
                    https://example-finance.test
                  </button>
                </div>
                <button
                  type="button"
                  onClick={handleUseDemo}
                  className="inline-flex items-center gap-1.5 text-xs text-slate-300 hover:text-white bg-slate-800/80 hover:bg-slate-700 px-3.5 py-2 rounded-lg border border-slate-700 transition-colors"
                >
                  <Sparkles className="h-3.5 w-3.5 text-amber-400" />
                  <span>Try demo website</span>
                </button>
              </div>

              {/* Privacy/Safety Note */}
              <div className="pt-2 text-[11px] text-slate-400 flex items-center gap-2 border-t border-slate-800/60">
                <Lock className="h-3.5 w-3.5 text-slate-500 shrink-0" />
                <span>External website fetch utilizes isolated SSRF protections without sending authentication tokens.</span>
              </div>
            </form>
          )}

          {/* TAB 4: ENTITY / REGISTRATION NUMBER */}
          {activeTab === "entity" && (
            <div className="mt-6 space-y-4">
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <label htmlFor="entity-input" className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
                    Company Name, SEBI License, or MCA CIN
                  </label>
                  <span className="text-[11px] text-blue-400/90 font-mono bg-blue-950/40 px-2 py-0.5 rounded border border-blue-800/40">
                    Registry Ingestion
                  </span>
                </div>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                    <Building2 className="h-5 w-5" />
                  </div>
                  <input
                    id="entity-input"
                    type="text"
                    value={entityInput}
                    onChange={(e) => {
                      setEntityInput(e.target.value);
                      if (inputError) setInputError(null);
                    }}
                    placeholder="e.g. INA000099999 or Example Wealth Advisors Pvt Ltd"
                    className="w-full pl-11 pr-4 py-3 rounded-xl bg-slate-950 border border-slate-700 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  />
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-between gap-3 pt-1">
                <button
                  type="button"
                  onClick={handleUseDemo}
                  className="inline-flex items-center gap-1.5 text-xs text-slate-300 hover:text-white bg-slate-800/80 hover:bg-slate-700 px-3.5 py-2 rounded-lg border border-slate-700 transition-colors"
                >
                  <Sparkles className="h-3.5 w-3.5 text-amber-400" />
                  <span>Try demo entity</span>
                </button>

                <Button
                  type="button"
                  variant="primary"
                  size="md"
                  onClick={handleSubmit}
                  isLoading={isAnalyzing}
                  className="h-11 px-6 shadow-lg shadow-blue-900/30"
                >
                  {!isAnalyzing && <ArrowRight className="h-4 w-4 mr-2" />}
                  Analyze with RakshaScan →
                </Button>
              </div>

              {/* Privacy/Safety Note */}
              <div className="pt-2 text-[11px] text-slate-400 flex items-center gap-2 border-t border-slate-800/60">
                <Lock className="h-3.5 w-3.5 text-slate-500 shrink-0" />
                <span>Statutory lookup cross-references cached regulatory indexes without sharing user inquiries.</span>
              </div>
            </div>
          )}

          {/* Error Message Alert */}
          {(inputError || externalError) && (
            <div className="mt-4 p-3 rounded-lg border border-rose-900/60 bg-rose-950/30 text-rose-300 text-xs flex items-center justify-between gap-2 animate-fadeIn">
              <div className="flex items-center gap-2 min-w-0">
                <AlertCircle className="h-4 w-4 shrink-0 text-rose-400" />
                <span className="truncate">{inputError || externalError}</span>
              </div>
              <button
                type="button"
                onClick={() => {
                  setInputError(null);
                  if (activeTab === "website") setUrlInput("");
                  if (activeTab === "message") setMessageInput("");
                  if (activeTab === "screenshot") handleClearFile();
                }}
                className="text-[11px] text-rose-400 hover:text-rose-200 underline font-medium shrink-0 ml-2 cursor-pointer"
                aria-label="Dismiss error"
              >
                Clear
              </button>
            </div>
          )}

          {/* Multi-step Loading Indicator */}
          {isAnalyzing && (
            <div className="mt-6 pt-5 border-t border-slate-800/80 animate-fadeIn">
              <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
                <span className="font-mono text-blue-400 font-medium flex items-center gap-2">
                  <span className="h-2 w-2 rounded-full bg-blue-500 animate-ping" />
                  Running structured intelligence & evidence pipeline...
                </span>
                <span className="font-mono text-slate-400">Unified Verification Pipeline</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                <div className="bg-blue-500 h-1.5 rounded-full animate-pulse w-3/4" />
              </div>
              <p className="text-[11px] text-slate-500 mt-2 font-mono">
                Pipeline: Input Normalization → Structured Extraction → Statutory Verification → Evidence Provenance → Trust Chain → Scam Journey
              </p>
            </div>
          )}

          {/* Architectural note footer */}
          <div className="mt-6 pt-4 border-t border-slate-800/60 flex items-start gap-2.5 text-xs text-slate-400">
            <Shield className="h-4 w-4 text-blue-400 shrink-0 mt-0.5" />
            <p>
              <strong>Single Unified Engine:</strong> All input modes feed into the same structured extraction, statutory verification, Financial Trust Chain, and Scam Journey analysis.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
