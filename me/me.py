import json
from clients.clients import get_openai_client
from me.pdf_loader import load_pdfs_text, load_summary
from me.prompts import build_system_prompt
from me.evaluator import ResponseEvaluator
from tools.schemas import TOOLS_SPEC
from tools import pushover as pushover_tools

class Me:
    def __init__(self):
        self.name = "Prateek Jain"
        self.openai = get_openai_client()
        # Load artifacts
        pdfs = ["context_files/linkedin.pdf", "context_files/cv.pdf", "context_files/resume.pdf"]
        self.docs = load_pdfs_text(pdfs)
        self.summary = load_summary("context_files/summary.txt")
        # Evaluator
        self.evaluator = ResponseEvaluator(self.name, self.summary, self.docs)

    # Map tool name -> callable
    def _tool_impl(self, name: str):
        return {
            "record_user_details": pushover_tools.record_user_details,
            "record_unknown_question": pushover_tools.record_unknown_question,
        }.get(name)

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            tool = self._tool_impl(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id
            })
        return results

    def _system_prompt(self) -> str:
        return build_system_prompt(self.name, self.summary, self.docs)

    def rerun_with_feedback(self, reply, message, history, feedback):
        updated_system_prompt = (
            self._system_prompt()
            + "\n\n## Previous answer rejected\nYou just tried to reply, but the quality control rejected your reply\n"
            + f"## Your attempted answer:\n{reply}\n\n"
            + f"## Reason for rejection:\n{feedback}\n\n"
        )
        messages = [{"role": "system", "content": updated_system_prompt}] + history + [{"role": "user", "content": message}]
        response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
        return response

    def chat(self, message: str, history: list[dict]):
        messages = [{"role": "system", "content": self._system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        response = None
        while not done:
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=TOOLS_SPEC
            )
            choice = response.choices[0]
            if choice.finish_reason == "tool_calls":
                tool_message = choice.message
                tool_calls = tool_message.tool_calls
                tool_results = self.handle_tool_call(tool_calls)
                messages.append(tool_message)
                messages.extend(tool_results)
            else:
                # Evaluate quality and possibly rerun
                agent_reply_text = choice.message.content
                evaluation = self.evaluator.evaluate(
                    reply=agent_reply_text,
                    message=message,
                    history=str(history)
                )
                if not evaluation.is_acceptable:
                    print("Response is not acceptable. Sending again for review with feedback.")
                    response = self.rerun_with_feedback(agent_reply_text, message, history, evaluation.feedback)
                else:
                    done = True

        return response.choices[0].message.content
