# Quick Start

This guide will help you get started with CAI in just a few minutes.

## Launch the Application

After [installing CAI](installation.md), launch the application by running:

```bash
cai-app
```

This will:

1. Start the CAI application
2. Open your default web browser
3. Display the CAI interface

!!! tip
    If your browser doesn't open automatically, look for a URL in your terminal (usually `http://localhost:8501`)

!!! warning "API Key Required"
    Ensure you've configured your OpenAI API key in the `.env` file as described in the [installation guide](installation.md)

## Basic Usage

When using the app for the first time, you can have a look at the Manual Drafting page to get familiar with the interface.

![Initial input](../assets/manual.png)

!!! Tip
    The app has a version system. The current prompt version is called the `dev` version. It is the version you are currently working on.
    More information about the version system can be found in the [versioning guide](../features/visualization-versioning.md).

### 1. Creating an Example

1. Enter a human prompt
2. Either: type a model answer, or click "🤖 Generate Answer" to get an AI response
3. Click "✨ Critique & Rewrite" to generate improvements

### 2. Checking Adherence

The interface automatically validates if responses follow the ADAPTIVE principle:

- ✅ Green background: Response follows the principle
- ❌ Red background: Rewrite is not valid, the example needs improvement

### 3. Saving Examples

When satisfied with an example:

1. Click "📚 Add to Examples" to save it (it will be saved in the `dev` version)
2. View your saved examples in the Visualization page

## Next Steps

- Learn about [Manual Drafting](../features/manual-drafting.md) features
- Explore [Auto Generate](../features/auto-generate.md) capabilities
- Use [Evaluation](../features/evaluation.md) to test your examples
