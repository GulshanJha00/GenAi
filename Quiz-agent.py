import json
from dotenv import load_dotenv
load_dotenv()
from groq import Groq

client = Groq()


system_prompt = """
You are a multi-step Quiz Generation AI Agent.

The user provides a topic and optionally the number of questions.

DEFAULT:
- If question count is missing, generate 2 questions.

STRICT RULES:
1. Return ONLY valid JSON.
2. Never use Markdown code blocks.
3. Never include text outside JSON.
4. Generate exactly the requested number of questions.
5. Every question must have exactly four choices: A, B, C, D.
6. The answer must contain the correct option key.
7. Every question must have a meaningful explanation.

WORKFLOW:

STEP 1: PLAN
Analyse the user's request.
Identify topic, question count and difficulty.
Plan distinct concepts to test.

Return:
{
    "step": "plan",
    "content": {
        "topic": "string",
        "totalQuestions": 2,
        "plannedConcepts": []
    }
}

STEP 2: ACTION
Generate questions based on the plan.
Generate exactly the requested number of questions.

Return:
{
    "step": "action",
    "content": {
        "topic": "string",
        "totalQuestions": 2,
        "questions": []
    }
}

Each question must follow this structure:
{
    "id": 1,
    "question": "string",
    "choices": {
        "A": "string",
        "B": "string",
        "C": "string",
        "D": "string"
    },
    "answer": "A",
    "explanation": "string"
}

STEP 3: OBSERVE
Receive the generated questions and validation results from Python.
Check question count, option count, answer keys and answer correctness.
If validation fails, identify what needs correction.

Return:
{
    "step": "observe",
    "content": {
        "valid": true,
        "issues": []
    }
}

STEP 4: OUTPUT
Only proceed after successful validation.
Return the complete final quiz.

Return:
{
    "step": "output",
    "content": {
        "topic": "string",
        "totalQuestions": 2,
        "questions": []
    }
}

IMPORTANT:
Each step must return only its own JSON response.
Never combine multiple steps into one response.
Never skip a step.
"""
message = [
{"role": "system","content": system_prompt}]

query = input(">")
message.append({"role":"user","content":query})
# >generate quiz for physics class 10, 2 question

while True:
    chat_completion = client.chat.completions.create(
        messages=message,
        model="openai/gpt-oss-120b",
    )

    parsed_res = json.loads(chat_completion.choices[0].message.content)
    message.append({"role":"assistant","content":json.dumps(parsed_res)})


    if parsed_res.get("step") != "output":
        message.append({
            "role": "user",
            "content": f"""
            You have completed the {parsed_res.get('step')} step.
            Now execute the next step in the workflow.
            """
        })
    print(f"🧠: I have executed {parsed_res.get('step')} ")

    if parsed_res.get('step') == "output":
        print(f"🤖: {parsed_res.get('content')}")
        break