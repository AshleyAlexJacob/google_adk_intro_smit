"""Simple CLI chat for the campus assistant. Run: python chat.py"""

import asyncio
from uuid import uuid4

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from campus_assistant.agent import root_agent

load_dotenv()  # reads GOOGLE_API_KEY from .env

APP = "smit_campus_assistant"
USER_ID = "55401"
SESSION_ID = str(uuid4())


async def main():
    sessions = InMemorySessionService()
    await sessions.create_session(app_name=APP, user_id=USER_ID, session_id=SESSION_ID)

    runner = Runner(agent=root_agent, app_name=APP, session_service=sessions)
    print("Campus assistant. Type quit to exit.")

    while True:
        query = (await asyncio.to_thread(input, "You: ")).strip()
        if not query:
            continue
        if query.lower() in {"quit", "exit", "q"}:
            break

        message = types.Content(role="user", parts=[types.Part(text=query)])
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=message,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                text = event.content.parts[0].text
                if text:
                    print(f"Assistant: {text}")


if __name__ == "__main__":
    asyncio.run(main())
