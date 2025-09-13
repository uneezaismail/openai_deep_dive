# ModelSettings – Detailed Guide

## Important Note
You will not see `ModelSettings` directly in traces.  
But they are always sent along with your request to the LLM.  
After the model predicts logits (numbers that represent how likely each word is),  
these settings decide how words are picked and how the response is shaped.

Think of it like this:
- The model gives probabilities for many possible next words.  
- ModelSettings are controls you adjust to influence randomness, style, verbosity, penalties, and more.  

---

## Randomness Controls

### `temperature: float | None`
- Controls how random or creative the model’s word choice is.  
- A low temperature = safe and predictable.  
- A high temperature = creative and risky.  

| Temperature | Behavior |
|-------------|-----------|
| `0.0`       | Always picks the most likely word (deterministic, boring). |
| `0.7`       | Balanced creativity (default sweet spot). |
| `1.5`       | Very creative, sometimes chaotic. |

Example:  
Prompt: "Tell me a story about a cat."  
- **0.0** → "A cat sat on the mat."  
- **0.9** → "A curious cat wandered into a neon city full of robots."  

---

### `top_p: float | None` (nucleus sampling)
- Instead of temperature, this limits the probability mass of possible words.  
- Example: `top_p=0.9` means only consider words that together cover 90% of the probability.  

Why useful?  
It ensures rare, weird words are filtered out, but still allows variety.  
- `top_p=1.0` → No filtering, all words possible.  
- `top_p=0.5` → Only a handful of the most likely words are allowed.

---

### `top_k: int | None` (not in this class, but related)
- Sometimes models use **top_k** = only consider the top k most likely words.  
- Example: `top_k=50` → only choose from 50 most likely words.

---

## Repetition Penalties

### `frequency_penalty: float | None`
- Punishes words that are already repeated too often.  
- Higher value = less repetition.  
- Good for avoiding "the cat the cat the cat..." loops.

Example:  
If the model keeps repeating "AI is smart", frequency penalty will make it stop after 1–2 times.  

---

### `presence_penalty: float | None`
- Punishes words that have appeared at all (not about frequency, just presence).  
- Encourages the model to introduce new topics instead of sticking to the same idea.

Example:  
Prompt: "List fruits."  
- No penalty → "apple, apple, apple, orange."  
- With presence penalty → "apple, orange, banana, mango."  

---

## Tool and Execution Controls

### `tool_choice: ToolChoice | None`
- Lets you tell the model which tool to use, if multiple are available.  
- Options:
  - `"auto"` → model decides.  
  - `"required"` → must use a tool.  
  - `"none"` → never use a tool.  
  - `MCPToolChoice("server", "tool_name")` → target a specific tool.

---

### `parallel_tool_calls: bool | None`
- Controls whether the model can call multiple tools in parallel.  
- `True` → faster (e.g., fetch data and translate at the same time).  
- `False` → only one tool per turn.  

---

## Output Size Controls

### `truncation: "auto" | "disabled" | None`
- Decides what happens if the input is too long.  
- `"auto"` → model/provider automatically truncates (keeps last tokens).  
- `"disabled"` → no truncation (may fail if input is too big).  

---

### `max_tokens: int | None`
- Hard limit on how many tokens the model can generate.  
- Example: `max_tokens=50` → answer is short, cut off after ~50 tokens.  

---

## Reasoning Models

### `reasoning: Reasoning | None`
- Special options for reasoning-enabled models (like OpenAI o1).  
- Fields:
  - `effort`: `"minimal"`, `"low"`, `"medium"`, `"high"` → controls how deeply the model reasons.  
  - `summary`: `"auto"`, `"concise"`, `"detailed"` → ask model to summarize its thought process.  

Example:  
- **low effort** → quick math guess.  
- **high effort** → step-by-step logical explanation.  

---

## Response Style

### `verbosity: "low" | "medium" | "high" | None`
- Controls how detailed the answer is.  

| Level | Example |
|-------|---------|
| `low` | "2 + 2 = 4" |
| `medium` | "2 + 2 equals 4, which is basic arithmetic." |
| `high` | "When adding two integers, such as 2 and 2, the sum is 4. This is the foundation of arithmetic addition." |

---

## Metadata and Storage

### `metadata: dict[str, str] | None`
- Extra info you attach (tags, IDs, etc.).  
- Useful for debugging or linking responses.  

---

### `store: bool | None`
- Whether to save the model’s output for later.  
- `True` → keep it.  
- `False` → do not save.  

---

### `include_usage: bool | None`
- Ask model to return usage info (tokens used, costs).  

---

### `response_include: list[ResponseIncludable] | None`
- Request extra data with the response (like logprobs, structured outputs).  

---

### `top_logprobs: int | None`
- How many top tokens’ logprobs to include.  
- Useful for debugging or showing alternate predictions.  

---

## Advanced Extras

### `extra_query: Query | None`
- Add extra query parameters to the request.  

### `extra_body: Body | None`
- Add custom body fields.  

### `extra_headers: Headers | None`
- Add custom headers.  

### `extra_args: dict[str, Any] | None`
- Catch-all bucket for unsupported or experimental params.  
- Use carefully.  

---

## Resolving Settings

Sometimes you define ModelSettings in different places, like:

- Inside an Agent (default settings).
- Inside a RunConfig (temporary, per-run settings).

The system must merge these into one final set before sending to the LLM.
That’s what the resolve() function does.

### How Resolution Works

- Start with base settings (often from the Agent).
- Look at the override settings (from RunConfig).
- For each field:
    - If override has a value → use it.
    - If override is None → keep base value.
- For `extra_args` → merge dictionaries instead of replacing.