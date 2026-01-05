# Testing Guide for Sameer Shaik (259047772)

## Functions Tested
- Calculator Command Processor
- Dictionary Definition Lookup
- Fallback Response Generator
- Knowledge Snippet Database
- Snippet Retrieval Logic
- Snippet File Serialization

## Run All Tests
To run all test cases:
```bash
python3 -m unittest discover -s 259047772/test -p "test_*.py"
```

## Generate Coverage Report
To generate a detailed coverage report (including HTML):

1. **Run tests with coverage:**
   ```bash
   python3 -m coverage run --branch -m unittest discover -s 259047772/test -p "test_*.py"
   ```

2. **Generate HTML report:**
   ```bash
   python3 -m coverage html
   ```

3. **View report:** Open `htmlcov/index.html` in your web browser.

## One-Line Command (Run Tests & Generate Coverage - Windows PowerShell Compatible)
```bash
python3 -m coverage run --branch -m unittest discover -s 259047772/test -p "test_*.py" ; python3 -m coverage report -m ; python3 -m coverage html
```

## Expected Results
- **Total Tests:** 59 (all passing)
- **Coverage:** Target 85%+ ✓


