from core.controllers import BaseOperationController
from lib.data_loaders import load_raw_df
from models.analysis_schema import ReportRowsParams

class ReportRowsController(BaseOperationController):
    class Meta:
        label = 'report_rows'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = "Report total rows in input file"
        help_detailed = "Performs a raw physical line count."
        param_model = ReportRowsParams
        arguments = BaseOperationController.arguments_from_model(ReportRowsParams)

    def _default(self):
        params = self.get_params()
        if not params: return
        self.app.console.print(f"Reporting Rows: {params.input_file}")
        # Logic...
