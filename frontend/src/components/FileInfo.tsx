"use client";

import { formatFileSize } from "@/lib/api";
import { CATEGORY_INFO } from "@/lib/formats";

interface FileInfoProps {
  file: File;
  onRemove: () => void;
}

function getFileCategory(ext: string): string {
  const imageExts = new Set(["png","jpg","jpeg","gif","bmp","tiff","tif","webp","svg","ico","psd","heic","avif","eps"]);
  const docExts = new Set(["pdf","docx","doc","xlsx","xls","pptx","ppt","odt","ods","odp","rtf","txt","html","htm","md","csv","tsv","tex"]);
  const audioExts = new Set(["mp3","wav","flac","aac","ogg","wma","m4a","aiff","opus"]);
  const videoExts = new Set(["mp4","avi","mkv","mov","wmv","flv","webm","mpeg","3gp"]);
  const archiveExts = new Set(["zip","tar","gz","bz2","7z","xz","rar"]);
  const dataExts = new Set(["json","yaml","yml","toml","xml","ini"]);
  const ebookExts = new Set(["epub","mobi","azw3","fb2"]);
  const fontExts = new Set(["ttf","otf","woff","woff2","eot"]);

  const e = ext.toLowerCase();
  if (imageExts.has(e)) return "image";
  if (docExts.has(e)) return "document";
  if (audioExts.has(e)) return "audio";
  if (videoExts.has(e)) return "video";
  if (archiveExts.has(e)) return "archive";
  if (dataExts.has(e)) return "data";
  if (ebookExts.has(e)) return "ebook";
  if (fontExts.has(e)) return "font";
  return "document";
}

export default function FileInfo({ file, onRemove }: FileInfoProps) {
  const ext = file.name.split(".").pop() || "";
  const category = getFileCategory(ext);
  const catInfo = CATEGORY_INFO[category];

  return (
    <div className="flex items-center gap-3 bg-[var(--color-surface)] rounded-lg p-3 border border-[var(--color-border)]">
      <div
        className="w-10 h-10 rounded-md flex items-center justify-center text-[10px] font-bold tracking-wide shrink-0"
        style={{
          backgroundColor: `${catInfo?.color || "#635bff"}15`,
          color: catInfo?.color || "#635bff",
        }}
      >
        {ext.toUpperCase().slice(0, 4)}
      </div>

      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium truncate">{file.name}</p>
        <p className="text-xs text-[var(--color-text-dim)]">
          {formatFileSize(file.size)} &middot; {catInfo?.label || "File"}
        </p>
      </div>

      <button
        onClick={onRemove}
        className="w-7 h-7 rounded-md hover:bg-[var(--color-bg-card-hover)] flex items-center justify-center transition-colors text-[var(--color-text-dim)] hover:text-[var(--color-error)] shrink-0"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  );
}
