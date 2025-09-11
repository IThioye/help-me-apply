import subprocess
import json


class LLMInterface:
    def __init__(self, model="gemma3:4b", language="en", prompt_file="data/prompts.json"):
        self.model = model
        self.language = language
        self.prompts = self._load_prompts(prompt_file)

    def _load_prompts(self, filepath: str):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"Could not load prompts file {filepath}: {e}")

    def _run_local_llm(self, prompt: str) -> str:
        """Example call to Ollama CLI. Adapt to your local LLM setup."""
        try:
            result = subprocess.run(
                f"ollama run {self.model}",
                input=prompt,
                capture_output=True,
                check=True,
                text=True,
                shell=True
            )
            # Check both stdout and stderr
            if result.stdout:
                return result.stdout.strip()
            elif result.stderr:
                return result.stderr.strip()
            else:
                return "⚠️ No output received from LLM"
            
        except Exception as e:
            return f"⚠️ LLM error: {e}"

    def build_prompt(self, task: str, user_message: str) -> str:
        """Combine system + user prompt based on task & language."""
        try:
            sys_prompt = self.prompts[task][self.language]
        except KeyError:
            raise ValueError(f"No system prompt found for task={task}, lang={self.language}")

        return f"{sys_prompt}\n\n{user_message}"

    def run(self, task: str, user_message: str) -> str:
        prompt = self.build_prompt(task, user_message)
        return self._run_local_llm(prompt)
