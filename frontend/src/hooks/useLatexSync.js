import { useCallback, useState } from "react";

export function useLatexSync(initialValue = "") {
  const [latexContent, setLatexContent] = useState(initialValue);

  const updateFromText = useCallback((value) => {
    setLatexContent(value);
  }, []);

  const updateFromMathField = useCallback((value) => {
    setLatexContent(value);
  }, []);

  return {
    latexContent,
    setLatexContent,
    updateFromText,
    updateFromMathField,
  };
}
