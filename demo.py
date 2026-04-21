import os
import json
import time
import logging
from dotenv import load_dotenv
from src.orchestrator import handle

# Load environment variables
load_dotenv()

# Setup logging to console (warnings only for cleaner UI)
logging.basicConfig(
    level=logging.WARNING,
    format='%(name)s - %(levelname)s - %(message)s'
)

def run_interactive():
    print("\n🏦 Welcome to the Smart Bank Customer Support Chat!")
    print("Type 'exit' or 'quit' to close the application.\n")
    
    while True:
        try:
            query = input("You: ")
            if query.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            if not query.strip():
                continue
                
            print("Agent is typing...")
            result = handle(query)
            
            # Cleanly format the response based on the status
            print("\n🤖 AGENT RESPONSE:")
            if result.get("status") == "resolved":
                print(f"[{result.get('agent', 'Unknown')} Agent]: {result.get('answer', '')}")
            elif result.get("status") == "redirect":
                print(f"[Receptionist]: {result.get('answer', '')}")
            elif result.get("status") == "escalated":
                print("⚠️  I couldn't confidently answer that. Escalating to a human support agent.")
                print("--- Escalation Ticket ---")
                ticket = result.get('ticket', {})
                print(f"Reason: {ticket.get('reason', 'N/A')}")
                print(f"Original Query: {ticket.get('original_query', 'N/A')}")
            else:
                print(f"[{result.get('status', 'Error')}]: {result.get('message', 'An error occurred')}")
            print("\n" + "-"*50 + "\n")
            
        except KeyboardInterrupt:
            print("\nSession ended. Goodbye!")
            break

if __name__ == "__main__":
    run_interactive()
