import { useState } from "react";

import MathFieldEditor from "./components/MathFieldEditor.jsx";
import PdfUploader from "./components/PdfUploader.jsx";
import PreviewPanel from "./components/PreviewPanel.jsx";
import { useLatexSync } from "./hooks/useLatexSync.js";
import api from "./services/api.js";

export default function App() {
  const { latexContent, updateFromText, updateFromMathField } = useLatexSync("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [statusMessage, setStatusMessage] = useState("Sẵn sàng.");
  const [documentId, setDocumentId] = useState(null);

  const handleUpload = async () => {
    if (!selectedFile) {
      setStatusMessage("Vui lòng chọn file PDF trước.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await api.post("/api/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setDocumentId(response.data.id);
      setStatusMessage(`Đã tải lên: ${response.data.filename}`);
    } catch (error) {
      setStatusMessage(error?.response?.data?.detail || "Không thể tải file lên.");
    }
  };

  const handleProcess = async () => {
    if (!documentId) {
      setStatusMessage("Cần tải file lên trước khi xử lý.");
      return;
    }

    try {
      const response = await api.post(`/api/process/${documentId}`);
      updateFromText(response.data.latex_content || "");
      setStatusMessage("Đã xử lý PDF và cập nhật LaTeX.");
    } catch (error) {
      setStatusMessage(error?.response?.data?.detail || "Không thể xử lý PDF.");
    }
  };

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-8">
      <div className="mx-auto grid max-w-7xl gap-6 lg:grid-cols-[1fr_1.1fr]">
        <section className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
          <div className="mb-6">
            <p className="text-sm font-medium uppercase tracking-wide text-indigo-600">Ebook2LateX</p>
            <h1 className="mt-2 text-3xl font-bold text-slate-900">PDF → OCR → LaTeX</h1>
            <p className="mt-3 text-sm text-slate-600">
              Khung giao diện này chuẩn bị cho luồng tải PDF, xử lý công thức và đồng bộ 2 chiều giữa
              ô văn bản LaTeX và MathLive.
            </p>
          </div>

          <div className="space-y-4">
            <PdfUploader onFileSelected={setSelectedFile} />

            <div className="flex flex-wrap gap-3">
              <button
                type="button"
                onClick={handleUpload}
                className="rounded-xl bg-indigo-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-indigo-700"
              >
                Tải lên PDF
              </button>
              <button
                type="button"
                onClick={handleProcess}
                className="rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-100"
              >
                Xử lý OCR
              </button>
            </div>

            <p className="rounded-xl bg-slate-100 px-4 py-3 text-sm text-slate-700">{statusMessage}</p>
          </div>

          <div className="mt-6 space-y-3">
            <label className="block text-sm font-medium text-slate-700" htmlFor="latex-input">
              LaTeX raw
            </label>
            <textarea
              id="latex-input"
              value={latexContent}
              onChange={(event) => updateFromText(event.target.value)}
              className="min-h-40 w-full rounded-xl border border-slate-200 bg-white p-4 text-sm shadow-sm outline-none focus:border-indigo-500"
              placeholder="Nhập LaTeX ở đây..."
            />
          </div>
        </section>

        <section className="space-y-6 rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
          <div>
            <h2 className="text-xl font-semibold text-slate-900">MathLive editor</h2>
            <p className="mt-2 text-sm text-slate-600">
              Khi sửa ở đây, textarea LaTeX sẽ cập nhật theo state chung.
            </p>
          </div>

          <MathFieldEditor value={latexContent} onChange={updateFromMathField} />
          <PreviewPanel latexContent={latexContent} />
        </section>
      </div>
    </main>
  );
}
