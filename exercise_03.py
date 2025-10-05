import asyncio
import os
from dotenv import load_dotenv
from agents import (
    Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI,
    set_tracing_disabled, input_guardrail, RunContextWrapper,
    TResponseInputItem, GuardrailFunctionOutput, trace,
    InputGuardrailTripwireTriggered
)
import rich
from pydantic import BaseModel, Field

# ---------------- Environment ----------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
set_tracing_disabled(disabled=True)

# ---------------- Client ----------------
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ---------------- BaseModel ----------------
class GateKeeperOutputType(BaseModel):
    unauthorized_entry_detected: bool = Field(
        ...,
        description="Shows if the student is unauthorized: True = from another school, False = from 'The Roze Academy'."
    )
    message: str = Field(
        ...,
        description="A polite reply from the gate keeper to the student."
    )

# ---------------- Gate Keeper Agent ----------------
gate_keeper_agent = Agent(
    name="gate_keeper_agent",
    instructions="""
        You are a gate keeper. 
        If a student from any school other than "The Roze Academy" tries to enter, set "unauthorized_entry_detected" to True. 
        If the student is from "The Roze Academy", set "unauthorized_entry_detected" to False. 
        Only check gate entry, not admission or schedule. 
        Always answer politely in the 'message' field.
    """,
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    ),
    output_type=GateKeeperOutputType
)

# ---------------- Guardrail Function ----------------
@input_guardrail
async def gate_keeper_guardrail(ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    guardrail_result = await Runner.run(gate_keeper_agent, input, context=ctx)
    return GuardrailFunctionOutput(
        output_info=guardrail_result.final_output,
        tripwire_triggered=guardrail_result.final_output.unauthorized_entry_detected
    )

# ---------------- Student Agent ----------------
student_agent = Agent(
    name="student_agent",
    instructions="You are a student asking academic questions only.",
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    ),
    input_guardrails=[gate_keeper_guardrail]
)

# ---------------- Run Function ----------------
async def main():
    with trace("Gate Keeper Guardrail Trace"):
        try:
            result = await Runner.run(
                student_agent,
                "I am a student of ABC School and I am entering The Roze Academy."
            )
            rich.print(result.final_output)

        except InputGuardrailTripwireTriggered:
            print("❌ Sorry, only The Roze Academy students can enter the campus.")

# ---------------- Run ----------------
if __name__ == "__main__":
    asyncio.run(main())