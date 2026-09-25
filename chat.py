"""Simple CLI chat for the campus assistant. Run: python chat.py"""

import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from campus_assistant.agent import root_agent

load_dotenv()  # reads OPENAI_API_KEY from .env

APP = "campus_assistant"
USER_ID = "student"
SESSION_ID = "1"


async def main():
    sessions = InMemorySessionService()
    await sessions.create_session(
        app_name=APP, user_id=USER_ID, session_id=SESSION_ID
    )
    runner = Runner(agent=root_agent, app_name=APP, session_service=sessions)

    print("Campus Assistant  |  type quit to exit")
    while True:
        query = input("You: ").strip()
        if query.lower() in {"quit", "exit", "q"}:
            break
        if not query:
            continue

        message = types.Content(role="user", parts=[types.Part(text=query)])
        async for event in runner.run_async(
            user_id=USER_ID, session_id=SESSION_ID, new_message=message
        ):
            if event.is_final_response() and event.content and event.content.parts:
                print("Agent:", event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
