
import pandas as pd
from main import ExcelDataProcessor

def test_upload_file():
    processor = ExcelDataProcessor()
    processor.upload_file()
    assert processor.uploaded_file is not None

def test_display_content_with_file():
    processor = ExcelDataProcessor()
    processor.uploaded_file = "test_file.xlsx"
    processor.display_content()
    assert isinstance(processor.data, pd.DataFrame)

def test_display_content_without_file():
    processor = ExcelDataProcessor()
    processor.display_content()
    assert processor.data is None
