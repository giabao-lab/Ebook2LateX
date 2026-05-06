import { useEffect, useRef } from "react";
import "mathlive";

export default function MathFieldEditor({ value, onChange }) {
  const fieldRef = useRef(null);

  useEffect(() => {
    if (fieldRef.current && fieldRef.current.value !== value) {
      fieldRef.current.value = value;
    }
  }, [value]);

  useEffect(() => {
    const field = fieldRef.current;
    if (!field) {
      return undefined;
    }

    const handleInput = () => onChange(field.value || "");
    field.addEventListener("input", handleInput);

    return () => field.removeEventListener("input", handleInput);
  }, [onChange]);

  return (
    <math-field
      ref={fieldRef}
      className="min-h-28 w-full rounded-xl border border-slate-200 bg-white p-4 text-lg shadow-sm"
      aria-label="MathLive formula editor"
    />
  );
}
