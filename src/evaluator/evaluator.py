import json
import time
import os
from typing import Dict, Any, List
from groq import Groq
from src.pipeline import QueryPipeline
from .test_questions import TEST_QUESTIONS

EVAL_PROMPT = """You are an expert grader evaluating an AI assistant's answers.
You will be provided with:
1. The Question.
2. The Expected Intent / Ground Truth Criteria.
3. The AI Assistant's Answer.

Evaluate whether the AI Assistant's Answer correctly satisfies the Question according to the Expected Intent.
Score it as one of the following:
- CORRECT: The answer provides the correct factual information or correctly declines if expected not to find it.
- INCORRECT: The answer provides wrong facts, hallucinates, or fails to satisfy the intent.
- PARTIAL: The answer is partially correct but misses key details.

Output your evaluation in strict JSON format like this:
{
    "score": "CORRECT",
    "reasoning": "A brief explanation of why."
}

Do not output any markdown formatting around the JSON.
"""

class Evaluator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.pipeline = QueryPipeline(config)
        self.client = Groq()
        self.results_dir = config.get("evaluator", {}).get("results_dir", "experiments")
        os.makedirs(self.results_dir, exist_ok=True)

    def evaluate_answer(self, question: str, expected: str, answer: str) -> Dict[str, Any]:
        prompt = f"Question: {question}\nExpected Intent: {expected}\nAI Answer: {answer}"
        try:
            completion = self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {"role": "system", "content": EVAL_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0
            )
            response_text = completion.choices[0].message.content.strip()
            # simple cleanup if LLM wraps in ```json ... ```
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            return json.loads(response_text)
        except Exception as e:
            return {"score": "ERROR", "reasoning": str(e)}

    def run_evaluation(self, experiment_name: str = "default") -> None:
        print(f"Starting evaluation: {experiment_name}")
        results = []
        correct_count = 0

        for tq in TEST_QUESTIONS:
            print(f"Testing Q{tq.id}: {tq.question}")
            start_time = time.time()
            try:
                answer = self.pipeline.query(tq.question)
            except Exception as e:
                answer = f"ERROR: {str(e)}"
            latency = time.time() - start_time

            eval_res = self.evaluate_answer(tq.question, tq.expected_intent, answer)
            
            if eval_res.get("score") == "CORRECT":
                correct_count += 1
            
            results.append({
                "id": tq.id,
                "question": tq.question,
                "expected": tq.expected_intent,
                "answer": answer,
                "latency_sec": round(latency, 2),
                "evaluation": eval_res
            })
            reasoning = eval_res.get('reasoning', '')
            try:
                print(f"  -> Score: {eval_res.get('score')} ({reasoning})")
            except UnicodeEncodeError:
                print(f"  -> Score: {eval_res.get('score')} ({reasoning.encode('ascii', 'ignore').decode()})")

        accuracy = correct_count / len(TEST_QUESTIONS)
        
        report = {
            "experiment_name": experiment_name,
            "timestamp": time.time(),
            "accuracy": accuracy,
            "total_questions": len(TEST_QUESTIONS),
            "correct_count": correct_count,
            "results": results
        }

        file_path = os.path.join(self.results_dir, f"eval_{experiment_name}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        
        print(f"Evaluation complete. Accuracy: {accuracy*100:.1f}%. Report saved to {file_path}")
