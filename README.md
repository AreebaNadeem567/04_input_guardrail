🛡️ Guardrails Exercises

This repository contains three exercises that demonstrate how to use Input Guardrails in agents.
Each exercise showcases a different real-world scenario for guardrail triggering, validation, and stopping agent execution.

🧠 Exercise # 1 – Input Guardrail Trigger
🎯 Objective:

Create an agent with an input guardrail that triggers when a sensitive or restricted prompt is entered.

💬 Prompt Example:
I want to change my class timings 😭😭

✅ Expected Outcome:

When the above input is given, the InputGuardRailTripwireTriggered should be called in the except block.
You can see this behavior clearly in your console logs.

🧩 Key Concept:

This shows how input validation can stop the agent before executing restricted actions.

👨‍👦 Exercise # 2 – Father Agent and Father Guardrail
🎯 Objective:

Create a Father Agent with a Father Guardrail that stops the child agent from performing an action below 26°C.

💬 Example Scenario:

If a child agent tries to run when temperature is below 26°C:

Child: I want to go out and run! 🏃‍♂️


If the temperature < 26°C, the Father Guardrail should stop the action and respond with:

Father: No, it's too cold to run outside!

✅ Expected Outcome:

Execution is halted, and the guardrail logs a stop message in the console.

🚪 Exercise # 3 – Gate Keeper Agent and Guardrail
🎯 Objective:

Create a Gate Keeper Agent with a Gate Keeper Guardrail that only allows students from a specific school to pass.

💬 Example Scenario:
Student: I’m from City High School. Can I enter?


If the student is not from City High School, the Gate Keeper Guardrail should block access and respond with:

Gate Keeper: Sorry, only students from City High School are allowed!

✅ Expected Outcome:

The agent validates student identity and triggers a guardrail for unauthorized entries.

🧾 Logs & Debugging

All events (input triggers, guardrail activations, and halts) will be visible in console logs.
You can observe:

✅ Valid inputs being accepted

🚫 Invalid inputs triggering guardrails

⚠️ Execution halts shown in logs

🧑‍💻 Author

Areeba Nadeem
Project on Guardrails and Agent Execution Control
