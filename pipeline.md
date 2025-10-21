# Eye Screening Form Extraction Pipeline

> **Note:** The layout description below is inferred from common Vietnamese general health check forms because I cannot directly preview `data/LTHN.jpg` in this environment. Please adjust field definitions if the actual form differs.

## 1. Form Layout Overview (Assumed)
- Header block with clinic details and examination date.
- Patient identity section (name, gender, DOB, ID number, address).
- Vital signs / screening metrics table (vision scores, intraocular pressure, etc.).
- Checkbox grids for symptoms, medical history, and referral recommendations.
- Doctor remarks area for free-form text.

## 2. Pipeline Stages & Modules

| Stage | Module (file) | Class / Component | Purpose | Input | Output |
|-------|---------------|-------------------|---------|-------|--------|
| 0. Configuration | `modules/config.py` | `ExtractionConfig` | Centralize paths, OCR languages, region templates. | Optional YAML/JSON or dict | Config object |
| 1. Load Image | `modules/image_loader.py` | `FormImageLoader` | Read form image from disk or stream. | Image path / bytes | Raw BGR image (NumPy array) |
| 2. Preprocess | `modules/preprocessing.py` | `PreprocessingPipeline` | Denoise, enhance contrast, deskew, binarize. | Raw image, config | Preprocessed image |
| 3. Layout Analysis | `modules/layout_analysis.py` | `LayoutAnalyzer` | Detect fixed regions, align template, produce ROIs. | Preprocessed image, config | Dict of ROI metadata + cropped images |
| 4a. Text Fields | `modules/field_extraction.py` | `TextFieldExtractor` | Extract structured text regions (header, patient info). | ROIs, `OCREngine` | Dict `{field_name: text}` |
| 4b. Checkbox Detection | `modules/checkbox_detection.py` | `CheckboxDetector` | Detect ticked/unticked boxes via threshold/ML. | ROI image(s), config | Dict `{checkbox_id: bool}` |
| 4c. Table Parsing | `modules/table_extraction.py` | `TableExtractor` | Extract tables (e.g., vision scores) cell by cell. | Table ROI, `OCREngine` | Structured table data |
| 5. OCR Core | `modules/ocr.py` | `OCREngine` | Wrap Tesseract/EasyOCR call with pre/post-processing. | ROI image, hints | Recognized text |
| 6. Post-processing | `modules/postprocessing.py` | `ResultAssembler` | Clean text, normalize values, merge outputs. | Text dict, checkbox dict, tables | Final patient record dict |

## 3. Execution Flow
1. Instantiate `ExtractionConfig` with field templates and module parameters.
2. `FormImageLoader.load(path)` → raw image.
3. `PreprocessingPipeline.run(image, config)` → enhanced image.
4. `LayoutAnalyzer.analyze(image, config)` → region catalog (`Region` objects / dict).
5. Route ROIs:
   - Text regions → `TextFieldExtractor.extract(rois, ocr)`.
   - Checkbox regions → `CheckboxDetector.detect(roi)`.
   - Table regions → `TableExtractor.extract(roi, ocr)`.
6. `ResultAssembler.assemble(...)` merges everything into a unified patient dict.
7. Persist or serve result (JSON export, database insert, API response).

## 4. Required External Dependencies (indicative)
- `opencv-python` for image handling.
- `numpy` for array operations.
- `pytesseract` or `easyocr` for OCR.
- `scikit-image` or `opencv-contrib-python` for deskew/filters.
- (Optional) `torch` + `detectron2`/`layoutparser` for advanced layout detection.

## 5. Module Interface Checklist
- Every class exposes an initializer accepting `config` or runtime parameters.
- Processing methods should return plain Python dicts or dataclasses for downstream interoperability.
- Logging hooks should be added later for traceability.

## 6. Future Enhancements
- Add document classification to handle multiple form templates.
- Introduce confidence scoring and human-in-the-loop review UI.
- Integrate validation rules (e.g., DOB format, numeric ranges).
