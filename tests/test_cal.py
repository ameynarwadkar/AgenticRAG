import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from app.agents.tools.calendar_tool import CalendarTool
from app.config.settings import get_settings

async def main():
    settings = get_settings()
    print(f"Testing Calendar for: {settings.google_calendar_id}")
    
    tool = CalendarTool()
    
    try:
        print("Authenticating and scheduling test event...")
        # Create a test event using the execute method
        response = await tool.execute(
            action="create_event",
            summary="Test Event from AgenticRAG",
            start_datetime="2027-10-10T10:00:00",
            end_datetime="2027-10-10T11:00:00"
        )
        print("\nSUCCESS! Authentication passed and tool executed.")
        print("Response:", response)
    except Exception as e:
        print(f"\nFAILED with error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
