from core.controllers import BaseOperationController
from models.analysis_schema import AnalyzeBandsParams

class AnalyzeBandsController(BaseOperationController):
    class Meta:
        label = 'analyze_bands'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = "Analyze Error Bands"
        help_detailed = "Detailed logic for analyze_bands"
        param_model = AnalyzeBandsParams
        arguments = BaseOperationController.arguments_from_model(AnalyzeBandsParams)

    def _default(self):
        self.app.console.print("Running analyze_bands...")
