// Category metadata for display
export const CATEGORY_INFO: Record<
  string,
  { label: string; icon: string; color: string; description: string }
> = {
  image: {
    label: "Images",
    icon: "IMG",
    color: "#635bff",
    description: "PNG, JPG, WebP, SVG, GIF, BMP, TIFF, ICO, PSD, HEIC, AVIF & more",
  },
  document: {
    label: "Documents",
    icon: "DOC",
    color: "#0ea5e9",
    description: "PDF, DOCX, XLSX, PPTX, ODT, RTF, HTML, Markdown, LaTeX & more",
  },
  audio: {
    label: "Audio",
    icon: "AUD",
    color: "#22c55e",
    description: "MP3, WAV, FLAC, AAC, OGG, M4A, OPUS, WMA, AIFF & more",
  },
  video: {
    label: "Video",
    icon: "VID",
    color: "#f97316",
    description: "MP4, AVI, MKV, MOV, WebM, FLV, MPEG, 3GP, GIF & more",
  },
  ebook: {
    label: "Ebooks",
    icon: "EPB",
    color: "#eab308",
    description: "EPUB, MOBI, AZW3, FB2, PDF, DOCX & more",
  },
  archive: {
    label: "Archives",
    icon: "ZIP",
    color: "#ec4899",
    description: "ZIP, TAR, GZ, BZ2, 7Z, XZ, RAR & more",
  },
  data: {
    label: "Data",
    icon: "DAT",
    color: "#14b8a6",
    description: "JSON, YAML, XML, TOML, CSV, TSV, INI",
  },
  font: {
    label: "Fonts",
    icon: "FNT",
    color: "#71717a",
    description: "TTF, OTF, WOFF, WOFF2, EOT",
  },
};

// Format to extension icon mapping
export const FORMAT_EXTENSIONS: Record<string, string> = {
  // Images
  png: "PNG", jpg: "JPG", jpeg: "JPG", gif: "GIF", bmp: "BMP",
  tiff: "TIFF", tif: "TIFF", webp: "WebP", svg: "SVG", ico: "ICO",
  psd: "PSD", heic: "HEIC", avif: "AVIF", eps: "EPS",
  // Documents
  pdf: "PDF", docx: "DOCX", doc: "DOC", xlsx: "XLSX", xls: "XLS",
  pptx: "PPTX", ppt: "PPT", odt: "ODT", ods: "ODS", odp: "ODP",
  rtf: "RTF", txt: "TXT", html: "HTML", htm: "HTML", md: "MD",
  csv: "CSV", tsv: "TSV", tex: "TeX", latex: "LaTeX",
  // Audio
  mp3: "MP3", wav: "WAV", flac: "FLAC", aac: "AAC", ogg: "OGG",
  wma: "WMA", m4a: "M4A", aiff: "AIFF", opus: "OPUS",
  // Video
  mp4: "MP4", avi: "AVI", mkv: "MKV", mov: "MOV", wmv: "WMV",
  flv: "FLV", webm: "WebM", mpeg: "MPEG", "3gp": "3GP",
  // Ebooks
  epub: "EPUB", mobi: "MOBI", azw3: "AZW3", fb2: "FB2",
  // Archives
  zip: "ZIP", tar: "TAR", gz: "GZ", bz2: "BZ2", "7z": "7Z",
  xz: "XZ", rar: "RAR",
  // Data
  json: "JSON", yaml: "YAML", yml: "YAML", toml: "TOML",
  xml: "XML", ini: "INI",
  // Fonts
  ttf: "TTF", otf: "OTF", woff: "WOFF", woff2: "WOFF2", eot: "EOT",
};
