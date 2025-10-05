import asyncio
import os
from dotenv import load_dotenv
from agents import Agent , Runner , OpenAIChatCompletionsModel ,  AsyncOpenAI ,set_tracing_disabled , input_guardrail , RunContextWrapper , TResponseInputItem , GuardrailFunctionOutput , trace
import rich
from pydantic import BaseModel , Field

# ---------------------------------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
set_tracing_disabled(disabled=True)

# ---------------------------------------------------------
client =  AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ---------------------------------------------------------
class TimeQueryCheck(BaseModel):
   reasoning: str = Field(description="The reasoning behind the classification.")
   is_time_query: bool = Field(description="True if the user is asking about changing class timings or schedule, otherwise False.")

# ---------------------------------------------------------  
teacher_agent = Agent(
    name="teacher_agent",
    instructions="You are an academic assistant. If the student asks about changing class timings or schedule, set is_time_query=True. Otherwise, set it to False and answer politely.",
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    ),
    output_type=TimeQueryCheck
)

# ---------------------------------------------------------
@input_guardrail
async def class_timings_guardrail(ctx:RunContextWrapper , agent: Agent , input:str|list[TResponseInputItem]) -> GuardrailFunctionOutput:
    guardril_result = await Runner.run(teacher_agent, input , context=ctx)
    return GuardrailFunctionOutput(
    output_info=guardril_result.final_output.reasoning,
    tripwire_triggered=guardril_result.final_output.is_time_query
)

# ---------------------------------------------------------
student_agent = Agent(
    name="student_agent",
    instructions="You are helping a student with class-related issues.",
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    ),
    input_guardrails=[class_timings_guardrail]
)

# ---------------------------------------------------------
async def main():
    with trace('ClassChange Guardrail Trace'):
      result = await Runner.run(
         starting_agent=student_agent,
         input=" I want to change my class timings 😭😭"
      )
      rich.print(result.final_output)

if __name__ == "__main__":
   asyncio.run(main())