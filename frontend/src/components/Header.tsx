"use client";

export default function Header() {
  return (
    <header className="w-full border-b border-[var(--color-border)]">
      <div className="px-6 h-14 flex items-center justify-between">
        <a href="/" className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-md bg-[var(--color-primary)] flex items-center justify-center text-xs font-bold text-white">
            A
          </div>
          <span className="text-sm font-semibold tracking-tight">
            Ash Loves Files
          </span>
        </a>

        <nav className="flex items-center gap-5 text-[13px]">
          <a
            href="#formats"
            className="text-[var(--color-text-dim)] hover:text-[var(--color-text)] transition-colors"
          >
            Formats
          </a>
          <a
            href="#how-it-works"
            className="text-[var(--color-text-dim)] hover:text-[var(--color-text)] transition-colors"
          >
            How it works
          </a>
        </nav>
      </div>
    </header>
  );
}
