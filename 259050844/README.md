# Test Suite - Abhinay Karnati (259050844)

## Functions Tested
- Note Creation Feature (`create_note()`)
- Note Retrieval & Viewing (`retrieve_note()`, `list_all_notes()`)
- Note Deletion Function (`delete_note()`)
- Advanced Note Search (`search_notes()`)
- Note Update & Edit Logic (`update_note()`)
- Note File Storage Handler (`_save_notes()`, `_load_notes()`)

## Run All Tests
```bash

python3 -m unittest 259050844.test.blackbox.specification_based.test_note_creation 259050844.test.blackbox.specification_based.test_note_retrieval 259050844.test.blackbox.specification_based.test_note_deletion 259050844.test.blackbox.specification_based.test_note_search 259050844.test.blackbox.specification_based.test_note_update 259050844.test.blackbox.specification_based.test_note_storage 259050844.test.whitebox.statement_coverage.test_notes_statements 259050844.test.whitebox.branch_coverage.test_notes_branches 259050844.test.whitebox.symbolic_execution.test_note_search_symbolic 259050844.test.whitebox.concolic_testing.test_note_search_concolic -v
```

## Generate Coverage Report

### Step 1: Run tests with coverage
```bash

python3 -m coverage run --branch -m unittest 259050844.test.blackbox.specification_based.test_note_creation 259050844.test.blackbox.specification_based.test_note_retrieval 259050844.test.blackbox.specification_based.test_note_deletion 259050844.test.blackbox.specification_based.test_note_search 259050844.test.blackbox.specification_based.test_note_update 259050844.test.blackbox.specification_based.test_note_storage 259050844.test.whitebox.statement_coverage.test_notes_statements 259050844.test.whitebox.branch_coverage.test_notes_branches 259050844.test.whitebox.symbolic_execution.test_note_search_symbolic 259050844.test.whitebox.concolic_testing.test_note_search_concolic
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
python3 -m coverage run --branch -m unittest 259050844.test.blackbox.specification_based.test_note_creation 259050844.test.blackbox.specification_based.test_note_retrieval 259050844.test.blackbox.specification_based.test_note_deletion 259050844.test.blackbox.specification_based.test_note_search 259050844.test.blackbox.specification_based.test_note_update 259050844.test.blackbox.specification_based.test_note_storage 259050844.test.whitebox.statement_coverage.test_notes_statements 259050844.test.whitebox.branch_coverage.test_notes_branches 259050844.test.whitebox.symbolic_execution.test_note_search_symbolic 259050844.test.whitebox.concolic_testing.test_note_search_concolic && python3 -m coverage report -m && python3 -m coverage html
```

