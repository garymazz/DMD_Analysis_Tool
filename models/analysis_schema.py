from pydantic import BaseModel, Field
from typing import Optional

class BaseAnalysisParams(BaseModel):
    input_file: str = Field(..., alias='input', description="Path to input file")
    no_header: bool = Field(False, description="Treat first row as data")
    output: Optional[str] = Field(None, description="Output file path")
class ReportRowsParams(BaseAnalysisParams): pass
class AnalyzeSeriesParams(BaseAnalysisParams):
    columns: Optional[str] = Field(None, description="Filter columns")
    row_start: int = Field(0, description="Start row")
    row_end: int = Field(-1, description="End row")
    err_max: float = Field(2.0, description="Max error")
    min_stack: int = Field(1, description="Min stack")
class AnalyzeBandsParams(BaseAnalysisParams):
    columns: Optional[str] = Field(None)
    row_start: int = Field(0)
    row_end: int = Field(-1)
    bands: str = Field(..., description="Bands string")
class AnalyzeConfigsParams(BaseAnalysisParams):
    columns: Optional[str] = Field(None)
    row_start: int = Field(0)
    row_end: int = Field(-1)
    err_max: float = Field(2.0)
class AnalyzeContiguousParams(BaseAnalysisParams):
    columns: Optional[str] = Field(None)
    row_start: int = Field(0)
    row_end: int = Field(-1)
    err_max: float = Field(2.0)
    min_rows: int = Field(1)
    limit: int = Field(0)
    hierarchy: str = Field("dmd,set")
    err_min: float = Field(0.0)
class CorrectDataParams(BaseAnalysisParams): pass
