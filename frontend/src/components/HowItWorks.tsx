"use client";

const steps = [
  {
    num: "1",
    title: "Upload",
    desc: "Drop any file. We support 120+ formats across images, documents, audio, video, and more.",
  },
  {
    num: "2",
    title: "Choose format",
    desc: "We detect your file type and show compatible output formats. Pick one.",
  },
  {
    num: "3",
    title: "Download",
    desc: "Conversion runs instantly. Download your file. No sign-up, no watermarks.",
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="px-6 py-20">
      <h2 className="text-lg font-semibold text-center mb-10">
        How it works
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {steps.map((step) => (
          <div key={step.num} className="text-center">
            <div className="w-8 h-8 rounded-full bg-[var(--color-surface)] border border-[var(--color-border)] flex items-center justify-center text-xs font-semibold text-[var(--color-text-dim)] mx-auto mb-3">
              {step.num}
            </div>
            <h3 className="text-sm font-semibold mb-1.5">{step.title}</h3>
            <p className="text-[var(--color-text-dim)] text-xs leading-relaxed">
              {step.desc}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
