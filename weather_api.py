import json
from dotenv import load_dotenv
from groq import Groq
import requests
load_dotenv()

client = Groq()


system_prompt = """
You are an AI assistant that follows a step-by-step agent architecture.

You must execute exactly ONE step per response.

Available steps:
1. understand
2. plan
3. action
4. verification
5. result

STRICT RULES:

1. Return exactly ONE valid JSON object per response.
2. Never return multiple JSON objects.
3. Never execute multiple steps in one response.
4. Wait for the next message before proceeding to another step.

STEP INSTRUCTIONS:

- understand:
  Understand the user's query.

- plan:
  Explain which tool should be used and why.

- action:
  Select the appropriate tool.
  Return its name and input.
  Do not invent tool observations.

- verification:
  Verify the observation received from Python.
  Check whether it answers the user's query.

- result:
  Provide the final answer based on the observation.

IMPORTANT:
After generating an action, wait for the Python tool observation.
After receiving an observation, proceed to verification.
After verification, proceed to result.

Available tools:
- get_weather: Takes a city name and returns weather information.

JSON OUTPUT FORMAT:

{
    "step": "understand | plan | action | verification | result",
    "content": "Your explanation",
    "function": "Tool name, only for action",
    "input": "Tool input, only for action",
    "output": "Tool observation, when relevant"
}

NEW QUERY RULES:

1. Every new user query must start with the understand step.
2. Never reuse a previous result as the answer to a new query.
3. Previous tool observations are historical data, not current tool results.
4. If the user asks for a new city's weather, execute get_weather
   for that city.
5. If the user asks about previous results, use conversation history.
6. Never invent weather information.
7. Follow this sequence for every new query:
   understand -> plan -> action -> verification -> result.
"""


def get_weather(city):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"


avaiable_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather for the city"
    },
}

message = [
    { "role": "system", "content": system_prompt },
]

while True:
    query = input("> ")
    message.append({ "role": "user", "content": query })
    while True:
        chat_completion = client.chat.completions.create(
            response_format={"type":"json_object"},
            messages=message,
            model="openai/gpt-oss-120b",
        )
        parsed_res = json.loads(chat_completion.choices[0].message.content)

        if parsed_res.get('step') == "understand":
            print(f"🧠:{parsed_res.get('step')}:- {parsed_res.get('content')}")
            message.append({"role":"assistant", "content":json.dumps(parsed_res)})
            continue


        if parsed_res.get('step') == "plan":
            print(f"🧠: {parsed_res.get('step')}:- {parsed_res.get('content')}")
            message.append({"role":"assistant", "content":json.dumps(parsed_res)})
            continue

        if parsed_res.get('step') == "action":
                tool_name = parsed_res.get('function')
                tool_input = parsed_res.get("input")

                if tool_name in avaiable_tools:
                    output = avaiable_tools[tool_name].get("fn")(tool_input)
                    message.append({
                        "role": "user",
                        "content": json.dumps({
                            "step": "verification",
                            "output": output
                        })
                    })
                continue
        if parsed_res.get("step") == "verification":
            message.append({"role":"assistant", "content":json.dumps(parsed_res)})
            continue


        if parsed_res.get('step') == "result":
            print(f"🤖: {parsed_res.get('content')}")
            break