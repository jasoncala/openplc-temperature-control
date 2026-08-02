# Boolean Structured Text Exercise

## Objective

Verify the OpenPLC Editor project structure, variable table, Structured Text
syntax, cyclic task, simulator, and debugger before implementing the main
temperature-control program.

## Program logic

```iecst
TestOutput := TestInput AND Enable;
```

## Validation results

| Test Input | Enable | Expected Output | Actual Output | Result |
|------------|--------|-----------------|---------------|--------|
| FALSE      | FALSE  | FALSE           | FALSE         | PASS   |
| FALSE      | TRUE   | FALSE           | FALSE         | PASS   |
| TRUE       | FALSE  | FALSE           | FALSE         | PASS   |
| TRUE       | TRUE   | TRUE            | TRUE          | PASS   |

## Learning Outcomes

The exercise confirmed:

- Variables are declared separately from the Structured Text body.
- Structured Text assignments use `:=`.
- Statements end in semicolons.
- A Program must execute through a configured task and instance.
- Debug values can be changed and observed through the simulator.