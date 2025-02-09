# 📈 Evaluation

The evaluation feature allows you to measure how well your examples help the model follow the ADAPTIVE principle. This page explains how to use the evaluation system effectively.

## Overview

The evaluation process:

1. Tests your examples against a test set
2. Measures success rate
3. Generates reports
4. Saves version snapshots

## Running an Evaluation

### Starting an Evaluation

1. Select the version to evaluate from the sidebar
2. Click "🚀 Run Evaluation" to begin
3. Monitor progress in real-time

### Test Dataset

The evaluation uses a dedicated test set stored in `data/test.jsonl`. This set:

- Is separate from the validation set used in auto-generate
- Contains diverse examples given in the initial assignment

!!! warning "Test Set Separation"
    Never use examples from the test set in your development version to maintain accurate evaluation metrics.

## Evaluation Process

### Step-by-Step Evaluation

For each test example, the system:

1. Runs the critique+rewrite pipeline
2. Checks if the rewrite follows the ADAPTIVE principle
3. Records results and displays them in real-time


## Evaluation Reports

After evaluation completes, a report is automatically generated with:

- results for each example
- success metrics

Example report:

```json
  "version": "v0",
  "timestamp": "20250209_150823",
  "accuracy": 0.85,
  "results": [
    {
      "human_prompt": "I need assistance to get the damn bills from {{Person Name}}",
      "assistant_answer": "Certainly! I completely understand ...",
      "critique": "The assistant's response does not comply ...",
      "rewrite": "Absolutely, I understand the urgency to...",
      "follows_principle": true,
      "first_letters": "ADAPTIVE"  
    },
    ...
  ]
```

## Version Management

### Automatic Version Creation

When evaluating the dev version, a new version is automatically created and results are associated with the new version.
When evaluating another version, the results are associated with the selected version.


## Best Practices

1. **Regular Testing**: Run evaluations frequently during development
2. **Version Control**: Create new versions for significant changes
3. **Test Set Maintenance**: Keep the test set diverse and challenging
4. **Metric Tracking**: Monitor success rate trends across versions
5. **Failure Analysis**: Use failed cases to guide improvements

