# Test Suite - Saikiran (259053820)

## Functions Tested
- Command Parsing Engine (`handle()`)
- Help Menu Generator
- Error & Invalid Command Handling
- Helper Functions (`_clean()`, `_lower()`, `_list_topics()`, `_get_info()`)

## Run All Tests
```bash
python3 -m unittest 259053820.test.blackbox.specification_based.test_command_parsing 259053820.test.blackbox.specification_based.test_help_menu 259053820.test.blackbox.specification_based.test_error_handling 259053820.test.whitebox.statement_coverage.test_command_parsing_statements 259053820.test.whitebox.branch_coverage.test_command_parsing_branches 259053820.test.whitebox.symbolic_execution.test_command_parsing_symbolic 259053820.test.whitebox.concolic_testing.test_command_parsing_concolic -v
```

## Generate Coverage Report

### Step 1: Run tests with coverage
```bash
python3 -m coverage run --branch -m unittest 259053820.test.blackbox.specification_based.test_command_parsing 259053820.test.blackbox.specification_based.test_help_menu 259053820.test.blackbox.specification_based.test_error_handling 259053820.test.whitebox.statement_coverage.test_command_parsing_statements 259053820.test.whitebox.branch_coverage.test_command_parsing_branches 259053820.test.whitebox.symbolic_execution.test_command_parsing_symbolic 259053820.test.whitebox.concolic_testing.test_command_parsing_concolic
```

### Step 2: Generate text report
```bash
python3 -m coverage report -m
```

### Step 3: Generate HTML report
```bash
python3 -m coverage html
open htmlcov/index.html
```

## One-Line Coverage Command (Windows PowerShell Compatible)
```bash
python3 -m coverage run --branch -m unittest 259053820.test.blackbox.specification_based.test_command_parsing 259053820.test.blackbox.specification_based.test_help_menu 259053820.test.blackbox.specification_based.test_error_handling 259053820.test.whitebox.statement_coverage.test_command_parsing_statements 259053820.test.whitebox.branch_coverage.test_command_parsing_branches 259053820.test.whitebox.symbolic_execution.test_command_parsing_symbolic 259053820.test.whitebox.concolic_testing.test_command_parsing_concolic ; python3 -m coverage report -m ; python3 -m coverage html
```

