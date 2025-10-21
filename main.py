"""Eye screening form extraction pipeline orchestrator."""

from modules.checkbox_detection import CheckboxDetector
from modules.config import ExtractionConfig
from modules.field_extraction import TextFieldExtractor
from modules.image_loader import FormImageLoader
from modules.layout_analysis import LayoutAnalyzer
from modules.ocr import OCREngine
from modules.postprocessing import ResultAssembler
from modules.preprocessing import PreprocessingPipeline
from modules.table_extraction import TableExtractor


def run_pipeline(image_path: str) -> dict:
	"""Run the full extraction pipeline and return a structured result."""

	config = ExtractionConfig(template_version="v1")

	loader = FormImageLoader()
	preprocessing = PreprocessingPipeline(config=config)
	analyzer = LayoutAnalyzer(config=config)
	ocr_engine = OCREngine(config=config)
	text_extractor = TextFieldExtractor(ocr_engine=ocr_engine, config=config)
	checkbox_detector = CheckboxDetector(config=config)
	table_extractor = TableExtractor(ocr_engine=ocr_engine, config=config)
	assembler = ResultAssembler(config=config)

	raw_image = loader.load(image_path)
	preprocessed_image = preprocessing.run(raw_image)
	regions = analyzer.analyze(preprocessed_image) or {}

	text_regions = regions.get("text", [])
	checkbox_regions = regions.get("checkbox", [])
	table_regions = regions.get("tables", [])

	text_fields = text_extractor.extract(text_regions) or {}
	checkbox_states = checkbox_detector.detect(checkbox_regions) or {}
	table_data = table_extractor.extract(table_regions) or []

	final_record = assembler.assemble(
		text_fields=text_fields,
		checkbox_states=checkbox_states,
		tables=table_data,
	)

	return final_record or {}


if __name__ == "__main__":
	image_file = "data/LTHN.jpg"
	result = run_pipeline(image_file)
	print("Extraction result:", result)
