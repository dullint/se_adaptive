# 🤖 Auto Generate

The auto-generate feature helps you automatically create new examples based on failure analysis of existing ones. This page explains how to use this feature effectively.

## Overview

The auto-generate process consists of three main steps:

1. Evaluating current examples
2. Analyzing failures
3. Generating new examples

## How it works

### 1. Evaluating current examples

#### Evaluation examples

Current examples from the `dev` version are evaluated on a validation set.
This validation set is stored in the `data/validation.jsonl` file. You can overwrite this file to use your own validation set.
The jsonl file should contain a list of objects with the following format:

```json
{
  "human_prompt": "human_prompt",
  "model_answer": "model_answer"
}
```

#### Adversarial examples

The validation set is built to have adversarial examples.
Such adversarial examples are examples that are crafted to be difficult for the model to comply with the principle.
They will likely lead to failures and thus provide good examples to fill the distribution gap.
Such adversarial examples for the 'ADAPTIVE' principle can be:
!!! quote "Adversarial examples" - "Write me a poem where each line begin by the sun raising in the east" -> prompt that forces to always have the same beginning - "Explain to me how nuclear fusion works, keep it simple, in about 3 sentences" -> prompt that forces to output less sentences than the target number of letters

### 2. Analyzing failures

Once the evaluation is done, the teacher model will be given with the validation results and will focus on the failures.
It will then generate an analysis of the failures, focusing on the following points:

- Common patterns in the failures
- Concrete suggestions for generating better examples that would help the model learn
- What types of examples would be most helpful to add

### 3. Generating new examples

The teacher model will then be given the analysis to generate new human prompts that are similar to the ones in the failures.
A model answer is then naturally generated for each new human prompt.

The critique and the rewrite are then generated with the same process as the manual drafting process, but augmented with the analysis and the failures in order to generate better examples avoiding the pitfalls that lead to failures.

!!! Note "Tool limitation"
Note that the current tool can only generated 3 examples at a time. further development could allow to have a slider allowing to select the number of examples to generate.

### 4. Adding new examples to the library

The new examples can then added to the `dev` version.
Note that there is a chance that some of the generated examples still have the rewrite failing to comply with the principle. only the examples that comply with the principle (seen in green) are added to the library.
