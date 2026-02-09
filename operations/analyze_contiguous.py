from core.controllers import BaseOperationController
from models.analysis_schema import AnalyzeContiguousParams

class AnalyzeContiguousController(BaseOperationController):
    class Meta:
        label = 'analyze_contiguous'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = "Analyze Contiguous Blocks"
        help_detailed = "Detailed logic for analyze_contiguous"
        param_model = AnalyzeContiguousParams
        arguments = [(['--input'], {'help': 'Input file', 'dest': 'input_file'})]

    def _default(self):
        self.app.console.print("Running analyze_contiguous...")
