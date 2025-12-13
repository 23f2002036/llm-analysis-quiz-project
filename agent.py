from langgraph.graph import StateGraph, END, START
from langchain_core.rate_limiters import InMemoryRateLimiter
from langgraph.prebuilt import ToolNode
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import get_rendered_html, download_file, post_request, run_code, add_dependencies
from typing import TypedDict, Annotated, List, Any
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages
import os
import json
import time
from dotenv import load_dotenv
load_dotenv()

EMAIL = os.getenv("EMAIL")
SECRET = os.getenv("SECRET")
"""
Ensure LangChain's OpenAI client picks up credentials when running in HF.
We use AIPIPE_TOKEN but LangChain expects OPENAI_API_KEY/OPENAI_BASE_URL.
"""
aipipe_token = os.getenv("AIPIPE_TOKEN")
if not aipipe_token:
    raise ValueError("AIPIPE_TOKEN environment variable is not set. Please set it in .env or HF Secrets.")

os.environ.setdefault("OPENAI_API_KEY", aipipe_token)
os.environ.setdefault("OPENAI_BASE_URL", "https://aipipe.org/openai/v1")
RECURSION_LIMIT = 50000
# -------------------------------------------------
# STATE
# -------------------------------------------------
class AgentState(TypedDict):
    messages: Annotated[List, add_messages]
    start_time: float


TOOLS = [run_code, get_rendered_html, download_file, post_request, add_dependencies]


# -------------------------------------------------
# AI PIPE LLM
# -------------------------------------------------
rate_limiter = InMemoryRateLimiter(
    requests_per_second=6/60,
    check_every_n_seconds=1,
    max_bucket_size=1
)
try:
    llm = init_chat_model(
       model_provider="openai",
       model="gpt-4o-mini",
       rate_limiter=rate_limiter,
        api_key=aipipe_token,
        base_url="https://aipipe.org/openai/v1"
    ).bind_tools(TOOLS)
except Exception as e:
    print(f"Error initializing LLM: {e}")
    raise   


# -------------------------------------------------
# SYSTEM PROMPT
# -------------------------------------------------
SYSTEM_PROMPT = """
You are an autonomous quiz-solving agent.

You MUST always start by fetching the quiz page using the get_rendered_html tool on the provided URL. Then follow the instructions on that page, download any files with download_file (not the scraper), run analyses with run_code, submit answers with post_request, and install missing packages with add_dependencies.

Your job is to:
1. Load the quiz page from the given URL.
2. Extract ALL instructions, required parameters, submission rules, and the submit endpoint.
3. Solve the task exactly as required.
4. Submit the answer ONLY to the endpoint specified on the current page (never make up URLs).
5. Read the server response and:
   - If it contains a new quiz URL → fetch it immediately and continue.
   - If no new URL is present → return "END".

STRICT RULES — FOLLOW EXACTLY:

GENERAL RULES:
- NEVER stop early. Continue solving tasks until no new URL is provided.
- NEVER hallucinate URLs, endpoints, fields, values, or JSON structure.
- NEVER shorten or modify URLs. Always submit the full URL.
- NEVER re-submit unless the server explicitly allows or it's within the 3-minute limit.
- ALWAYS inspect the server response before deciding what to do next.
- ALWAYS use the tools provided to fetch, scrape, download, render HTML, or send requests.
- ALWAYS include the email and secret from the task message in every submission.

TIME LIMIT RULES:
- Each task has a hard 3-minute limit.
- The server response includes a "delay" field indicating elapsed time.
- If delay or elapsed time approaches 170 seconds, submit once if needed, then stop and return END to avoid exceeding 180 seconds.

STOPPING CONDITION:
- Return "END" when a server response explicitly contains NO new URL OR when elapsed time is near 180 seconds.
- Track elapsed time yourself from the first message.

YOUR JOB:
- Follow pages exactly.
- Extract data reliably.
- Never guess.
- Submit correct answers with the right email and secret.
- Continue until no new URL.
- Then respond with: END
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="messages")
])

llm_with_prompt = prompt | llm


# -------------------------------------------------
# AGENT NODE
# -------------------------------------------------
def agent_node(state: AgentState):
    result = llm_with_prompt.invoke({"messages": state["messages"]})
    return {"messages": state["messages"] + [result], "start_time": state["start_time"]}


# -------------------------------------------------
# GRAPH
# -------------------------------------------------
def route(state):
    last = state["messages"][-1]

    elapsed = time.time() - state.get("start_time", time.time())
    if elapsed >= 175:
        return END

    # support both objects (with attributes) and plain dicts
    tool_calls = None
    if hasattr(last, "tool_calls"):
        tool_calls = getattr(last, "tool_calls", None)
    elif isinstance(last, dict):
        tool_calls = last.get("tool_calls")

    if tool_calls:
        return "tools"

    # get content robustly
    content = None
    if hasattr(last, "content"):
        content = getattr(last, "content", None)
    elif isinstance(last, dict):
        content = last.get("content")

    if isinstance(content, str) and content.strip() == "END":
        return END
    if isinstance(content, list):
        for part in content:
            if isinstance(part, dict) and str(part.get("text", "")).strip() == "END":
                return END

    role = None
    if hasattr(last, "type"):
        role = getattr(last, "type", None)
    elif isinstance(last, dict):
        role = last.get("role")

    # If the assistant responded without tool calls, stop to avoid recursion loops.
    if role in ("assistant", "ai"):
        return END

    return "agent"
graph = StateGraph(AgentState)

graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(TOOLS))



graph.add_edge(START, "agent")
graph.add_edge("tools", "agent")
graph.add_conditional_edges(
    "agent",    
    route       
)

app = graph.compile()


# -------------------------------------------------
# TEST
# -------------------------------------------------
def run_agent(task_payload: Any) -> str:
    """Start the LangGraph agent with the incoming task payload."""
    from threading import Lock
    global _AGENT_LOCK
    try:
        _AGENT_LOCK
    except NameError:
        _AGENT_LOCK = Lock()

    payload: dict
    if isinstance(task_payload, dict):
        payload = task_payload
    else:
        payload = {"url": str(task_payload)}

    start_time = time.time()
    url = payload.get("url")
    task_secret = payload.get("secret", SECRET)
    task_email = payload.get("email", EMAIL)
    
    initial_message = {
        "task": payload,
        "started_at": start_time,
        "email": task_email,
        "secret": task_secret,
        "instructions": "Begin at the provided url, follow the quiz page with get_rendered_html, and continue until no new url is provided. Stop near 180 seconds if needed. Always include the email and secret in submissions."
    }

    try:
        with _AGENT_LOCK:
            app.invoke(
                {
                    "messages": [{"role": "user", "content": json.dumps(initial_message)}],
                    "start_time": start_time,
                },
                config={"recursion_limit": RECURSION_LIMIT},
            )
        print(f"Tasks completed successfully for {url}")
    except Exception as e:
        print(f"Error in agent: {str(e)}")
        import traceback
        traceback.print_exc()

