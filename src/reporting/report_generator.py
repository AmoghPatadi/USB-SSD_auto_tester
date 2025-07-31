import logging
import os
from plotly.subplots import make_subplots
import plotly.graph_objects as go

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self, config):
        self.config = config
        self.output_dir = config['reporting']['output_dir']
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_reports(self, results):
        self._generate_html_report(results)
        self._generate_csv_report(results)

    def _generate_html_report(self, results):
        logger.info("Generating HTML report...")
        report_path = os.path.join(self.output_dir, 'report.html')
        with open(report_path, 'w') as file:
            file.write("<html><head><title>Test Report</title></head><body>")
            file.write("<h1>USB/SSD Test Report</h1>")
            
            # Skip summary fields for individual test sections
            summary_fields = {'total_tests', 'passed', 'failed', 'success_rate'}
            
            for test_type, result in results.items():
                if test_type not in summary_fields and isinstance(result, dict):
                    file.write(f"<h2>{test_type.capitalize()} Tests</h2>")
                    file.write(f"<p>Total Tests: {result['total_tests']}</p>")
                    file.write(f"<p>Passed: {result['passed']}</p>")
                    file.write(f"<p>Failed: {result['failed']}</p>")
                    file.write(f"<p>Success Rate: {result['success_rate']}%</p>")
            
            # Add overall summary if available
            if 'total_tests' in results:
                file.write("<h2>Overall Summary</h2>")
                file.write(f"<p>Total Tests: {results['total_tests']}</p>")
                file.write(f"<p>Passed: {results['passed']}</p>")
                file.write(f"<p>Failed: {results['failed']}</p>")
                file.write(f"<p>Success Rate: {results['success_rate']:.1f}%</p>")
                
            file.write("</body></html>")
        logger.info(f"HTML report saved to {report_path}")

    def _generate_csv_report(self, results):
        logger.info("Generating CSV report...")
        report_path = os.path.join(self.output_dir, 'report.csv')
        with open(report_path, 'w') as file:
            file.write("test_type,total_tests,passed,failed,success_rate\n")
            
            # Skip summary fields for individual test sections
            summary_fields = {'total_tests', 'passed', 'failed', 'success_rate'}
            
            for test_type, result in results.items():
                if test_type not in summary_fields and isinstance(result, dict):
                    file.write(f"{test_type},{result['total_tests']},{result['passed']},{result['failed']},{result['success_rate']}\n")
            
            # Add overall summary if available
            if 'total_tests' in results:
                file.write(f"overall,{results['total_tests']},{results['passed']},{results['failed']},{results['success_rate']:.1f}\n")
                
        logger.info(f"CSV report saved to {report_path}")

