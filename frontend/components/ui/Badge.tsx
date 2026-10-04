import * as React from "react";
import { cn } from "@/lib/utils";
import { VerificationStatus, RiskSeverity } from "@/types";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "outline" | "secondary";
  status?: VerificationStatus;
  severity?: RiskSeverity;
  size?: "sm" | "md" | "lg";
}

export function StatusBadge({
  status,
  className,
  size = "md",
}: {
  status: VerificationStatus;
  className?: string;
  size?: "sm" | "md" | "lg";
}) {
  const sizeClasses = {
    sm: "px-2 py-0.5 text-xs font-medium tracking-wide",
    md: "px-2.5 py-1 text-xs font-semibold tracking-wider",
    lg: "px-3 py-1.5 text-sm font-semibold tracking-wider",
  };

  const statusStyles: Record<
    VerificationStatus,
    { bg: string; text: string; border: string; dot: string; label: string }
  > = {
    VERIFIED: {
      bg: "bg-emerald-950/60",
      text: "text-emerald-400",
      border: "border-emerald-700/60",
      dot: "bg-emerald-400",
      label: "VERIFIED",
    },
    UNVERIFIED: {
      bg: "bg-amber-950/50",
      text: "text-amber-400",
      border: "border-amber-700/60",
      dot: "bg-amber-400",
      label: "UNVERIFIED",
    },
    CONTRADICTORY: {
      bg: "bg-rose-950/60",
      text: "text-rose-400",
      border: "border-rose-700/60",
      dot: "bg-rose-400",
      label: "CONTRADICTORY",
    },
    UNKNOWN: {
      bg: "bg-slate-900/80",
      text: "text-slate-300",
      border: "border-slate-700",
      dot: "bg-slate-400",
      label: "UNKNOWN",
    },
  };

  const current = statusStyles[status] || statusStyles.UNKNOWN;

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-md border font-mono uppercase transition-colors",
        current.bg,
        current.text,
        current.border,
        sizeClasses[size],
        className
      )}
    >
      <span className={cn("h-1.5 w-1.5 rounded-full", current.dot)} />
      {current.label}
    </span>
  );
}

export function SeverityBadge({
  severity,
  className,
}: {
  severity: RiskSeverity;
  className?: string;
}) {
  const styles: Record<RiskSeverity, { bg: string; text: string; border: string; label: string }> = {
    LOW: {
      bg: "bg-blue-950/50",
      text: "text-blue-300",
      border: "border-blue-700/50",
      label: "LOW CONCERN",
    },
    MEDIUM: {
      bg: "bg-amber-950/60",
      text: "text-amber-300",
      border: "border-amber-600/60",
      label: "MEDIUM CONCERN",
    },
    HIGH: {
      bg: "bg-rose-950/70",
      text: "text-rose-300",
      border: "border-rose-600/70",
      label: "HIGH CONCERN",
    },
  };

  const current = styles[severity];

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-md border px-3 py-1 text-xs font-bold tracking-wider uppercase font-mono shadow-xs",
        current.bg,
        current.text,
        current.border,
        className
      )}
    >
      <span className="relative flex h-2 w-2">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-current opacity-60"></span>
        <span className="relative inline-flex rounded-full h-2 w-2 bg-current"></span>
      </span>
      {current.label}
    </span>
  );
}
