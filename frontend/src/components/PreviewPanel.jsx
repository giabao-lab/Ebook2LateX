export default function PreviewPanel({ latexContent }) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-base font-semibold text-slate-900">Preview LaTeX</h2>
      <pre className="whitespace-pre-wrap break-words rounded-lg bg-slate-950 p-4 text-sm text-slate-100">
        {latexContent || "Chưa có nội dung LaTeX."}
      </pre>
    </section>
  );
}
