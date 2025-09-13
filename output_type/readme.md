# Understanding `output_type` in OpenAI Agents SDK

##  What is `output_type`?
In the **OpenAI Agents SDK**, the `output_type` defines the **shape of the final output** that an agent should return.  

Normally, an agent just gives you free-form text. But sometimes you want the agent to return **structured data** (like JSON, objects, or key-value pairs). That’s where `output_type` comes in.

Think of it as a contract between **your agent** and **your code**:
- You tell the agent: “Whatever you generate, it must match this structure.”
- The SDK validates and parses the output into Python objects for you.

---

##  Why do we use `output_type`?
-  **Structured data** → instead of parsing text manually.
-  **Validation** → ensures the agent sticks to a predictable format.
-  **Easier automation** → you can directly use the agent’s response in code (dicts, dataclasses, etc.).
-  **Error handling** → the SDK checks output against your schema and raises errors if invalid.

---

##  Types of `output_type`

There are 3 main ways to define an `output_type`:

1. **Direct type**  
   Assign a simple type (like `list`, `bool`, or `int`) directly.  
   The agent will validate its response against that type.

2. **Dataclass / Pydantic model**  
   Define your output as a Python dataclass or Pydantic model.  
   The SDK automatically creates and validates a JSON schema from it.

3. **Custom schema (via `AgentOutputSchemaBase`)**  
   For advanced use cases, extend `AgentOutputSchemaBase` to build your own schema.  
   This gives you full control over how the schema looks and how validation is performed.

---

###  Controlling Strictness with `AgentOutputSchema`

By default, the SDK enforces **strict JSON schema validation** (the model must return exactly valid JSON).  
If your schema is not strict-compatible, you can wrap your type with:

- `AgentOutputSchema(YourType, strict_json_schema=True)` → Enforces exact JSON schema.  
- `AgentOutputSchema(YourType, strict_json_schema=False)` → More flexible, allows approximate JSON outputs that may need light correction.

---

##  Strict vs Non-Strict JSON Schema

When using `AgentOutputSchema`, you can control how strictly the agent follows your schema:

###  Strict (`strict_json_schema=True`)
- The agent **must** produce valid JSON according to your schema.  
- Fails fast if the response doesn’t match.  
- **Best for:** cases where you need reliable automation or structured outputs (e.g., API calls, workflows).

###  Non-Strict (`strict_json_schema=False`)
- The agent **tries** to follow your schema, but can be flexible.  
- Can handle cases where the response is close but not perfect.  
- **Best for:** exploratory tasks, partial structure, or when your schema isn’t fully strict-compatible.

---

## In-depth Concepts of `output_type`

When you set an `output_type`, the SDK runs through a series of checks to decide whether it should be used directly or wrapped inside a `"response"` key. The flow is like this:

1. **Plain text case**  
   - If `output_type` is `str` or `None` → treated as plain text.  
   - No JSON schema is generated, and no `"response"` wrapping happens.  

2. **BaseModel or TypedDict case**  
   - If `output_type` is a subclass of `pydantic.BaseModel` or a `TypedDict` → trusted as an **object-shaped schema**.  
   - Used directly, without wrapping.  

3. **Everything else**  
   - If it’s not `str`, not `None`, and not a `BaseModel`/`TypedDict`, the SDK **wraps it inside a dictionary** with the key `"response"`.  
   - Examples:  
     - `int` → `{"response": 42}`  
     - `list[str]` → `{"response": ["a", "b"]}`  
     - `dataclass` → `{"response": {"field": "value"}}`  

4. **Strict schema check**  
   - If `strict_json_schema=True`, the SDK will enforce that the generated schema is strictly valid.  
   - If the schema can’t be made strict → raises a `UserError`.  

5. **Validation at runtime**  
   - When parsing model output, if wrapping was expected but `"response"` is missing, it raises a `ModelBehaviorError`.  
   - This means developer errors (bad schema) and model errors (bad output) are caught separately.  

---

 **Key takeaway:**  
- Only **plain text (`str`/`None`)** and **object-shaped types (`BaseModel`, `TypedDict`)** are left unwrapped.  
- **All other types (dataclasses, lists, ints, bools, etc.)** are automatically wrapped inside a `"response"` key to guarantee valid JSON schema.  


👉 You will also see this `"response"` key clearly in your traces.

📄 [Download the PDF with MCQs on this topic](agent_outputschema_mcqs.pdf)