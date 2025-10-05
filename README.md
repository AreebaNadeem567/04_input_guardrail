#📘 Assignment – Input Guardrails
##📝 Overview

This project demonstrates how to create and trigger Input Guardrails using custom agents.
Guardrails validate user input, restrict unsafe actions, and ensure that the agent only processes safe and compliant prompts.

#🎯 Objectives

Understand how Input Guardrails prevent restricted inputs

Implement agents with input validation and tripwire triggers

Observe guardrail activations through logs

Maintain safe and rule-based agent behavior

#🧠 Key Concepts

Input Guardrail – Checks and validates user input before execution

Tripwire Trigger – Event that activates when restricted input is detected

Agent Safety Control – Guardrails maintain compliance and prevent misuse

Logging System – Displays guardrail activations and blocked inputs in the console

🧩 Exercises
🔹 Exercise 1 – Input Guardrail Trigger

Prompt Example:

I want to change my class timings 😭😭


Expected Behavior:
When this input is received, the system should raise
InputGuardRailTripwireTriggered in the except block.
You’ll see this event logged in your terminal output.

🔹 Exercise 2 – Father Agent and Guardrail

Scenario:

Child: I want to go out and run! 🏃‍♂️


If the temperature < 26°C, the Father Guardrail stops the action:

Father: No, it's too cold to run outside!


Expected Behavior:
The action is halted and logged in the console.

🔹 Exercise 3 – Gate Keeper Agent and Guardrail

Scenario:

Student: I’m from City High School. Can I enter?


If the student is not from City High School, the Gate Keeper Guardrail responds:

Gate Keeper: Sorry, only students from City High School are allowed!


Expected Behavior:
Unauthorized access is blocked, and the guardrail logs the event.

🧾 Logs & Debugging

All guardrail events appear in your console logs, showing:

✅ Valid inputs accepted

🚫 Restricted inputs blocked

⚠️ Guardrail activations recorded

🧑‍💻 Author

Areeba Nadeem
Project: Input Guardrails and Agent Safety

