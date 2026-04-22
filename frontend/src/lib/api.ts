const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

export interface JobResponse {
  id: string;
  originalFilename: string;
  inputFormat: string;
  outputFormat: string;
  category: string;
  status: "pending" | "processing" | "completed" | "failed";
  progress: number;
  outputFilename: string | null;
  fileSize: number;
  outputSize: number;
  errorMessage: string | null;
  createdAt: string;
  completedAt: string | null;
}

export interface FormatsResponse {
  [category: string]: {
    input: string[];
    output: string[];
  };
}

export interface OutputFormatsResponse {
  formats: {
    [category: string]: string[];
  };
  error?: string;
}

export async function uploadFile(
  file: File,
  outputFormat: string
): Promise<{ jobId: string; status: string }> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("output_format", outputFormat);

  const res = await fetch(`${API_BASE}/api/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Upload failed" }));
    throw new Error(err.detail || "Upload failed");
  }

  return res.json();
}

export async function startConversion(jobId: string): Promise<JobResponse> {
  const res = await fetch(`${API_BASE}/api/convert/${jobId}`, {
    method: "POST",
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Conversion failed" }));
    throw new Error(err.detail || "Conversion failed");
  }

  return res.json();
}

export async function getJobStatus(jobId: string): Promise<JobResponse> {
  const res = await fetch(`${API_BASE}/api/job/${jobId}`);

  if (!res.ok) {
    throw new Error("Failed to get job status");
  }

  return res.json();
}

export function getDownloadUrl(jobId: string): string {
  return `${API_BASE}/api/download/${jobId}`;
}

export async function getAllFormats(): Promise<FormatsResponse> {
  const res = await fetch(`${API_BASE}/api/formats`);
  if (!res.ok) throw new Error("Failed to fetch formats");
  return res.json();
}

export async function getOutputFormats(
  inputFormat: string
): Promise<OutputFormatsResponse> {
  const res = await fetch(`${API_BASE}/api/formats/${inputFormat}`);
  if (!res.ok) throw new Error("Failed to fetch output formats");
  return res.json();
}

export interface AIInsightResponse {
  jobId: string;
  category: string;
  inputFormat: string;
  availableOutputFormats: string[];
  preview: string;
  summary?: string;
  recommended?: { format: string; reason: string };
  alternatives?: { format: string; reason: string }[];
  tips?: string[];
  suggested_filename?: string;
  model?: string;
  error?: string;
}

export async function getAIInsight(jobId: string): Promise<AIInsightResponse> {
  const res = await fetch(`${API_BASE}/api/ai/analyze/${jobId}`, {
    method: "POST",
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "AI analysis failed" }));
    throw new Error(err.detail || "AI analysis failed");
  }
  return res.json();
}

export async function analyzeUpload(file: File): Promise<AIInsightResponse> {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_BASE}/api/ai/analyze-upload`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "AI analysis failed" }));
    throw new Error(err.detail || "AI analysis failed");
  }
  return res.json();
}

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
}
