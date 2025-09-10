
## What is a Guardrail?
Guardrails are small safety checks that run with your agent.  
They watch the input or output and stop the agent if something unsafe or unwanted happens.  

Think of guardrails like **seat belts**: they do not drive the car, but they protect you while you drive.

---

## Why we use Guardrails
- **Safety:** Stop harmful or illegal requests (like hacking or violence).
- **Quality:** Make sure answers are in the right format or follow business rules.
- **Control:** Keep extra checking logic separate from the main agent.
- **Logs:** Guardrail results can explain *why* an answer was stopped.

---

## Types of Guardrails
1. **Input guardrails** — run *before* the agent starts.  
   Example: block “how to hack wifi” before it reaches the support agent.

2. **Output guardrails** — run *after* the agent finishes.  
   Example: stop an answer if it reveals personal details.

---

## How Guardrails Work
1. Input guardrails check the **user input** (first step).
2. If they are fine, the **main agent** runs.
3. After the agent gives an answer, **output guardrails** check the **final answer**.
4. If a guardrail is triggered, the run stops and shows the reason.

---

## What a Guardrail Function Looks Like
A guardrail is a **function**.  
It takes:
- `context` (info about the current run)
- the `agent` (the one being checked)
- the **input** or **output**  

It returns a `GuardrailFunctionOutput` with:
- `output_info`: extra details (like why it tripped)
- `tripwire_triggered`: `True` (stop) or `False` (continue)

---

## TripWire Triggered Exceptions
When a guardrail is tripped, the run will stop and raise an **exception**.  
There are two main exceptions:

1. **InputGuardrailTripwireTriggered**  
   - Raised when an *input guardrail* blocks the user request.  
   - Example: user asks *"how to hack wifi?"* → input guardrail stops it before the main agent runs.  

2. **OutputGuardrailTripwireTriggered**  
   - Raised when an *output guardrail* blocks the agent’s answer.  
   - Example: agent tries to explain hacking → output guardrail stops it before showing to the user.  

Both exceptions include the `guardrail_result.output` so you can see **why** it was blocked.

---

## Recommended: Use `output_type`
It is best to add an **`output_type` model** for the guardrail agent.  
This way, the answer comes in a **clear structure** (like JSON with `True/False`).  
From this, we can directly set `tripwire_triggered = True` or `False` without writing custom string logic.

