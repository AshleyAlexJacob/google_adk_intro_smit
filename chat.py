"""Simple Python CLI chat for the SMIT Peshawar campus assistant."""

from __future__ import annotations

import argparse
import asyncio
import importlib.util
import os
import sys
import uuid
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

APP_NAME = "smit_campus_assistant"
USER_ID = "cli_student"

_STEP_CANDIDATES = {
    1: ROOT / "steps" / "01_what_is_adk" / "agent.py",
    2: ROOT / "steps" / "02_llm_agent_tools" / "agent.py",
    3: ROOT / "steps" / "03_litellm" / "agent.py",
    4: ROOT / "steps" / "04_mcp_tools" / "agent.py",
    5: ROOT / "steps" / "05_agent_garden" / "agent.py",
    6: ROOT / "steps" / "06_streaming" / "agent.py",
    7: ROOT / "steps" / "07_hierarchical_routing" / "agent.py",
    8: ROOT / "steps" / "08_delegation" / "agent.py",
    9: ROOT / "steps" / "09_error_handling" / "agent.py",
}
STEP_AGENTS = {number: path for number, path in _STEP_CANDIDATES.items() if path.is_file()}


def load_root_agent(step: int | None):
    if step is None:
        from campus_assistant.agent import root_agent

        return root_agent

    path = STEP_AGENTS[step]
    spec = importlib.util.spec_from_file_location(f"step_{step}_agent", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load agent from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.root_agent


def _part_text(part) -> str:
    return getattr(part, "text", None) or ""


def _has_api_key() -> bool:
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    if provider == "openai":
        return bool(os.getenv("OPENAI_API_KEY"))
    if provider == "anthropic":
        return bool(os.getenv("ANTHROPIC_API_KEY"))
    return bool(os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"))


async def ask(
    runner: Runner,
    session_id: str,
    query: str,
    *,
    verbose: bool = False,
    stream: bool = False,
) -> str:
    content = types.Content(role="user", parts=[types.Part(text=query)])
    run_config = RunConfig(streaming_mode=StreamingMode.SSE if stream else StreamingMode.NONE)
    final_chunks: list[str] = []
    streamed = False

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=content,
        run_config=run_config,
    ):
        if verbose:
            kind = type(event).__name__
            print(f"  [event] author={getattr(event, 'author', '?')} type={kind} final={event.is_final_response()}")
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if getattr(part, "function_call", None):
                        print(f"  [tool call] {part.function_call.name}({part.function_call.args})")
                    if getattr(part, "function_response", None):
                        print(f"  [tool result] {part.function_response.name}")

        if not event.content or not event.content.parts:
            continue

        texts = [_part_text(part) for part in event.content.parts if not getattr(part, "function_call", None)]
        piece = "".join(t for t in texts if t)
        if not piece:
            continue

        if event.is_final_response():
            final_chunks.append(piece)
        elif stream:
            print(piece, end="", flush=True)
            streamed = True

    final = "".join(final_chunks).strip()
    if stream:
        if not streamed and final:
            print(final, end="", flush=True)
        print()
    return final or "(no response)"


async def new_session(service: InMemorySessionService) -> str:
    session_id = str(uuid.uuid4())
    await service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
    return session_id


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SMIT Peshawar campus assistant CLI chat")
    parser.add_argument(
        "--step",
        type=int,
        choices=sorted(_STEP_CANDIDATES),
        help="Chat with a workshop step agent (1-9). Default: assembled campus_router.",
    )
    parser.add_argument("--stream", action="store_true", help="Print tokens as they arrive (SSE).")
    parser.add_argument("--verbose", action="store_true", help="Print tool calls and events for debugging.")
    parser.add_argument("--message", "-m", help="Send one message and exit (non-interactive).")
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    if not _has_api_key():
        print("Missing API key. Copy .env.example to .env and set GOOGLE_API_KEY.")
        print("Get a Gemini key at https://aistudio.google.com/app/apikey")
        sys.exit(1)

    if args.step and args.step not in STEP_AGENTS:
        print(f"Step {args.step} is not on this branch. Try git checkout complete")
        sys.exit(1)

    root_agent = load_root_agent(args.step)
    session_service = InMemorySessionService()
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
    session_id = await new_session(session_service)

    if args.message:
        if args.stream:
            print("Assistant: ", end="", flush=True)
            await ask(
                runner,
                session_id,
                args.message,
                verbose=args.verbose,
                stream=True,
            )
        else:
            print(f"You: {args.message}")
            reply = await ask(
                runner,
                session_id,
                args.message,
                verbose=args.verbose,
                stream=False,
            )
            print(f"Assistant: {reply}")
        return

    print("=" * 60)
    print(" SMIT Peshawar · Campus Assistant")
    print(f" Agent: {root_agent.name}")
    if args.step:
        print(f" Step:  {args.step}")
    print(" Commands: quit | reset | verbose | stream")
    print("=" * 60)

    verbose = args.verbose
    stream = args.stream
    while True:
        try:
            query = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return
        if not query:
            continue
        lowered = query.lower()
        if lowered in {"quit", "exit", "q"}:
            print("Goodbye.")
            return
        if lowered == "reset":
            session_id = await new_session(session_service)
            print("Started a new conversation.")
            continue
        if lowered == "verbose":
            verbose = not verbose
            print(f"Verbose: {verbose}")
            continue
        if lowered == "stream":
            stream = not stream
            print(f"Stream: {stream}")
            continue

        print("Assistant: ", end="", flush=True)
        reply = await ask(runner, session_id, query, verbose=verbose, stream=stream)
        if not stream:
            print(reply)


if __name__ == "__main__":
    asyncio.run(main())
