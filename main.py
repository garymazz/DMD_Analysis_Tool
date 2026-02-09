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

# Register Controllers
for c in [ReportRowsController, AnalyzeSeriesController, AnalyzeBandsController, 
          AnalyzeConfigsController, AnalyzeContiguousController, CorrectDataController]:
    DMDFramework.Meta.handlers.append(c)

def main():
    with DMDFramework() as app:
        app.run()

if __name__ == '__main__':
    main()
