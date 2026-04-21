# Smart Bank Customer Support Agent

Welcome to the AI-powered Bank Customer Support Agent! This project is designed to act as an intelligent "first responder" for a bank's mobile app customers. It can answer common questions, figure out exactly what kind of problem the customer has, and instantly forward complicated issues to a real human.

---

## 🌟 Project Highlights

- **Multi-Agent System:** Uses several specialized AI workers instead of just one, ensuring better accuracy.
- **Smart Triage:** Instantly blocks questions that aren't related to the bank (like "give me a pizza recipe").
- **Dynamic Tool Use:** Automatically searches a saved FAQ file if a question looks common, answering the user faster.
- **Escalation Safety Check:** If the AI is not confident in its answer, it stops guessing and creates a support ticket for a human.

---

## 🗺️ How the System Works (The Flow)

Here is exactly what happens when a customer sends a message:

1. **Incoming Message:** The customer asks a question.
2. **The Manager (Orchestrator):** Predictably receives the request and passes it to the receptionist (Triage).
3. **The Receptionist (Triage Agent):** Reads the message and categorizes it. It might use the **FAQ Lookup Tool** to answer instantly. If not, it decides who is best to help: Technical, Billing, or General.
4. **The Expert (Specialist Agent):** The designated worker (e.g., Billing) receives the question, comes up with the best response, and scores its own confidence out of 1.0.
5. **The Final Call (Resolution vs. Escalation):** 
   - **Confidence $\ge$ 0.7:** The system confidently sends the answer to the user.
   - **Confidence < 0.7:** The Manager steps in, stops the message, and uses the **Escalation Tool** to create a ticket for human review.

---

## 📦 Detailed Explanation of Each Component

### 1. The Orchestrator (`src/orchestrator.py`)
This is the brain that holds the system together. It controls the traffic. It takes the customer's input, routes it through the correct Agents, checks the final confidence scores, and decides whether to output the AI's message or make a human support ticket.

### 2. The Triage Agent (`src/agents/triage.py`)
Think of this as the main lobby receptionist. It never solves complex problems. Its only job is to:
- Verify if the query is bank-related.
- Decide if the query is **Technical**, **Billing**, or **General**.
- Optionally call the FAQ Lookup Tool for a quick answer.

### 3. The Specialist Agents (`src/agents/...`)
We use three different agents, one for each specific problem area. They are loaded with specific instructions (Prompts) on how to handle distinct banking domains:
- **`technical.py`**: Handles app crashes, bugs, and login sequences.
- **`billing.py`**: Deals with unknown charges, transfer failures, and card limits.
- **`general.py`**: Handles basic queries like store locations and policy questions.

### 4. The Tools (`src/tools/...`)
- **`faq_lookup.py`**: A search utility. The AI decides autonomously if it should search the `data/faq.json` file for quick answers before moving further.
- **`escalate.py`**: The failsafe generator. It packages all the chat history and the AI's confusion into a standardized ticket format to send to human customer service.

---

## 📊 Evaluation & Monitoring in Production

To build a professional AI, writing the code is only half the battle. Maintaining it is just as important.

- **Why Evaluation matters:** When we update the AI prompts, we don't know if we accidentally broke something without testing it. In a production state, we should maintain a labeled set of 100 historical bank questions and constantly evaluate the AI against this set to ensure triage accuracy and response quality don't drop.
- **Why Monitoring matters:** AI models can drift or degrade silently over time. By using logging tools (like LangSmith), we can track the **Escalation Rate**. If the escalation spikes suddenly, we immediately know the AI is struggling with new user issues and needs adjustment.

---

## 🚀 How to Run the Project

The easiest way to test this agent is using the provided `demo.py` script.

1. Ensure you have activated your Python environment and have your `.env` file loaded with your LLM API keys (`GROQ_API_KEY`).
2. Run the script:
   ```bash
   python demo.py
   ```
3. Watch the terminal! The script will automatically fire off 5 different test cases showing:
   - A Technical question
   - A Billing question
   - A General question
   - An Out-of-Scope (non-bank) question
   - A highly complex question that triggers the human Escalation Tool.
