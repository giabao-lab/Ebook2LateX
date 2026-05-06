from typing import List
import os
import base64
import json

try:
    from pix2tex.cli import LatexOCR
except ImportError:  # pragma: no cover - dependency may be installed later
    LatexOCR = None

import requests


class OCREngine:
    def __init__(self) -> None:
        # prefer local pix2tex if available
        self.model_available = LatexOCR is not None
        self.model = LatexOCR() if self.model_available else None

        # Mathpix credentials (optional)
        self.mathpix_app_id = os.getenv("MATHPIX_APP_ID")
        self.mathpix_app_key = os.getenv("MATHPIX_APP_KEY")

    def image_to_latex_mathpix(self, image_path: str) -> str:
        if not (self.mathpix_app_id and self.mathpix_app_key):
            return ""

        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")

        payload = {
            "src": f"data:image/png;base64,{img_b64}",
            "formats": ["latex_styled", "latex_normal"],
        }

        headers = {
            "app_id": self.mathpix_app_id,
            "app_key": self.mathpix_app_key,
            "Content-type": "application/json",
        }

        try:
            resp = requests.post("https://api.mathpix.com/v3/text", headers=headers, data=json.dumps(payload), timeout=30)
            resp.raise_for_status()
            data = resp.json()
            # prefer latex_normal if available
            return data.get("latex_normal") or data.get("latex_styled") or ""
        except Exception:
            return ""

    def image_to_latex(self, image_path: str) -> str:
        # 1) Try local pix2tex model
        if self.model is not None:
            try:
                return self.model(image_path)
            except Exception:
                # fallback to mathpix if configured
                pass

        # 2) Try Mathpix API if credentials are present
        latex = self.image_to_latex_mathpix(image_path)
        return latex or ""

    def batch_image_to_latex(self, image_paths: List[str]) -> List[str]:
        results: List[str] = []
        for p in image_paths:
            results.append(self.image_to_latex(p))
        return results
