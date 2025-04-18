from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

EXCEL_PATH = BASE_DIR.joinpath('data/operations.xls')
LOG_PATH = BASE_DIR.joinpath('logs/app.log')
REPORTS_PATH = BASE_DIR.joinpath('reports.json')
