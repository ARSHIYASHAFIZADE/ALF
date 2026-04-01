"use client";

import { useState, useCallback } from "react";
import Header from "@/components/Header";
import UploadZone from "@/components/UploadZone";
import FileInfo from "@/components/FileInfo";
import FormatPicker from "@/components/FormatPicker";
import ConversionProgress from "@/components/ConversionProgress";
import FormatExplorer from "@/components/FormatExplorer";
import HowItWorks from "@/components/HowItWorks";
import Footer from "@/components/Footer";
import {
  uploadFile,
  startConversion,
  JobResponse,
  formatFileSize,
} from "@/lib/api";

const MAX_FILE_SIZE = 100 * 1024 * 1024;

type Step = "upload" | "format" | "converting" | "done";

export default function Home() {
  const [step, setStep] = useState<Step>("upload");
  const [file, setFile] = useState<File | null>(null);
  const [inputFormat, setInputFormat] = useState("");
  const [selectedFormat, setSelectedFormat] = useState("");
  const [job, setJob] = useState<JobResponse | null>(null);
  const [isConverting, setIsConverting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileSelect = useCallback((f: File) => {
    const ext = f.name.split(".").pop()?.toLowerCase() || "";

    if (!ext || f.name.startsWith(".") || !f.name.includes(".")) {
      setError("File has no extension. Rename it with the correct extension (e.g. photo.jpg).");
      return;
    }

    if (f.size > MAX_FILE_SIZE) {
      setError(`File too large (${formatFileSize(f.size)}). Max 100 MB.`);
      return;
    }

    if (f.size === 0) {
      setError("File is empty.");
      return;
    }

    setFile(f);
    setInputFormat(ext);
    setSelectedFormat("");
    setError(null);
    setJob(null);
    setStep("format");
  }, []);

  const handleFormatSelect = useCallback((fmt: string) => {
    setSelectedFormat(fmt);
  }, []);

  const handleConvert = useCallback(async () => {
    if (!file || !selectedFormat) return;

    setIsConverting(true);
    setError(null);
    setStep("converting");

    try {
      const { jobId } = await uploadFile(file, selectedFormat);
      const result = await startConversion(jobId);
      setJob(result);

      if (result.status === "completed") {
        setStep("done");
      } else if (result.status === "failed") {
        setError(result.errorMessage || "Conversion failed");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setIsConverting(false);
    }
  }, [file, selectedFormat]);

  const handleReset = useCallback(() => {
    setStep("upload");
    setFile(null);
    setInputFormat("");
    setSelectedFormat("");
    setJob(null);
    setError(null);
    setIsConverting(false);
  }, []);

  const handleRemoveFile = useCallback(() => {
    setFile(null);
    setInputFormat("");
    setSelectedFormat("");
    setError(null);
    setStep("upload");
  }, []);

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="flex-1">
        {/* Hero */}
        <section className="px-6 pt-16 pb-6 text-center">
          <h2 className="text-2xl md:text-3xl font-bold mb-2 tracking-tight">
            Convert any file, instantly
          </h2>
          <p className="text-[var(--color-text-dim)] text-sm">
            120+ formats supported. Free, private, no sign-up.
          </p>
        </section>

        {/* Converter */}
        <section className="max-w-2xl mx-auto px-6 pb-16">
          <div className="bg-[var(--color-bg-card)] rounded-lg border border-[var(--color-border)] p-5">
            {step === "upload" && (
              <>
                <UploadZone onFileSelect={handleFileSelect} />
                {error && (
                  <div className="mt-3 text-center text-[var(--color-error)] text-xs bg-[var(--color-error)]/5 border border-[var(--color-error)]/10 rounded-md p-2.5">
                    {error}
                  </div>
                )}
              </>
            )}

            {step === "format" && file && (
              <div className="space-y-4">
                <FileInfo file={file} onRemove={handleRemoveFile} />

                <FormatPicker
                  inputFormat={inputFormat}
                  selectedFormat={selectedFormat}
                  onSelect={handleFormatSelect}
                />

                {error && (
                  <div className="text-center text-[var(--color-error)] text-xs bg-[var(--color-error)]/5 border border-[var(--color-error)]/10 rounded-md p-2.5">
                    {error}
                  </div>
                )}

                {selectedFormat && (
                  <button
                    onClick={handleConvert}
                    disabled={isConverting}
                    className="w-full py-2.5 rounded-md bg-[var(--color-primary)] text-white text-sm font-medium hover:bg-[var(--color-primary-dark)] transition-colors disabled:opacity-50"
                  >
                    Convert to .{selectedFormat.toUpperCase()}
                  </button>
                )}
              </div>
            )}

            {step === "converting" && (
              <ConversionProgress
                job={job}
                isConverting={isConverting}
                error={error}
                onReset={handleReset}
              />
            )}

            {step === "done" && (
              <ConversionProgress
                job={job}
                isConverting={false}
                error={null}
                onReset={handleReset}
              />
            )}
          </div>
        </section>

        <HowItWorks />
        <FormatExplorer />
      </main>

      <Footer />
    </div>
  );
}
