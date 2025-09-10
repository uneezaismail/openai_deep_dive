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
