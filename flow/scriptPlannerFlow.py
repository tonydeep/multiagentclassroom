import os
# Disable telemetry completely
os.environ['CREWAI_DISABLE_TELEMETRY'] = 'true'
os.environ['OTEL_SDK_DISABLED'] = 'true'
os.environ['OTEL_EXPORTER_OTLP_ENDPOINT'] = ''

from pydantic import BaseModel
from crewai.flow import Flow, start, listen
from flow.crews.scriptPlannerCrew import ScriptPlannerCrew
from dotenv import load_dotenv
from flow.utils.helpers import parse_yaml, save_yaml
import re
load_dotenv()

class ScriptPlannerState(BaseModel):
    script: dict = {}
    roles: dict = {}
    evaluation_history: list = []
    optimization_history: list = []

class ScriptPlannerFlow(Flow[ScriptPlannerState]):
    def __init__(self, **kwargs):
        super().__init__()
        self.problem = kwargs["problem"]
        self.solution = kwargs["solution"]
        self.keywords = kwargs["keywords"]
        self.skill_tree = kwargs["skill_tree"]
        self.script_writer = ScriptPlannerCrew(agent_name="ScriptWriter", task_name="write_script")
        self.script_evaluator = ScriptPlannerCrew(agent_name="ScriptEvaluator", task_name="evaluate_script")
        self.script_optimizer = ScriptPlannerCrew(agent_name="ScriptOptimizer", task_name="optimize_script")
        self.script_analyst = ScriptPlannerCrew(agent_name="ScriptAnalyst", task_name="annotate_script")
        self.roles_writer = ScriptPlannerCrew(agent_name="RolesWriter", task_name="write_roles")

    @start()
    def generate_base_script(self):
        script = self.script_writer.crew().kickoff(inputs={
            "problem": self.problem,
            "solution": self.solution,
            "keywords": self.keywords
        })
        self.state.script = script.raw.replace("```yaml", "").replace("```", "")

    @listen(generate_base_script)
    def optimize_script(self):
        # Step 2: E₀ ← EVALUATOR(S, L₀) - Initial evaluation
        current_script = self.state.script
        print(f"----------------CURRENT SCRIPT-----------------:\n {current_script}")
        
        # Prepare evaluation history (empty for first evaluation)
        previous_evaluations = "\n".join([f"Lần đánh giá {i+1}:\n{eval_text}" for i, eval_text in enumerate(self.state.evaluation_history)]) if self.state.evaluation_history else "Chưa có lần đánh giá nào trước đó."
                
        
        feedback = self.script_evaluator.crew().kickoff(inputs={
            "original_problem": self.problem,
            "original_solution": self.solution,
            "original_script": current_script,
            "skill_tree": self.skill_tree,
            "previous_evaluations": previous_evaluations
        })
        feedback_text = feedback.raw.replace("```yaml", "").replace("```", "")
        print(f"----------------FEEDBACK-----------------:\n {feedback_text}")
        
        # Store evaluation in history
        self.state.evaluation_history.append(feedback_text)
        
        match = re.search(r"overall_score:\s*\[?(\d+)\]?", feedback_text)
        overall_score = int(match.group(1)) if match and match.group(1) != "N/A" else 0

        # Steps 3-4: L ← L₀, E ← E₀, while E.score < τ
        loop_count = 0
        while overall_score < 90 and loop_count < 10:
            loop_count += 1
            # Step 5: L ← OPTIMIZER(S, L, E) - với memory
            # Prepare optimization history
            previous_optimizations = "\n".join([f"Lần tối ưu {i+1}:\n{opt_text}\n\n" for i, opt_text in enumerate(self.state.optimization_history)]) if self.state.optimization_history else "Chưa có lần tối ưu nào trước đó."
            
            
            optimized_result = self.script_optimizer.crew().kickoff(inputs={
                "original_problem": self.problem,
                "original_solution": self.solution,
                "original_script": current_script,  
                "evaluator_feedback": feedback_text,
                "previous_optimizations": previous_optimizations,
                "skill_tree": self.skill_tree
            })
            optimized_script = optimized_result.raw.replace("```yaml", "").replace("```", "")
            
            # Store optimization in history (what was changed and why)
            self.state.optimization_history.append(optimized_script)
            
            current_script = optimized_script
            print("----------------CURRENT SCRIPT-----------------:\n ", current_script)
            
            # Step 6: E ← EVALUATOR(S, L) - với memory
            previous_evaluations = "\n".join([f"Lần đánh giá {i+1}:\n{eval_text}" for i, eval_text in enumerate(self.state.evaluation_history)])
                        
            feedback = self.script_evaluator.crew().kickoff(inputs={
                "original_problem": self.problem,
                "original_solution": self.solution,
                "original_script": current_script,
                "skill_tree": self.skill_tree,
                "previous_evaluations": previous_evaluations
            })
            feedback_text = feedback.raw.replace("```yaml", "").replace("```", "")
            
            # Store evaluation in history
            self.state.evaluation_history.append(feedback_text)
            
            match = re.search(r"overall_score:\s*\[?(\d+)\]?", feedback_text)
            overall_score = int(match.group(1)) if match and match.group(1) != "N/A" else 0
            
            print("----------------FEEDBACK-----------------:\n ", feedback_text)

        self.state.script = current_script

    @listen(optimize_script)
    def annotate_script(self) -> dict:
        annotated_script = self.script_analyst.crew().kickoff(inputs={
            "optimized_script": self.state.script,
            "skill_tree": self.skill_tree
        })
        analyst_notes = parse_yaml(annotated_script.raw)["AnalystNotes"]
        print(f"----------------ANALYST NOTES-----------------:\n {analyst_notes}")
        script = parse_yaml(self.state.script)

        for stage in script.values():
            if isinstance(stage, dict) and 'tasks' in stage:
                for task in stage['tasks']:
                    if isinstance(task, dict) and 'id' in task and task['id'] in analyst_notes:
                        task["notes"] = analyst_notes[task['id']]
                        

        self.state.script = script
        return script


    
def generate_script(folder_path: str, **kwargs: dict) -> dict:
    dynamic_script_path = f"{folder_path}/dynamic_script.yaml"
    scriptFlow = ScriptPlannerFlow(**kwargs)
    script = scriptFlow.kickoff()
    save_yaml(dynamic_script_path, script)

    return script


if __name__ == "__main__":
    with open("flow/crews/config/skill_tree.yaml", "r") as f:
        skill_tree = f.read()
        
    problem = """Xét tính đơn điệu của hàm số $f(x) = \frac{x-1}{x+1}$."""
    solution = """
        **Bước 1: Tìm Tập Xác Định**
        Tập xác định của hàm số $f(x) = \frac{x-1}{x+1}$ là $D = \mathbb{R} \setminus \{-1\}$.

        **Bước 2: Tính Đạo Hàm**
        Đạo hàm của hàm số là $f'(x) = \frac{2}{(x+1)^2}$.

        **Bước 3: Xét Dấu Đạo Hàm, Tính Giới Hạn và Lập Bảng Biến Thiên**
        * **Xét dấu đạo hàm:** Vì $f'(x) = \frac{2}{(x+1)^2} > 0$ với mọi $x \neq -1$, hàm số luôn đồng biến trên các khoảng xác định của nó.
        * **Tính giới hạn:**
            $\lim_{x \to +\infty} f(x) = 1$
            $\lim_{x \to -\infty} f(x) = 1$
            $\lim_{x \to -1^+} f(x) = -\infty$ 
            $\lim_{x \to -1^-} f(x) = +\infty$
        * **Lập Bảng Biến Thiên:**
            | $x$    | $-\infty$ |       $-1$       | $+\infty$ |
            | :------- | :-------: | :----------------: | :-------: |
            | $f'(x)$ |    $+$    |          $\|$          |    $+$    |
            | $f(x)$  |     $1$ $\nearrow$  $+\infty$     | $\|$  |    $-\infty$ $\nearrow$  $1$ |

        **Kết Luận:**
        Hàm số đồng biến trên khoảng $(-\infty; -1)$ và trên khoảng $(-1; +\infty)$.
    """
    script = generate_script(folder_path="test/scripts", 
                             problem=problem,
                             solution=solution,
                             keywords="",
                             skill_tree=skill_tree)