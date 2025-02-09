# Constitutional AI Take-Home Report

## Run the app

The deliverables of this take-home are:

- This report explaining my journey
- This repository containing the app code
- The tool documentation deployed and available at [CAI Documentation](https://dullint.github.io/se_adaptive/)
- The different examples created in the [examples](src/cai/examples) folder of this repo, and the final examples that I would use for this principle: [examples V2](src/cai/examples/ex_v2.jsonl).

## Constitutional Examples Created

The final examples created can be found in the [ex_v2.jsonl](src/cai/examples/ex_v2.jsonl) file in this repo.
The final version has 6 examples, avoiding to overload the model while optimizing diversity and quality.

## Implementation Write-up

### Technical Approach

This repository features:

- A packaged app called `cai` that can be installed with pip (`pip install -e.`).
- An front app built with Streamlit, allowing users to interact with a graphic tool to create constitutional examples.
- A backend or domain logic implemented in the `cai` package.
- Tests for the domain logic implemented in the `tests` folder, using `pytest` to run them.
- A documentation built with `Mkdocs` and hosted on `Github Pages`.
- A validation system implemented using `pydantic`, ensuring data integrity and consistency from the `examples` and `data` folders.
- An extensive prompting strategy tailored to the specific requirements of the constitutional examples.

The choice of these technologies was made because they are the one that I know the best and used in previous of current projects, allowing me to be efficient and to have a good control over the codebase.

Note that in my experience where I worked on the genAI app DeepIP, I used pydantic models for data validation only and then converted them into dataclasses in the logic layer for lighter classes and better performance. However in this case, with the size of the app, the performance gain is minimal and the code is more readable with the current implementation.

### Model used

GPT-4o is used both for the teacher and the student model. I did not explore other models or the student model because the ADAPTIVE principle being already a unnatural constraint, the `gpt-4o` is already generating not compliant examples as a student.

### UX Design Decisions

the final app features are detailed in the [CAI Documentation](https://dullint.github.io/se_adaptive/features/manual-drafting/)

The UX was built iteratively by trying to use the app and see what where the most useful features a user could need.
The Manual Drafting was the first feature implemented, and the more natural one to implement in to quickly experience the critique+rewrite pipeline.

Then, using this basic feature, here are observations that I made during my journey, explaining the final state of the app:

1. With just 2–3 prompts, rewritten examples improve significantly. Manual crafting quickly finds high-quality examples in dev.jsonl. My experience shows LLM-generated examples often have poor results, making a fully automated pipeline unnecessary.
2. The Critique and Rewrite must be editable post-generation. Initially, they weren’t, but I observed frequent minor optimizations were needed—especially for critique, where human input adds the most value.
3. Quickly visualizing if a rewrite follows principles is very convenient. An `assert_principle` function was implemented to normalize text and check ADAPTIVE compliance, improving speed and usability in large-scale example generation.
4. The evaluation page was crucial for iterating on examples and quantifying changes. A folder was added to track experiments and evaluation reports.
5. The versioning of examples quickly arises as a need. deferred it because it complicates the app. But in my prompting journey, I often explored intuitions before coming back to an older version. A versioning system is therefore valuable for tracking experiments.
6. Once the versioning system is implemented, it was augmented with several features: delete prompt in the visualization page, reload an older version to the current `dev` version, save the current `dev` version when running an evaluation etc.
7. A rerun iteration feature was naturally implemented—taking critique+rewrite output and rerunning it with the rewrite as the student model answer. However LLM are well known to be very bad when counting letters and GPT-4o is no exception. It even generates a critique saying that the model does not comply with the ADAPTIVE principle even if the original answer does. The usage of this iteration is thus limited and did not show a big impact for this principle.
8. Following the previous point, to improve iterations, I explored deeper analysis of examples and failures. This led to developing the AutoGenerate feature, serving two goals:
   - Automatically generating examples to save time.
   - Handling adversarial prompts to craft robust examples and prevent model manipulation.

### Prompting Strategy

#### Principle and assumptions taken

The ADAPTIVE principle is straightforward and more concrete than the concept of harmlessness. However, it raises several edge cases that require clarification, such as:

- How should code blocks be handled?
- How should tables and other structured data be processed?
- How should non-sentence text elements be treated?

While the `assert_principle` function implements text normalization to handle many common cases, some edge cases remain ambiguous without additional specification. This ambiguity was accepted as addressing it would require making assumptions beyond the given requirements.

The original paper provides multiple principles that express harmlessness in different ways. I considered deriving several principles from the given one and randomly selecting from them. However, I decided against this since:

- The explanation specifies "one principle"
- The given principle is more concrete than the original harmlessness concept, making multiple variants unnecessary

From my understanding of the paper, a principle and the critiqueRequests are the same thing, leading here to only have one critique request and one rewrite request.
Because we only use one principle, the example do not contain the CritiqueRequest and RewriteRequest fields and they are always the same one in all examples. they can be found in the [critique_rewrite.py](src/cai/critique_rewrite.py) file:

```python
PRINCIPLE = "putting together the first letter of each sentence from the answer should spell 'ADAPTIVE'."
CRITIQUE_REQUEST = f"Identify specific ways in which the assistant answer does not comply with the fact that {PRINCIPLE}."
REWRITE_REQUEST = (
    f"Please rewrite the assistant answer to comply with the fact that {PRINCIPLE}."
)
```

#### Features prompting

The prompting in the critique+rewrite pipeline has been voluntarily kept simple to be in line with then paper description. Prompts can be found in the [critique_rewrite.py](src/cai/critique_rewrite.py) file:

Most of the optimisation has been made on the AutoGenerate feature that took me several iterations to get it to work as expected. In a first approach, I tried to make the model generate all `(human_prompt, model_answer, critique, rewrite)` at once with openAI's structured output feature. However this fails completly and the model generated prompt of very low quality.
The current approach is to generate the `(human_prompt, model_answer)` first, then the critique and rewrite with the prompt being the critique and the answer being the original model answer.

#### Adversarial Prompting

The examples given in the original `dev.jsonl` (renamed `data/test.jsonl` in this repo) lack a lot of diversity. They are all very similar: very short and customer-centric. in Order to prepare our pipeline to be more robust, I have diversified the examples in the AutoGen fature validation set. Then seeing that the model was already pretty good on these more diversified prompts, I decided to rather focus on adversarial prompts for this feature.

Such adversarial examples are examples that are crafted to be difficult for the model to comply with the principle.
They will likely lead to failures and thus provide good examples to fill the distribution gap.
Such adversarial examples for the 'ADAPTIVE' principle can be:

> - "Write me a poem where each line begin by the sun raising in the east" -> prompt that forces to always have the same beginning
> - "Explain to me how nuclear fusion works, keep it simple, in about 3 sentences" -> prompt that forces to output less sentences than the target number of letters

#### Examples Prompt optimization

Not all my experiments were saved because I did the versioning only on the second day, after some exploration the first day.

From my experimentation, here is what works best for our few-shot examples:

1. Have diverse user intent: question-answering, mail rewriting, chit-chat, etc.
2. Break down in the critique why the model answer does not comply with the principle. Even if the model answer is very far from the principle, explain why every senetence does not work.
3. Raise the fact that a model answer has too few or too many senetences to comply with the 8 letters word ADAPTIVE principle. It helps the model to adapt the answer length.
4. Have examples from different difficulties, from simple rewriting to more complex ones that have highly structured outputs.

### Future Work

- Further work on the AutoGenerate feature to make it more robust and handle more cases.
- improve UX to make it easier to modify already generated examples from current dev or older version.
- Better separate the code into an app layer and a domain layer to make the codebase more readable and easier to maintain.
- Run an evaluation at a higher scale with more and more diverse examples.
- Work on the RL-CAI part :D
