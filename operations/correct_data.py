from core.controllers import BaseOperationController
from models.analysis_schema import CorrectDataParams

class CorrectDataController(BaseOperationController):
    class Meta:
        label = 'correct_data'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = "Correct Data Window Sizes"
        help_detailed = "Detailed logic for correct_data"
        param_model = CorrectDataParams
        arguments = [(['--input'], {'help': 'Input file', 'dest': 'input_file'})]

    def _default(self):
        self.app.console.print("Running correct_data...")
