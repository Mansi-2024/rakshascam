"use client";

import * as React from "react";
import {
  TrustChainGraphData,
  TrustChainNodeData,
  TrustChainRelationshipData,
  TrustChainNode,
  TrustChainRelationship,
  EvidenceItem,
  VerificationResult,
} from "@/types";
import {
  FileText,
  Building,
  Award,
  UserCheck,
  Globe,
  Smartphone,
  Share2,
  CreditCard,
  CheckCircle2,
  AlertTriangle,
  AlertCircle,
  HelpCircle,
  EyeOff,
  ArrowRight,
  ArrowDown,
  Info,
  ShieldCheck,
  X,
} from "lucide-react";

interface TrustChainVisualizerProps {
  graph?: TrustChainGraphData;
  nodes?: TrustChainNode[];
  relationships?: TrustChainRelationship[];
  evidenceList?: EvidenceItem[];
  verificationResults?: VerificationResult[];
}

export function TrustChainVisualizer({
  graph,
  nodes: legacyNodes,
  relationships: legacyRelationships,
  evidenceList = [],
  verificationResults = [],
}: TrustChainVisualizerProps) {
  // Normalize graph nodes
  const nodes: TrustChainNodeData[] = React.useMemo(() => {
    if (graph && graph.nodes && graph.nodes.length > 0) {
      return graph.nodes;
    }
    if (legacyNodes && legacyNodes.length > 0) {
      return legacyNodes.map((n) => ({
        node_id: n.id,
        node_type: n.type.toUpperCase(),
        label: n.label,
        value: n.claimedValue || n.details || n.description || n.label,
        status: n.status,
        evidence_ids: n.evidenceList ? n.evidenceList.map((e) => e.id) : [],
        verification_ids: [],
        metadata: {},
      }));
    }
    return [];
  }, [graph, legacyNodes]);

  // Normalize graph relationships
  const relationships: TrustChainRelationshipData[] = React.useMemo(() => {
    if (graph && graph.relationships && graph.relationships.length > 0) {
      return graph.relationships;
    }
    if (legacyRelationships && legacyRelationships.length > 0) {
      return legacyRelationships.map((r, idx) => ({
        relationship_id: `legacy-rel-${idx}`,
        source_node_id: r.fromNodeId,
        target_node_id: r.toNodeId,
        relationship_type: r.relationType.toUpperCase(),
        status: r.status,
        evidence_ids: [],
        verification_ids: [],
        explanation: r.notes || "Observed relationship",
      }));
    }
    return [];
  }, [graph, legacyRelationships]);

  // Selected item for drawer/modal
  const [selectedNode, setSelectedNode] = React.useState<TrustChainNodeData | null>(null);
  const [selectedRel, setSelectedRel] = React.useState<TrustChainRelationshipData | null>(null);

  // Dynamic summary calculation from actual relationships
  const summary = React.useMemo(() => {
    const totalRel = relationships.length;
    const verified = relationships.filter((r) => r.status.toUpperCase() === "VERIFIED").length;
    const contradictory = relationships.filter((r) => r.status.toUpperCase() === "CONTRADICTORY").length;
    const unverified = relationships.filter((r) => r.status.toUpperCase() === "UNVERIFIED").length;
    const unknown = relationships.filter((r) => r.status.toUpperCase() === "UNKNOWN").length;
    const unobserved = relationships.filter(
      (r) => r.status.toUpperCase() === "NOT_OBSERVED" || r.status.toUpperCase() === "UNAVAILABLE"
    ).length;

    return {
      totalRel,
      verified,
      contradictory,
      unverified,
      unknown,
      unobserved,
    };
  }, [relationships]);

function renderNodeIcon(type: string, className: string = "h-4 w-4") {
  const t = type.toUpperCase();
  switch (t) {
    case "CLAIM":
      return <FileText className={className} />;
    case "ENTITY":
      return <Building className={className} />;
    case "REGISTRATION":
      return <Award className={className} />;
    case "OFFICIAL_IDENTITY":
      return <UserCheck className={className} />;
    case "WEBSITE":
      return <Globe className={className} />;
    case "APP":
      return <Smartphone className={className} />;
    case "SOCIAL_ACCOUNT":
      return <Share2 className={className} />;
    case "PAYMENT_IDENTITY":
      return <CreditCard className={className} />;
    default:
      return <FileText className={className} />;
  }
}

  const getStatusBadge = (status: string) => {
    const s = status.toUpperCase();
    if (s === "VERIFIED") {
      return {
        label: "VERIFIED",
        border: "border-emerald-500/70",
        bg: "bg-emerald-950/80 text-emerald-300",
        icon: <CheckCircle2 className="h-3 w-3 text-emerald-400" />,
      };
    }
    if (s === "CONTRADICTORY") {
      return {
        label: "CONTRADICTORY",
        border: "border-rose-500/80",
        bg: "bg-rose-950/80 text-rose-300",
        icon: <AlertTriangle className="h-3 w-3 text-rose-400" />,
      };
    }
    if (s === "UNVERIFIED") {
      return {
        label: "UNVERIFIED",
        border: "border-amber-500/70",
        bg: "bg-amber-950/80 text-amber-300",
        icon: <AlertCircle className="h-3 w-3 text-amber-400" />,
      };
    }
    if (s === "NOT_OBSERVED") {
      return {
        label: "NOT OBSERVED",
        border: "border-slate-700",
        bg: "bg-slate-900/80 text-slate-400",
        icon: <EyeOff className="h-3 w-3 text-slate-400" />,
      };
    }
    return {
      label: "UNKNOWN",
      border: "border-slate-600/70",
      bg: "bg-slate-900/80 text-slate-300",
      icon: <HelpCircle className="h-3 w-3 text-slate-400" />,
    };
  };

  // Find relationship between consecutive nodes in the 8-node chain
  const findRelationshipBetween = (sourceId: string, targetId: string) => {
    return relationships.find(
      (r) =>
        (r.source_node_id === sourceId && r.target_node_id === targetId) ||
        (r.source_node_id === targetId && r.target_node_id === sourceId)
    );
  };

  // Evidence lookup helper
  const getEvidenceById = (eid: string) => {
    return evidenceList.find((e) => e.id === eid);
  };

  // Verification lookup helper
  const getVerificationById = (vid: string) => {
    return verificationResults.find((v) => v.id === vid);
  };

  return (
    <div className="space-y-6">
      {/* FINANCIAL TRUST CHAIN HEADER & DYNAMIC SUMMARY */}
      <div className="p-5 rounded-2xl border border-slate-800 bg-slate-950/90 shadow-xl space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800/80 pb-3">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-5 w-5 text-blue-400" />
              <h3 className="text-base sm:text-lg font-bold text-white tracking-wide uppercase">
                Financial Trust Chain
              </h3>
            </div>
            <p className="text-xs text-slate-400">
              Deterministic provenance graph tracing claimed assertions to authoritative institutional records.
              Relationships are established <strong>only when supported by available evidence</strong>.
            </p>
          </div>

          <div className="text-xs font-mono px-3 py-1.5 rounded-lg bg-blue-950/60 border border-blue-800/50 text-blue-300 self-start sm:self-center shrink-0">
            {summary.totalRel} Relationships Analyzed
          </div>
        </div>

        {/* Dynamic Calculated Relationship Counts Bar */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 text-xs font-mono">
          <div className="p-2.5 rounded-xl bg-emerald-950/40 border border-emerald-900/60 flex items-center justify-between">
            <span className="text-slate-400">Verified</span>
            <span className="text-emerald-400 font-bold text-sm">{summary.verified}</span>
          </div>
          <div className="p-2.5 rounded-xl bg-amber-950/40 border border-amber-900/60 flex items-center justify-between">
            <span className="text-slate-400">Unverified</span>
            <span className="text-amber-400 font-bold text-sm">{summary.unverified}</span>
          </div>
          <div className="p-2.5 rounded-xl bg-rose-950/40 border border-rose-900/60 flex items-center justify-between">
            <span className="text-slate-400">Contradictory</span>
            <span className="text-rose-400 font-bold text-sm">{summary.contradictory}</span>
          </div>
          <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
            <span className="text-slate-400">Unknown</span>
            <span className="text-slate-200 font-bold text-sm">{summary.unknown}</span>
          </div>
          <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between col-span-2 sm:col-span-1">
            <span className="text-slate-400">Unobserved</span>
            <span className="text-slate-400 font-bold text-sm">{summary.unobserved}</span>
          </div>
        </div>

        {/* Status Propagation Policy Banner */}
        <div className="p-3 rounded-lg bg-slate-900/40 border border-slate-800/60 text-[11px] text-slate-400 flex items-start gap-2">
          <Info className="h-4 w-4 text-blue-400 shrink-0 mt-0.5" />
          <span>
            <strong>Propagation Rule:</strong> Node and relationship statuses do not automatically cascade. An authoritative statutory registration does NOT verify an unlisted website, nor does a live website authenticate corporate standing.
          </span>
        </div>
      </div>

      {/* GRAPH VISUALIZATION: DESKTOP & MOBILE RESPONSIVE */}
      <div className="space-y-4">
        {/* DESKTOP (Grid Flow) */}
        <div className="hidden lg:block space-y-4">
          <div className="grid grid-cols-4 gap-4">
            {nodes.slice(0, 4).map((node, index) => {
              const badge = getStatusBadge(node.status);
              const nextNode = nodes[index + 1];
              const rel = nextNode ? findRelationshipBetween(node.node_id, nextNode.node_id) : undefined;
              const isSelected = selectedNode?.node_id === node.node_id;

              return (
                <div key={node.node_id} className="relative flex flex-col">
                  {/* Node Card */}
                  <div
                    onClick={() => {
                      setSelectedNode(node);
                      setSelectedRel(null);
                    }}
                    className={`p-4 rounded-xl border transition-all cursor-pointer bg-slate-900/80 hover:bg-slate-800/80 ${
                      isSelected
                        ? "ring-2 ring-blue-500 border-blue-400 shadow-lg shadow-blue-500/10"
                        : `${badge.border} hover:border-slate-600`
                    }`}
                  >
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <div className="flex items-center gap-2">
                        <div className="p-2 rounded-lg bg-slate-800/80 text-blue-400 border border-slate-700/60">
                          {renderNodeIcon(node.node_type, "h-4 w-4")}
                        </div>
                        <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 font-semibold">
                          {node.node_type.replace("_", " ")}
                        </span>
                      </div>
                      <span
                        className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${badge.bg} ${badge.border}`}
                      >
                        {badge.icon}
                        <span>{badge.label}</span>
                      </span>
                    </div>

                    <h5 className="text-xs font-semibold text-slate-300 mb-1">{node.label}</h5>
                    <p className="text-xs text-white font-mono break-words line-clamp-2" title={node.value}>
                      {node.value}
                    </p>

                    <div className="mt-3 pt-2.5 border-t border-slate-800/80 flex items-center justify-between text-[10px] font-mono text-slate-400">
                      <span>Click to inspect details</span>
                      {node.evidence_ids.length > 0 && (
                        <span className="text-blue-400">{node.evidence_ids.length} Evidence</span>
                      )}
                    </div>
                  </div>

                  {/* Relationship Indicator to Next Node in row */}
                  {index < 3 && rel && (
                    <div className="mt-2 text-center">
                      <button
                        type="button"
                        onClick={() => {
                          setSelectedRel(rel);
                          setSelectedNode(null);
                        }}
                        className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-mono border transition-all ${
                          getStatusBadge(rel.status).bg
                        } ${getStatusBadge(rel.status).border} hover:scale-105`}
                      >
                        <span>{rel.relationship_type}</span>
                        <ArrowRight className="h-3 w-3" />
                      </button>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Row Connector Indicator from row 1 to row 2 */}
          {nodes.length > 4 && (
            <div className="flex justify-end pr-8">
              {(() => {
                const relBetween4And5 = findRelationshipBetween(nodes[3].node_id, nodes[4].node_id);
                return (
                  <button
                    type="button"
                    onClick={() => {
                      if (relBetween4And5) {
                        setSelectedRel(relBetween4And5);
                        setSelectedNode(null);
                      }
                    }}
                    className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-[10px] font-mono border border-slate-700 bg-slate-900/90 text-slate-300 hover:border-blue-500"
                  >
                    <span>{relBetween4And5 ? relBetween4And5.relationship_type : "CONTINUES"}</span>
                    <ArrowDown className="h-3.5 w-3.5 text-blue-400" />
                  </button>
                );
              })()}
            </div>
          )}

          {/* Row 2 of Nodes */}
          <div className="grid grid-cols-4 gap-4">
            {nodes.slice(4, 8).map((node, index) => {
              const badge = getStatusBadge(node.status);
              const nextNode = nodes[4 + index + 1];
              const rel = nextNode ? findRelationshipBetween(node.node_id, nextNode.node_id) : undefined;
              const isSelected = selectedNode?.node_id === node.node_id;

              return (
                <div key={node.node_id} className="relative flex flex-col">
                  {/* Node Card */}
                  <div
                    onClick={() => {
                      setSelectedNode(node);
                      setSelectedRel(null);
                    }}
                    className={`p-4 rounded-xl border transition-all cursor-pointer bg-slate-900/80 hover:bg-slate-800/80 ${
                      isSelected
                        ? "ring-2 ring-blue-500 border-blue-400 shadow-lg shadow-blue-500/10"
                        : `${badge.border} hover:border-slate-600`
                    }`}
                  >
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <div className="flex items-center gap-2">
                        <div className="p-2 rounded-lg bg-slate-800/80 text-blue-400 border border-slate-700/60">
                          {renderNodeIcon(node.node_type, "h-4 w-4")}
                        </div>
                        <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 font-semibold">
                          {node.node_type.replace("_", " ")}
                        </span>
                      </div>
                      <span
                        className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${badge.bg} ${badge.border}`}
                      >
                        {badge.icon}
                        <span>{badge.label}</span>
                      </span>
                    </div>

                    <h5 className="text-xs font-semibold text-slate-300 mb-1">{node.label}</h5>
                    <p className="text-xs text-white font-mono break-words line-clamp-2" title={node.value}>
                      {node.value}
                    </p>

                    <div className="mt-3 pt-2.5 border-t border-slate-800/80 flex items-center justify-between text-[10px] font-mono text-slate-400">
                      <span>Click to inspect details</span>
                      {node.evidence_ids.length > 0 && (
                        <span className="text-blue-400">{node.evidence_ids.length} Evidence</span>
                      )}
                    </div>
                  </div>

                  {/* Relationship Indicator to Next Node in row */}
                  {index < 3 && rel && (
                    <div className="mt-2 text-center">
                      <button
                        type="button"
                        onClick={() => {
                          setSelectedRel(rel);
                          setSelectedNode(null);
                        }}
                        className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-mono border transition-all ${
                          getStatusBadge(rel.status).bg
                        } ${getStatusBadge(rel.status).border} hover:scale-105`}
                      >
                        <span>{rel.relationship_type}</span>
                        <ArrowRight className="h-3 w-3" />
                      </button>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* MOBILE / TABLET (Vertical Connected Chain) */}
        <div className="block lg:hidden space-y-3">
          {nodes.map((node, idx) => {
            const badge = getStatusBadge(node.status);
            const nextNode = nodes[idx + 1];
            const rel = nextNode ? findRelationshipBetween(node.node_id, nextNode.node_id) : undefined;
            const isSelected = selectedNode?.node_id === node.node_id;

            return (
              <div key={node.node_id} className="space-y-2">
                <div
                  onClick={() => {
                    setSelectedNode(node);
                    setSelectedRel(null);
                  }}
                  className={`p-4 rounded-xl border transition-all cursor-pointer bg-slate-900/90 ${
                    isSelected ? "ring-2 ring-blue-500 border-blue-400" : `${badge.border}`
                  }`}
                >
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <div className="flex items-center gap-2">
                      <div className="p-2 rounded-lg bg-slate-800 text-blue-400 border border-slate-700">
                        {renderNodeIcon(node.node_type, "h-4 w-4")}
                      </div>
                      <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 font-semibold">
                        {node.node_type.replace("_", " ")}
                      </span>
                    </div>
                    <span
                      className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-[10px] font-mono font-bold border ${badge.bg} ${badge.border}`}
                    >
                      {badge.icon}
                      <span>{badge.label}</span>
                    </span>
                  </div>

                  <h5 className="text-xs font-semibold text-slate-300">{node.label}</h5>
                  <p className="text-xs text-white font-mono break-words">{node.value}</p>

                  <div className="mt-2 text-[10px] font-mono text-slate-400 flex items-center justify-between">
                    <span>Tap to view provenance</span>
                    {node.evidence_ids.length > 0 && (
                      <span className="text-blue-400">{node.evidence_ids.length} Evidence</span>
                    )}
                  </div>
                </div>

                {/* Mobile Vertical Connection Link */}
                {rel && (
                  <div className="flex justify-center py-1">
                    <button
                      type="button"
                      onClick={() => {
                        setSelectedRel(rel);
                        setSelectedNode(null);
                      }}
                      className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-mono border transition-all ${
                        getStatusBadge(rel.status).bg
                      } ${getStatusBadge(rel.status).border}`}
                    >
                      <span>{rel.relationship_type}</span>
                      <ArrowDown className="h-3 w-3" />
                      <span>({rel.status})</span>
                    </button>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* INSPECTOR PANEL / DRAWER FOR SELECTED NODE OR RELATIONSHIP */}
      {(selectedNode || selectedRel) && (
        <div className="p-5 rounded-2xl border border-blue-900/60 bg-slate-950/95 shadow-2xl space-y-4 animate-in fade-in duration-200">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2">
              <Info className="h-4 w-4 text-blue-400" />
              <h4 className="text-sm font-bold text-white uppercase tracking-wider">
                {selectedNode ? "Node Provenance Inspection" : "Relationship Provenance Inspection"}
              </h4>
            </div>
            <button
              type="button"
              onClick={() => {
                setSelectedNode(null);
                setSelectedRel(null);
              }}
              className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
            >
              <X className="h-4 w-4" />
            </button>
          </div>

          {/* NODE INSPECTOR */}
          {selectedNode && (
            <div className="space-y-4 text-xs font-mono">
              <div className="flex flex-wrap items-center justify-between gap-2 p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                <div>
                  <span className="text-slate-500 text-[10px] block">NODE TYPE</span>
                  <span className="text-white font-bold text-sm">
                    {selectedNode.node_type.replace("_", " ")}
                  </span>
                </div>
                <div>
                  <span className="text-slate-500 text-[10px] block">STATUS</span>
                  <span
                    className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-xs font-bold border ${
                      getStatusBadge(selectedNode.status).bg
                    } ${getStatusBadge(selectedNode.status).border}`}
                  >
                    {getStatusBadge(selectedNode.status).icon}
                    <span>{selectedNode.status}</span>
                  </span>
                </div>
              </div>

              <div>
                <span className="text-slate-400 font-bold block mb-1">OBSERVED VALUE / STATEMENT</span>
                <div className="p-3 rounded-xl bg-slate-900/90 border border-slate-800 text-slate-200 whitespace-pre-wrap font-sans text-xs">
                  {selectedNode.value}
                </div>
              </div>

              {/* Status Explanation */}
              <div>
                <span className="text-slate-400 font-bold block mb-1">STATUS EXPLANATION</span>
                <p className="text-slate-300 font-sans text-xs leading-relaxed">
                  {selectedNode.status === "CONTRADICTORY" && (
                    <span className="text-rose-400 font-semibold block mb-1">
                      ⚠️ Contradiction Detected: Observed assertion directly conflicts with independent statutory directory records.
                    </span>
                  )}
                  {selectedNode.status === "VERIFIED" && (
                    <span className="text-emerald-400 font-semibold block mb-1">
                      ✓ Authoritatively Verified: Confirmed against official regulatory registry records.
                    </span>
                  )}
                  {selectedNode.status === "UNVERIFIED" && (
                    <span className="text-amber-400 font-semibold block mb-1">
                      ⚠️ Unverified: Claim was made on the webpage, but third-party confirmation is pending or absent.
                    </span>
                  )}
                  {selectedNode.status === "NOT_OBSERVED" && (
                    <span className="text-slate-400 font-semibold block mb-1">
                      ℹ️ Not Observed: No supporting evidence or declaration was identified on the public website.
                    </span>
                  )}
                  {selectedNode.status === "UNKNOWN" && (
                    <span className="text-slate-400 font-semibold block mb-1">
                      ❓ Unknown: Insufficient public evidence was observed to establish status.
                    </span>
                  )}
                </p>
              </div>

              {/* Traceable Evidence */}
              {selectedNode.evidence_ids.length > 0 && (
                <div>
                  <span className="text-slate-400 font-bold block mb-1.5">
                    LINKED EVIDENCE OBJECTS ({selectedNode.evidence_ids.length})
                  </span>
                  <div className="space-y-2">
                    {selectedNode.evidence_ids.map((eid) => {
                      const evObj = getEvidenceById(eid);
                      return (
                        <div
                          key={eid}
                          className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1"
                        >
                          <div className="flex items-center justify-between text-[10px] text-slate-400">
                            <span className="text-blue-400 font-bold">{eid}</span>
                            <span>{evObj?.source_type || "PAGE_TEXT"}</span>
                          </div>
                          <p className="text-slate-200 font-sans text-xs italic">
                            &ldquo;{evObj?.extracted_text || "Observed text captured during ingestion."}&rdquo;
                          </p>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
              {/* Traceable Verification Records */}
              {selectedNode.verification_ids.length > 0 && (
                <div>
                  <span className="text-slate-400 font-bold block mb-1.5">
                    AUTHORITATIVE VERIFICATION RECORDS ({selectedNode.verification_ids.length})
                  </span>
                  <div className="space-y-2">
                    {selectedNode.verification_ids.map((vid) => {
                      const verObj = getVerificationById(vid);
                      return (
                        <div
                          key={vid}
                          className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1"
                        >
                          <div className="flex items-center justify-between text-[10px] text-slate-400">
                            <span className="text-emerald-400 font-bold">{vid}</span>
                            <span>{verObj?.source_name || "Statutory Directory"}</span>
                          </div>
                          {verObj?.matched_entity && (
                            <p className="text-xs text-white">
                              Matched Entity: <strong>{verObj.matched_entity}</strong>
                            </p>
                          )}
                          <p className="text-slate-300 font-sans text-xs italic">
                            {verObj?.reason || "Verification check recorded."}
                          </p>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* RELATIONSHIP INSPECTOR */}
          {selectedRel && (
            <div className="space-y-4 text-xs font-mono">
              <div className="flex flex-wrap items-center justify-between gap-2 p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                <div>
                  <span className="text-slate-500 text-[10px] block">RELATIONSHIP TYPE</span>
                  <span className="text-white font-bold text-sm">
                    {selectedRel.relationship_type}
                  </span>
                </div>
                <div>
                  <span className="text-slate-500 text-[10px] block">STATUS</span>
                  <span
                    className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-xs font-bold border ${
                      getStatusBadge(selectedRel.status).bg
                    } ${getStatusBadge(selectedRel.status).border}`}
                  >
                    {getStatusBadge(selectedRel.status).icon}
                    <span>{selectedRel.status}</span>
                  </span>
                </div>
              </div>

              <div>
                <span className="text-slate-400 font-bold block mb-1">PROVENANCE EXPLANATION / REASON</span>
                <div className="p-3 rounded-xl bg-slate-900/90 border border-slate-800 text-slate-200 font-sans text-xs leading-relaxed">
                  {selectedRel.explanation}
                </div>
              </div>

              {selectedRel.status === "CONTRADICTORY" && (
                <div className="p-3 rounded-xl bg-rose-950/40 border border-rose-800/80 text-rose-300 font-sans text-xs space-y-1">
                  <strong>Explicit Contradiction Notice:</strong>
                  <p>
                    The registration number cited on this webpage is registered to a different legal entity in the statutory registry.
                    RakshaScan reports this verified discrepancy without applying prejudicial or non-evidentiary fraud labels.
                  </p>
                </div>
              )}

              {selectedRel.evidence_ids.length > 0 && (
                <div>
                  <span className="text-slate-400 font-bold block mb-1">
                    SUPPORTING EVIDENCE ({selectedRel.evidence_ids.length})
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {selectedRel.evidence_ids.map((eid) => (
                      <span
                        key={eid}
                        className="px-2 py-0.5 rounded bg-slate-800 text-blue-300 border border-slate-700 text-[10px]"
                      >
                        {eid}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
