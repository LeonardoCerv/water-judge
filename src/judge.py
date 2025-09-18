import os
import json
import re
from dotenv import load_dotenv
from eth_account import Account
from eth_account.messages import encode_defunct
from cerebras.cloud.sdk import Cerebras
from fastapi import FastAPI
import uvicorn
import logging
import hashlib
from typing import Dict, Any, List

# Setup
load_dotenv()
app = FastAPI(title="Water Judge", description="AI-powered water quality analysis")
logger = logging.getLogger(__name__)

# Initialize Ethereum wallet for decision signing
mnemonic = os.environ.get("MNEMONIC")
if not mnemonic:
    raise ValueError("MNEMONIC environment variable required")
Account.enable_unaudited_hdwallet_features()
account = Account.from_mnemonic(mnemonic)

# Cache for finalized reports to reduce AI calls
_FINALIZE_CACHE = {}
_FINALIZE_ORDER = []

def finalize_report(combined: Dict[str, Any], use_case: str) -> Dict[str, Any]:
    """Combines water analysis data with the intended use case to generate a final AI-synthesized report in the required format."""
    combined_json = json.dumps(combined, ensure_ascii=False)
    cache_key = hashlib.sha256((combined_json + "\n" + (use_case or '')).encode('utf-8')).hexdigest()
    cached = _FINALIZE_CACHE.get(cache_key)
    if cached is not None:
        return cached

    # Build input for AI analysis
    input_parts = [f"Water analysis data: {combined_json}", f"Intended use case: {use_case}"]
    if isinstance(combined, dict) and combined.get('location', {}).get('hint'):
        input_parts.append(f"Location context: {combined['location']['hint']}")
    combined_input = ". ".join(input_parts)

    result = analyze_water(combined_input, use_case)

    # Transform AI result to the expected output format
    final_result = {
        'water_health_percent': f"{result.get('health_percentage', 50)}%",
        'current_water_use_cases': result.get('current_safety_analysis', 'Use with caution; treat before sensitive uses.'),
        'potential_dangers': result.get('risk_analysis', 'Possible microbial or chemical contaminants.'),
        'purify_for_selected_use': result.get('purification_instructions', 'Filter and disinfect before your selected use.'),
    }

    # Cache result to avoid redundant AI calls
    _FINALIZE_CACHE[cache_key] = final_result
    _FINALIZE_ORDER.append(cache_key)
    if len(_FINALIZE_ORDER) > 32:
        old = _FINALIZE_ORDER.pop(0)
        _FINALIZE_CACHE.pop(old, None)

    return final_result

def generate_detailed_plan(final_result: Dict[str, Any], analysis: Dict[str, Any] | None = None) -> List[Dict[str, str]]:
    """Generates a list of 2-3 practical purification steps based on the final analysis, using AI to tailor recommendations."""
    ctx = {
        'final': final_result or {},
        'waterbody': (analysis or {}).get('waterbody') if isinstance(analysis, dict) else None,
        'location': (analysis or {}).get('location') if isinstance(analysis, dict) else None,
    }
    ctx_json = json.dumps(ctx, ensure_ascii=False)

    input_parts = [
        f"Context: {ctx_json}",
        "Generate 2-3 practical purification steps.",
        "Each step should have a clear title and brief description.",
        "Focus on effective, realistic methods."
    ]
    combined_input = ". ".join(input_parts)

    result = analyze_water(combined_input, final_result.get('selected_use', 'drinking'))
    instructions = result.get('purification_instructions', '')

    steps = []
    if instructions:
        step_pattern = r'(?:Step\s*\d+|^\d+\.|\n\s*\d+\.|\n\s*[-*]\s*)'
        parts = re.split(step_pattern, instructions)
        # Parse AI-generated instructions into structured steps
        for i, part in enumerate(parts):
            if part.strip() and len(part.strip()) > 10:
                steps.append({'title': f"Step {i+1}", 'description': part.strip()})

    # Use fallback steps if AI parsing yields insufficient results
    if not steps or len(steps) < 2:
        steps = [
            {'title': 'Filter water', 'description': 'Use clean cloth or filter to remove visible particles.'},
            {'title': 'Disinfect', 'description': 'Boil for 1 minute or use purification tablets.'},
            {'title': 'Safe storage', 'description': 'Store in clean containers, avoid recontamination.'},
        ]

    return steps[:3]

def analyze_water(input_data: str, use_case: str = "drinking") -> dict:
    """Queries the AI model with water data and use case to obtain health percentage, safety analysis, risks, and purification instructions."""
    client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

    # Construct detailed prompt for AI to perform tailored water analysis
    prompt = f"""
    You are a water quality expert. Analyze the SPECIFIC water data provided and give a tailored assessment.

    WATER DATA: {input_data}
    USE CASE: {use_case}

    IMPORTANT: Base your analysis on the ACTUAL values and parameters in the water data above. Do NOT give generic responses.

    Return ONLY valid JSON with exactly these 4 fields:

    {{
        "health_percentage": <number 0-100 based on the specific contaminants and values in the data>,
        "current_safety_analysis": "<1-2 sentences SPECIFIC to the {use_case} use and the actual data provided>",
        "risk_analysis": "<1-2 sentences about the SPECIFIC dangers based on the actual contaminants detected>",
        "purification_instructions": "<2-3 concise steps SPECIFICALLY tailored to treat the contaminants in this water>"
    }}

    Analyze the actual data values and give responses that vary based on what's detected. Be very specific.
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a water quality expert. Analyze the SPECIFIC data provided and give tailored responses that vary based on the actual contaminants and values detected. Never give generic responses."},
                {"role": "user", "content": prompt}
            ],
            model="qwen-3-235b-a22b-thinking-2507",
            max_completion_tokens=1000,
            temperature=0.4,
        )

        ai_response = response.choices[0].message.content
        # Extract JSON from AI response
        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            return create_concise_fallback(input_data, use_case)

    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return create_concise_fallback(input_data, use_case, error=str(e))

def create_concise_fallback(input_data: str, use_case: str, error: str = None) -> dict:
    """Returns a default analysis response when AI processing fails, providing conservative recommendations."""
    return {
        "health_percentage": 50,
        "current_safety_analysis": f"Unable to fully assess safety for {use_case} use. Exercise caution and consider professional testing. Basic filtration and disinfection recommended.",
        "risk_analysis": "Potential risks include microbial contamination and chemical impurities. Professional water testing advised for accurate risk assessment.",
        "purification_instructions": "Filter through clean cloth, boil for 1 minute, or use purification tablets. Store in clean containers and avoid recontamination."
    }

def sign_decision(decision_text: str) -> str:
    """Signs the analysis result with an Ethereum wallet to enable cryptographic verification."""
    message = encode_defunct(text=decision_text)
    signed = account.sign_message(message)
    return signed.signature.hex()

# API Endpoints
@app.get("/")
async def root():
    """Returns basic API metadata including service info and judge address."""
    return {
        "service": "Water Judge API",
        "version": "2.0-simplified", 
        "judge_address": account.address,
        "description": "AI-powered comprehensive water quality analysis with detailed explanations"
    }

@app.post("/judge")
async def judge_endpoint(data: dict):
    """Processes incoming water analysis data, generates quality report and purification plan, then signs the result."""
    try:
        combined = data
        use_case = data.get("use_case", "drinking")
        
        final_result = finalize_report(combined, use_case)
        plan = generate_detailed_plan(final_result, combined)
        signature = sign_decision(json.dumps(final_result, ensure_ascii=False))
        
        return {
            "judge_address": account.address,
            "result": final_result,
            "purification_plan": plan,
            "signature": signature,
            "input_processed": combined
        }
        
    except Exception as e:
        logger.error(f"Judge endpoint error: {str(e)}")
        return {
            "error": str(e),
            "judge_address": account.address
        }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Validate required environment variables before starting
    required_vars = ["MNEMONIC", "CEREBRAS_API_KEY"]
    for var in required_vars:
        if not os.environ.get(var):
            logger.error(f"{var} environment variable is required!")
            exit(1)
    
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    logger.info(f"🚰 Water Judge API starting on {host}:{port}")
    logger.info(f"⚡ Judge Address: {account.address}")
    logger.info("📝 Endpoints: GET / | POST /judge")
    
    uvicorn.run(app, host=host, port=port, log_level="info")