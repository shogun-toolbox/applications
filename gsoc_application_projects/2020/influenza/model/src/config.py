from pathlib import Path

COUNTRIES = ['austria', 'belgium', 'germany', 'italy', 'netherlands']

path = Path.cwd()
raw_data_path = path.parent / 'data' / 'raw'
combined_data_path = path.parent / 'data' / 'combined'
cleaned_data_path = path.parent / 'data' / 'cleaned'
processed_data_path = path.parent / 'data' / 'processed'
test_data_path = path.parent / 'data' / 'test'
keywords_path = path.parent / 'data' / 'revised_keywords'
model_path = path.parent / 'models' / 'model.pkl'

years = [2007 + i for i in range(13)]
