# Test Suite - Guna Charan (259047752)

## Functions Tested
- User Profile Setup (`setup_profile()`)
- Profile Update Function (`update_profile()`)
- Profile Serialization (`_save_profile()`, `_load_profile()`)
- Reminder Creation Engine (`create_reminder()`)
- Reminder Listing & Searching (`list_reminders()`, `search_reminders()`)
- Reminder Deletion Logic (`delete_reminder()`)

## Run All Tests
```bash
cd "/Users/mohammedmustaq/Downloads/smqa3 1/smqa 3 final"
python3 -m unittest 259047752.test.blackbox.specification_based.test_profile_system 259047752.test.blackbox.specification_based.test_reminder_system 259047752.test.whitebox.statement_coverage.test_profile_statements 259047752.test.whitebox.statement_coverage.test_reminder_statements 259047752.test.whitebox.branch_coverage.test_reminder_branches 259047752.test.whitebox.symbolic_execution.test_reminder_logic_symbolic 259047752.test.whitebox.concolic_testing.test_reminder_branches_concolic -v
```

## Generate Coverage Report

### Step 1: Run tests with coverage
```bash
cd "/Users/mohammedmustaq/Downloads/smqa3 1/smqa 3 final"
python3 -m coverage run --branch -m unittest 259047752.test.blackbox.specification_based.test_profile_system 259047752.test.blackbox.specification_based.test_reminder_system 259047752.test.whitebox.statement_coverage.test_profile_statements 259047752.test.whitebox.statement_coverage.test_reminder_statements 259047752.test.whitebox.branch_coverage.test_reminder_branches 259047752.test.whitebox.symbolic_execution.test_reminder_logic_symbolic 259047752.test.whitebox.concolic_testing.test_reminder_branches_concolic
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

## One-Line Coverage Command
```bash
cd "/Users/mohammedmustaq/Downloads/smqa3 1/smqa 3 final" && python3 -m coverage run --branch -m unittest 259047752.test.blackbox.specification_based.test_profile_system 259047752.test.blackbox.specification_based.test_reminder_system 259047752.test.whitebox.statement_coverage.test_profile_statements 259047752.test.whitebox.statement_coverage.test_reminder_statements 259047752.test.whitebox.branch_coverage.test_reminder_branches 259047752.test.whitebox.symbolic_execution.test_reminder_logic_symbolic 259047752.test.whitebox.concolic_testing.test_reminder_branches_concolic && python3 -m coverage report -m && python3 -m coverage html
```

