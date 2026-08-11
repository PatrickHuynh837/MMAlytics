# Data Pipeline

## Data Sources

### UFC Fight Data

Primary historical fight data is collected from UFCStats.

### Betting Odds

Betting odds are collected through the UFC Odds API.

## Data Ingestion

The pipeline currently uses:

- Python
- Pandas
- Beautiful Soup
- Playwright
- UFCStats
- UFC Odds API

UFC data is primarily scraped from the UFC website.

Betting data is retrieved through the odds API.

## Data Processing

### Cleaning

Data is cleaned before being stored in the database.

The goal is to perform sufficient cleaning to ensure the stored
data is usable while avoiding unnecessary transformations that
could make the original data difficult to recover.

### Transformation

Additional transformations are performed to produce data suitable
for downstream feature engineering and machine learning.