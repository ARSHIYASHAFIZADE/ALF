"use client";

export default function Footer() {
  return (
    <footer className="border-t border-[var(--color-border)] mt-20">
      <div className="px-6 py-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-[var(--color-text-dim)]">
        <div className="flex items-center gap-2">
          <div className="w-5 h-5 rounded bg-[var(--color-primary)] flex items-center justify-center text-[10px] font-bold text-white">
            A
          </div>
          <span className="font-medium text-[var(--color-text)]">Ash Loves Files</span>
        </div>
        <p>Free &middot; No sign-up &middot; Files auto-delete in 1 hour</p>
      </div>
    </footer>
  );
}
