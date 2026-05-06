export default function PdfUploader({ onFileSelected }) {
  return (
    <label className="flex cursor-pointer flex-col gap-2 rounded-xl border border-dashed border-slate-300 bg-white p-4 text-sm text-slate-600 shadow-sm">
      <span className="font-medium text-slate-900">Tải PDF</span>
      <span>Chọn file PDF để chuẩn bị parse và OCR công thức.</span>
      <input
        type="file"
        accept="application/pdf"
        className="hidden"
        onChange={(event) => onFileSelected?.(event.target.files?.[0] ?? null)}
      />
    </label>
  );
}
