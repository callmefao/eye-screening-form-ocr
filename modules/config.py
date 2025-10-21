import json
from pathlib import Path
from typing import Any, Dict, Optional


class ExtractionConfig:
    """Collects pipeline defaults and allows overrides per run."""

    def __init__(self, overrides: Optional[Dict[str, Any]] = None) -> None:
        self._settings: Dict[str, Any] = self._default_settings()
        if overrides:
            self.update(overrides)

    @staticmethod
    def _default_settings() -> Dict[str, Any]:
        # Defaults rely on open-source components only (e.g., vietocr).
        return {
            "ocr": {
                "engine": "vietocr",
                "model": {
                    "cfg": "vgg_transformer",
                    "pretrained": True,
                    "device": "cpu",
                },
                "tokenizer": "vi",
                "height": 32,
                "max_width": 512,
            },
            "layout": {
                "template_version": "v1",
                "expected_size": (1654, 2339),
                "alignment": {
                    "method": "feature_matching",
                    "max_rotation": 5,
                },
            },
            "preprocessing": {
                "grayscale": True,
                "bilateral_filter": {
                    "enabled": True,
                    "diameter": 9,
                    "sigma_color": 75,
                    "sigma_space": 75,
                },
                "clahe": {
                    "enabled": True,
                    "clip_limit": 2.0,
                    "tile_grid_size": (8, 8),
                },
                "deskew": {
                    "enabled": True,
                    "max_angle": 7,
                },
                "binarize": {
                    "method": "adaptive_gaussian",
                    "block_size": 31,
                    "c": 5,
                },
            },
            "regions": {
                "text": [
                    {"id": "patient_name", "bbox": [120, 260, 820, 320]},
                    {"id": "dob", "bbox": [120, 320, 400, 370]},
                ],
                "checkbox": [
                    {"id": "history_diabetes", "bbox": [1100, 640, 1140, 680]},
                ],
                "tables": [
                    {"id": "vision_table", "bbox": [120, 720, 1520, 1100]},
                ],
            },
        }

    def get(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._settings[key] = value

    def update(self, payload: Dict[str, Any]) -> None:
        for key, value in payload.items():
            if isinstance(value, dict) and isinstance(self._settings.get(key), dict):
                self._settings[key].update(value)
            else:
                self._settings[key] = value

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._settings)

    @classmethod
    def from_json(cls, json_path: str) -> "ExtractionConfig":
        data = json.loads(Path(json_path).read_text(encoding="utf-8"))
        return cls(data)
