#!/usr/bin/env python3
import os
import json
from dotenv import load_dotenv
from eth_account import Account
from eth_account.messages import encode_defunct
from cerebras.cloud.sdk import Cerebras
from fastapi import FastAPI

app = FastAPI()

# Load environment variables
load_dotenv()

# Load wallet
mnemonic = os.environ.get("MNEMONIC")
if not mnemonic:
    raise ValueError("MNEMONIC not set")
Account.enable_unaudited_hdwallet_features()
account = Account.from_mnemonic(mnemonic)

def run_structured_analysis(prompt: str, **kwargs) -> dict:
    """Run AI analysis that returns executable Python code building a result dict"""
    client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))
    
    # Add kwargs to the prompt
    if kwargs:
        prompt += f"\nYou have been provided with these additional arguments: {kwargs}"
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Output Python code only that builds the result dict and calls final_answer(json.dumps(result, ensure_ascii=False))."},
            {"role": "user", "content": prompt},
        ],
        model="qwen-3-235b-a22b-instruct-2507",
        max_completion_tokens=2000,
        temperature=0,
    )
    
    code = response.choices[0].message.content
    
    # Execute the code safely
    local_vars = {}
    final_result = None
    
    def final_answer(value):
        nonlocal final_result
        final_result = value
        return value
    
    global_vars = {
        'json': json,
        'final_answer': final_answer,
        **kwargs  # Make kwargs available as variables
    }
    
    try:
        exec(code, global_vars, local_vars)
        if final_result:
            return json.loads(final_result)
        elif 'result' in local_vars:
            return local_vars['result']
        else:
            return {"error": "No result found in executed code"}
    except Exception as e:
        return {"error": f"Failed to execute AI code: {str(e)}", "code": code}

@app.post("/analyze")
async def analyze_scene(data: dict):
    
    scene_description = data.get("scene_description", "")
    additional_args = data.get("additional_args", {})
    
    prompt = f"""
    Using the given scene_description, produce a single Python dict named result with this exact structure:
    environment_context: {{potential_sources: list, notes: str}}
    surface_clarity: {{clarity: str, turbidity: str, surface_contaminants: list, notes: str}}
    color_chemistry: {{observed_colors: list, inferred_risks: list, notes: str}}
    evaluation: {{
        issues_identified: list,
        recommendations: list,
        water_usage_classification: one of safe_for_drinking|agricultural_only|recreational_only|unsafe|requires_purification,
        recommended_uses: list,
        usage_parameters: list of exactly 10 dicts with {{name, value, rationale}},
        confidence: float 0..1,
        caveats: list
    }}
    Rules: be realistic, avoid speculation, only flag high risk with strong visible evidence.
    Output Python code only: import json; build result; final_answer(json.dumps(result, ensure_ascii=False)).
    """
    
    result = run_structured_analysis(prompt, scene_description=scene_description, **additional_args)
    
    signature = sign_decision(json.dumps(result, ensure_ascii=False))
    return {
        "judge_address": account.address,
        "result": result,
        "signature": signature
    }

def sign_decision(decision_text: str):
    message = encode_defunct(text=decision_text)
    signed = account.sign_message(message)
    return signed.signature.hex()

@app.post("/judge")
async def judge(data: dict):
    input_text = data.get("input_text", "")
    
    prompt = f"""
    Using the given water sample data, produce a single Python dict named result with this exact structure:
    environment_context: {{potential_sources: list, notes: str}}
    surface_clarity: {{clarity: str, turbidity: str, surface_contaminants: list, notes: str}}
    color_chemistry: {{observed_colors: list, inferred_risks: list, notes: str}}
    evaluation: {{
        issues_identified: list,
        recommendations: list,
        water_usage_classification: one of safe_for_drinking|agricultural_only|recreational_only|unsafe|requires_purification,
        recommended_uses: list,
        usage_parameters: list of exactly 10 dicts with {{name, value, rationale}},
        confidence: float 0..1,
        caveats: list
    }}
    Rules: be realistic, avoid speculation, only flag high risk with strong evidence from measurements.
    Output Python code only: import json; build result; final_answer(json.dumps(result, ensure_ascii=False)).
    """
    
    result = run_structured_analysis(prompt, input_text=input_text)
    
    signature = sign_decision(json.dumps(result, ensure_ascii=False))
    return {
        "judge_address": account.address,
        "result": result,
        "signature": signature
    }

@app.get("/")
async def root():
    return {
        "message": "Water Judge Service",
        "endpoints": {
            "/judge": "Analyze water sample data (measurements)",
            "/analyze": "Analyze scene description (visual)"
        },
        "judge_address": account.address
    }