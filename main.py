import json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
import os
import time
from tool import GetWeather
from langchain.globals import set_debug

load_dotenv()


llm = ChatOpenAI(
    api_key=os.getenv('LLM_API_KEY'),
    model=os.getenv('LLM_MODEL_NAME'),
    base_url=os.getenv('LLM_BASE_URL'),
    streaming=False
)


tools = [GetWeather]
llm_with_tools = llm.bind_tools(tools=tools)

messages = [
    { 'role': 'system', 'content': 'You are a helpful weather assistant.'},
    { 'role': 'user', 'content': 'What is the weather in Me Tri - Ha Noi?' }
]

response = llm_with_tools.invoke(messages)
parser = PydanticToolsParser(tools=tools, return_id=True)

parsed_tools = parser.invoke(response)
for tool_call in response.tool_calls:
    for parsed_tool in parsed_tools:
        if tool_call['name'] == parsed_tool.__class__.__name__:
            parsed_tool.id = tool_call['id']

for tool_call in parsed_tools:
    messages.append({
        'role': 'assistant',
        'content': None,
        'tool_calls': response.tool_calls})

    result = tool_call.invoke({})
    messages.append(
        {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
    )


response = llm_with_tools.invoke(messages)
parser = StrOutputParser()
print(parser.invoke(response))

