from core.controllers import BaseOperationController
from models.analysis_schema import AnalyzeSeriesParams

class AnalyzeSeriesController(BaseOperationController):
    class Meta:
        label = 'analyze_series'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = "Analyze Stack Series"
        help_detailed = "Detailed logic for analyze_series"
        param_model = AnalyzeSeriesParams
        arguments = [(['--input'], {'help': 'Input file', 'dest': 'input_file'})]

    def _default(self):
        self.app.console.print("Running analyze_series...")
