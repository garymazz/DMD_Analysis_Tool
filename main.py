#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.app import DMDFramework
from operations.report_rows import ReportRowsController
from operations.analyze_series import AnalyzeSeriesController
from operations.analyze_bands import AnalyzeBandsController
from operations.analyze_configs import AnalyzeConfigsController
from operations.analyze_contiguous import AnalyzeContiguousController
from operations.correct_data import CorrectDataController

# Register controllers once to avoid duplicate handler registration on repeated imports
for controller in [
    ReportRowsController,
    AnalyzeSeriesController,
    AnalyzeBandsController,
    AnalyzeConfigsController,
    AnalyzeContiguousController,
    CorrectDataController,
]:
    if controller not in DMDFramework.Meta.handlers:
        DMDFramework.Meta.handlers.append(controller)

def main():
    with DMDFramework() as app:
        app.run()

if __name__ == '__main__':
    main()
