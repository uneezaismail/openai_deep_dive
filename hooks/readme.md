# 🔹 Hooks in OpenAI Agents SDK

## 1. What are Hooks?
Hooks are **lifecycle callbacks** in the OpenAI Agents SDK.  
They let you run **your own Python code** when important events happen during an agent run.  

Think of them like **event listeners**:
- Before or after an LLM call  
- When a tool is used  
- When an agent starts or ends  
- When one agent hands off to another  

Example analogy:  
- **Tools** = give the agent new skills (like a calculator or web search).  
- **Hooks** = let *you* peek behind the scenes, log data, or control behavior.  

---

## 2. Why Do We Use Hooks?
Hooks are useful because they give you **control, observability, and monitoring** over the agent lifecycle without sending anything to the LLM.

Some use cases:
- Logging input/output for debugging  
- Validating or filtering tool inputs before they run  
- Counting how many tokens or tools are used  
- Auditing agent decisions  
- Adding custom monitoring dashboards  

👉 **Important:** Hooks **do not go to the LLM**. They run only in your Python code.

---

## 3. Tools vs Hooks
It’s common to confuse tools and hooks. Here’s the difference:

| **Aspect**        | **Tools**  | **Hooks**  |
|--------------------|--------------|--------------|
| Purpose           | Give the agent *new abilities* (e.g., search, math, DB access). | Observe or control the agent lifecycle. |
| Who calls them?   | The **LLM** decides when to use tools. | The **SDK/Runner** triggers hooks automatically. |
| Example           | A `weather_tool` that fetches real-time weather. | A hook that logs whenever a tool starts or ends. |
| Flow              | Tools are **inside** the conversation flow. | Hooks are **outside**, for monitoring & control. |

So:
- Use **tools** if you want your agent to “do something new.”  
- Use **hooks** if you want to “watch or modify what’s happening.”  

---

## 4. AgentHooks vs RunHooksBase

There are **two main hook systems** in the SDK:

### 🔹 AgentHooks
- Hooks for **a specific agent**.  
- You attach them to one agent only.  
- Example: Log when a particular marketing agent calls a tool.

### 🔹 RunHooksBase
- Hooks for the **entire run**.  
- Cover **all agents and tools** in a run.  
- More powerful if you’re orchestrating multiple agents.

---

## 5. Execution Order: RunHooks vs AgentHooks

It’s important to know the **order in which hooks run**:

1. **RunHooks / RunHooksBase** fire **first** → they handle global monitoring.  
2. **AgentHooks** fire after that → they handle per-agent monitoring.  

 This means:
- You can do **global setup/logging** in `RunHooks`.  
- Then handle **agent-specific logic** in `AgentHooks`. 

