# Audience Automation

## First: Make sure you have python installed
`python -v`

### If you use Windows
`pip install pandas`

### Master Build

Drop the product_map.csv file in to the master directory. **Must be named exact.**

Run `python master_py.py`

A JSON file will be generated of all products sorted per audience.

### Resize Builds

Drop the product_map.csv file in to the resizes directory. **Must be named exact.**

Run `python run.py`

A JSON file will be generated of all products sorted per audience.
