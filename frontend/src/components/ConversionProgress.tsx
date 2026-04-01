"use client";

import { JobResponse, formatFileSize, getDownloadUrl } from "@/lib/api";

interface ConversionProgressProps {
  job: JobResponse | null;
  isConverting: boolean;
  error: string | null;
  onReset: () => void;
}

export default function ConversionProgress({
  job,
  isConverting,
  error,
  onReset,
}: ConversionProgressProps) {
  if (error) {
    return (
      <div className="rounded-lg border border-[var(--color-error)]/20 bg-[var(--color-error)]/5 p-6 text-center">
        <div className="w-10 h-10 rounded-full bg-[var(--color-error)]/10 flex items-center justify-center mx-auto mb-3">
          <svg className="w-5 h-5 text-[var(--color-error)]" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        <h3 className="text-sm font-semibold text-[var(--color-error)] mb-1">
          Conversion failed
        </h3>
        <p className="text-[var(--color-text-dim)] text-xs mb-4 max-w-sm mx-auto">
          {error}
        </p>
        <button
          onClick={onReset}
          className="px-4 py-2 rounded-md text-xs font-medium bg-[var(--color-surface)] hover:bg-[var(--color-bg-card-hover)] text-[var(--color-text)] border border-[var(--color-border)] transition-colors"
        >
          Try again
        </button>
      </div>
    );
  }

  if (isConverting && (!job || job.status === "processing" || job.status === "pending")) {
    const progress = job?.progress || 0;
    return (
      <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-6 text-center">
        <div className="w-8 h-8 mx-auto mb-3">
          <div className="w-full h-full rounded-full border-2 border-[var(--color-border)] border-t-[var(--color-primary)] spinner" />
        </div>
        <p className="text-sm font-medium mb-1">Converting...</p>
        <p className="text-[var(--color-text-dim)] text-xs mb-4">
          {job?.originalFilename} &rarr; .{job?.outputFormat}
        </p>
        <div className="w-full max-w-xs mx-auto h-1.5 bg-[var(--color-border)] rounded-full overflow-hidden">
          <div
            className="progress-bar h-full rounded-full"
            style={{ width: `${Math.max(progress, 5)}%` }}
          />
        </div>
        <p className="text-[10px] text-[var(--color-text-dim)] mt-1.5">{progress}%</p>
      </div>
    );
  }

  if (job?.status === "completed") {
    return (
      <div className="rounded-lg border border-[var(--color-success)]/20 bg-[var(--color-success)]/5 p-6 text-center">
        <div className="w-10 h-10 rounded-full bg-[var(--color-success)]/10 flex items-center justify-center mx-auto mb-3">
          <svg className="w-5 h-5 text-[var(--color-success)]" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
          </svg>
        </div>
        <h3 className="text-sm font-semibold text-[var(--color-success)] mb-0.5">
          Done
        </h3>
        <p className="text-[var(--color-text-dim)] text-xs mb-1">
          {job.originalFilename} &rarr; {job.outputFilename}
        </p>
        <p className="text-[10px] text-[var(--color-text-dim)] mb-5">
          {formatFileSize(job.fileSize)} &rarr; {formatFileSize(job.outputSize)}
          {job.outputSize < job.fileSize && (
            <span className="text-[var(--color-success)] ml-1">
              {Math.round((1 - job.outputSize / job.fileSize) * 100)}% smaller
            </span>
          )}
        </p>

        <div className="flex items-center justify-center gap-2">
          <a
            href={getDownloadUrl(job.id)}
            download
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-md bg-[var(--color-primary)] text-white text-xs font-medium hover:bg-[var(--color-primary-dark)] transition-colors"
          >
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
            </svg>
            Download
          </a>
          <button
            onClick={onReset}
            className="px-4 py-2 rounded-md text-xs font-medium bg-[var(--color-surface)] hover:bg-[var(--color-bg-card-hover)] text-[var(--color-text)] border border-[var(--color-border)] transition-colors"
          >
            Convert another
          </button>
        </div>
      </div>
    );
  }

  return null;
}
