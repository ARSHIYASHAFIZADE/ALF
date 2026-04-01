"use client";

import { useState, useEffect } from "react";
import { getAllFormats, FormatsResponse } from "@/lib/api";
import { CATEGORY_INFO } from "@/lib/formats";

export default function FormatExplorer() {
  const [formats, setFormats] = useState<FormatsResponse>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAllFormats()
      .then(setFormats)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const totalInput = new Set(
    Object.values(formats).flatMap((c) => c.input)
  ).size;
  const totalOutput = new Set(
    Object.values(formats).flatMap((c) => c.output)
  ).size;

  return (
    <section id="formats" className="px-6 py-16">
      <div className="text-center mb-10">
        <h2 className="text-lg font-semibold mb-2">
          Supported formats
        </h2>
        <p className="text-[var(--color-text-dim)] text-xs">
          {loading ? (
            "Loading..."
          ) : (
            <>
              {totalInput} input formats &middot; {totalOutput} output formats
            </>
          )}
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {Object.entries(CATEGORY_INFO).map(([key, info]) => {
          const catFormats = formats[key];
          return (
            <div
              key={key}
              className="bg-[var(--color-bg-card)] rounded-lg p-4 border border-[var(--color-border)] hover:border-[var(--color-border)] transition-all"
            >
              <div className="flex items-center gap-2 mb-2">
                <div
                  className="w-6 h-6 rounded flex items-center justify-center text-[9px] font-bold"
                  style={{
                    backgroundColor: `${info.color}15`,
                    color: info.color,
                  }}
                >
                  {info.icon}
                </div>
                <h3 className="text-sm font-semibold">{info.label}</h3>
              </div>
              <p className="text-[var(--color-text-dim)] text-[11px] mb-2.5 leading-relaxed">
                {info.description}
              </p>
              {catFormats && (
                <div className="flex flex-wrap gap-1">
                  {catFormats.input.slice(0, 10).map((fmt) => (
                    <span
                      key={fmt}
                      className="text-[10px] font-mono uppercase px-1.5 py-0.5 rounded bg-[var(--color-surface)] text-[var(--color-text-dim)]"
                    >
                      {fmt}
                    </span>
                  ))}
                  {catFormats.input.length > 10 && (
                    <span className="text-[10px] px-1.5 py-0.5 text-[var(--color-text-dim)]">
                      +{catFormats.input.length - 10}
                    </span>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
