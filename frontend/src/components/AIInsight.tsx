"use client";

import { useEffect, useRef, useState } from "react";
import { analyzeUpload, AIInsightResponse } from "@/lib/api";

interface AIInsightProps {
  file: File;
  inputFormat: string;
  selectedFormat: string;
  onSelectFormat: (format: string) => void;
}

export default function AIInsight({
  file,
  inputFormat,
  selectedFormat,
  onSelectFormat,
}: AIInsightProps) {
  const [insight, setInsight] = useState<AIInsightResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [typed, setTyped] = useState("");
  const requested = useRef<File | null>(null);

  useEffect(() => {
    if (!file || requested.current === file) return;
    requested.current = file;
    setLoading(true);
    setError(null);
    setInsight(null);
    setTyped("");

    analyzeUpload(file)
      .then((data) => {
        if (data.error) {
          setError(data.error);
        } else {
          setInsight(data);
        }
      })
      .catch((e) => setError(e.message || "AI analysis failed"))
      .finally(() => setLoading(false));
  }, [file]);

  // Typewriter effect on the summary to make the AI output feel alive
  useEffect(() => {
    if (!insight?.summary) return;
    setTyped("");
    const s = insight.summary;
    let i = 0;
    const step = Math.max(1, Math.floor(s.length / 120));
    const t = setInterval(() => {
      i = Math.min(s.length, i + step);
      setTyped(s.slice(0, i));
      if (i >= s.length) clearInterval(t);
    }, 18);
    return () => clearInterval(t);
  }, [insight?.summary]);

  if (loading) {
    return (
      <div
        className="rounded-lg border p-4 space-y-2"
        style={{
          borderColor: "var(--color-primary)",
          background:
            "linear-gradient(135deg, color-mix(in srgb, var(--color-primary) 8%, transparent), transparent)",
        }}
      >
        <div className="flex items-center gap-2">
          <span className="inline-block w-2 h-2 rounded-full bg-[var(--color-primary)] animate-pulse" />
          <span className="inline-block w-2 h-2 rounded-full bg-[var(--color-primary)] animate-pulse [animation-delay:120ms]" />
          <span className="inline-block w-2 h-2 rounded-full bg-[var(--color-primary)] animate-pulse [animation-delay:240ms]" />
          <span className="text-xs font-semibold text-[var(--color-primary)] tracking-wide uppercase">
            AI is analyzing your file
          </span>
        </div>
        <p className="text-[11px] text-[var(--color-text-dim)]">
          Reading contents · picking the best format · drafting tips…
        </p>
      </div>
    );
  }

  if (error || !insight) {
    return (
      <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-3">
        <p className="text-[11px] text-[var(--color-text-dim)]">
          <span className="text-[var(--color-text)] font-medium">AI offline.</span>{" "}
          {error || "No insight available."} You can still pick a format manually below.
        </p>
      </div>
    );
  }

  const rec = insight.recommended;
  const recPicked = rec && selectedFormat === rec.format;

  return (
    <div
      className="rounded-lg border p-4 space-y-3"
      style={{
        borderColor: "var(--color-primary)",
        background:
          "linear-gradient(135deg, color-mix(in srgb, var(--color-primary) 10%, transparent), transparent)",
      }}
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center justify-center w-5 h-5 rounded bg-[var(--color-primary)] text-white text-[10px] font-bold">
            AI
          </span>
          <span className="text-xs font-semibold tracking-wide uppercase text-[var(--color-primary)]">
            Smart insight
          </span>
        </div>
        {insight.model && (
          <span className="text-[10px] text-[var(--color-text-dim)] font-mono">
            {insight.model.split("-").slice(0, 2).join("-")}
          </span>
        )}
      </div>

      {/* Summary with typewriter */}
      <p className="text-sm leading-relaxed text-[var(--color-text)]">
        {typed}
        {typed.length < (insight.summary?.length || 0) && (
          <span className="inline-block w-1.5 h-3.5 align-middle bg-[var(--color-primary)] ml-0.5 animate-pulse" />
        )}
      </p>

      {/* Recommended format CTA */}
      {rec?.format && (
        <div className="flex items-start gap-2">
          <button
            onClick={() => onSelectFormat(rec.format)}
            disabled={recPicked}
            className={`shrink-0 px-3 py-1.5 rounded-md text-xs font-mono font-semibold border transition-all ${
              recPicked
                ? "bg-[var(--color-primary)] text-white border-transparent"
                : "bg-[var(--color-bg-card)] border-[var(--color-primary)] text-[var(--color-primary)] hover:bg-[var(--color-primary)] hover:text-white"
            }`}
          >
            {recPicked ? "✓ " : "→ "}.{rec.format.toUpperCase()}
          </button>
          <p className="text-xs text-[var(--color-text-dim)] mt-1.5 leading-relaxed">
            <span className="text-[var(--color-text)] font-medium">Recommended.</span>{" "}
            {rec.reason}
          </p>
        </div>
      )}

      {/* Alternatives */}
      {insight.alternatives && insight.alternatives.length > 0 && (
        <div>
          <p className="text-[10px] font-semibold uppercase tracking-wide text-[var(--color-text-dim)] mb-1.5">
            Or try
          </p>
          <div className="flex flex-wrap gap-1.5">
            {insight.alternatives.map((alt) => (
              <button
                key={alt.format}
                onClick={() => onSelectFormat(alt.format)}
                title={alt.reason}
                className={`px-2.5 py-1 rounded-md text-[11px] font-mono font-semibold border transition-all ${
                  selectedFormat === alt.format
                    ? "bg-[var(--color-primary)] text-white border-transparent"
                    : "bg-[var(--color-bg-card)] border-[var(--color-border)] text-[var(--color-text-dim)] hover:text-[var(--color-text)] hover:border-[var(--color-primary)]"
                }`}
              >
                .{alt.format.toUpperCase()}
                <span className="ml-1 opacity-60 font-sans font-normal">
                  — {alt.reason}
                </span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Tips */}
      {insight.tips && insight.tips.length > 0 && (
        <div className="pt-1 border-t border-[var(--color-border)]/40">
          <p className="text-[10px] font-semibold uppercase tracking-wide text-[var(--color-text-dim)] mb-1.5">
            Heads-up
          </p>
          <ul className="space-y-0.5">
            {insight.tips.map((tip, i) => (
              <li key={i} className="text-[11px] text-[var(--color-text-dim)] leading-relaxed">
                <span className="text-[var(--color-primary)] mr-1">▸</span>
                {tip}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Suggested filename */}
      {insight.suggested_filename && (
        <div className="flex items-center gap-2 text-[11px]">
          <span className="text-[var(--color-text-dim)] uppercase tracking-wide font-semibold">
            Rename to
          </span>
          <code className="px-2 py-0.5 rounded bg-[var(--color-surface)] text-[var(--color-text)] font-mono">
            {insight.suggested_filename}.{(selectedFormat || rec?.format || inputFormat).toLowerCase()}
          </code>
        </div>
      )}
    </div>
  );
}
