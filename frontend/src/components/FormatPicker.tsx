"use client";

import { useState, useEffect } from "react";
import { getOutputFormats } from "@/lib/api";
import { CATEGORY_INFO } from "@/lib/formats";

interface FormatPickerProps {
  inputFormat: string;
  selectedFormat: string;
  onSelect: (format: string) => void;
}

export default function FormatPicker({
  inputFormat,
  selectedFormat,
  onSelect,
}: FormatPickerProps) {
  const [formats, setFormats] = useState<Record<string, string[]>>({});
  const [loading, setLoading] = useState(true);
  const [activeCategory, setActiveCategory] = useState<string>("");

  useEffect(() => {
    if (!inputFormat) return;
    setLoading(true);
    getOutputFormats(inputFormat)
      .then((res) => {
        const aliases: Record<string, string[]> = {
          jpg: ["jpeg"], jpeg: ["jpg"],
          tif: ["tiff"], tiff: ["tif"],
          yml: ["yaml"], yaml: ["yml"],
          htm: ["html"], html: ["htm"],
        };
        const toFilter = new Set([inputFormat, ...(aliases[inputFormat] || [])]);
        const filtered: Record<string, string[]> = {};
        for (const [cat, fmts] of Object.entries(res.formats || {})) {
          const cleaned = (fmts as string[]).filter((f) => !toFilter.has(f));
          if (cleaned.length > 0) filtered[cat] = cleaned;
        }
        setFormats(filtered);
        const cats = Object.keys(filtered);
        if (cats.length > 0) setActiveCategory(cats[0]);
      })
      .catch(() => setFormats({}))
      .finally(() => setLoading(false));
  }, [inputFormat]);

  if (loading) {
    return (
      <div className="text-center py-6">
        <div className="w-5 h-5 border-2 border-[var(--color-primary)] border-t-transparent rounded-full spinner mx-auto mb-2" />
        <p className="text-[var(--color-text-dim)] text-xs">
          Loading formats...
        </p>
      </div>
    );
  }

  const categories = Object.keys(formats);

  if (categories.length === 0) {
    return (
      <div className="text-center py-6">
        <p className="text-[var(--color-text-dim)] text-sm">
          No conversion options available for .{inputFormat}
        </p>
      </div>
    );
  }

  return (
    <div>
      <p className="text-sm font-medium mb-3">Convert to</p>

      {/* Category tabs */}
      <div className="flex flex-wrap gap-1.5 mb-3">
        {categories.map((cat) => {
          const info = CATEGORY_INFO[cat];
          return (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                activeCategory === cat
                  ? "bg-[var(--color-primary)] text-white"
                  : "bg-[var(--color-surface)] text-[var(--color-text-dim)] hover:bg-[var(--color-bg-card-hover)] hover:text-[var(--color-text)]"
              }`}
            >
              {info?.label || cat}
              <span className="ml-1 opacity-60">
                {formats[cat].length}
              </span>
            </button>
          );
        })}
      </div>

      {/* Format pills */}
      <div className="flex flex-wrap gap-1.5">
        {(formats[activeCategory] || []).map((fmt) => (
          <button
            key={fmt}
            onClick={() => onSelect(fmt)}
            className={`format-pill px-3 py-2 rounded-md text-xs font-mono font-semibold uppercase border transition-all ${
              selectedFormat === fmt
                ? "selected border-transparent"
                : "bg-[var(--color-bg-card)] border-[var(--color-border)] text-[var(--color-text)] hover:border-[var(--color-primary)]"
            }`}
          >
            .{fmt}
          </button>
        ))}
      </div>
    </div>
  );
}
