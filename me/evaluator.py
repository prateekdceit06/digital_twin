from models.evaluation import Evaluation
from clients.clients import get_gemini_client
from me.prompts import build_evaluator_system_prompt, build_evaluator_user_prompt

class ResponseEvaluator:
    def __init__(self, name: str, summary: str, docs: dict[str, str]):
        self.name = name
        self.summary = summary
        self.docs = docs
        self.gemini = get_gemini_client()

    def evaluate(self, reply: str, message: str, history: str) -> Evaluation:
        system = build_evaluator_system_prompt(self.name, self.summary, self.docs)
        user = build_evaluator_user_prompt(reply, message, history)
        messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
        resp = self.gemini.beta.chat.completions.parse(
            model="gemini-2.0-flash",
            messages=messages,
            response_format=Evaluation
        )
        return resp.choices[0].message.parsed
