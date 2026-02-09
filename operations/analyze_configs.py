from core.controllers import BaseOperationController
from models.analysis_schema import AnalyzeConfigsParams

class AnalyzeConfigsController(BaseOperationController):
    class Meta:
        label = 'analyze_configs'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = "Analyze Valid Configs"
        help_detailed = "Detailed logic for analyze_configs"
        param_model = AnalyzeConfigsParams
        arguments = BaseOperationController.arguments_from_model(AnalyzeConfigsParams)

    def _default(self):
        self.app.console.print("Running analyze_configs...")
