#!/usr/bin/env python3
"""
Simplified Water Judge API - Single File Solution
Generates comprehensive water quality analysis with detailed explanations
"""

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

# Additional imports for image analysis
import io
import hashlib
import time
from contextlib import contextmanager
from typing import Dict, Any, List

# Plain-text reference ranges for strip analytes (for qualitative guidance only)
_REFERENCE_RANGES_TEXT = (
    "Total Alkalinity: 40 - 240 mg/L\n"
    "pH: 6.8 - 8.4\n"
    "Hardness: TBD (To Be Determined)\n"
    "Hydrogen Sulfide: 0 mg/L\n"
    "Iron: 0 - 0.3 mg/L\n"
    "Copper: 0 - 1 mg/L\n"
    "Lead: 0 - 15 µg/L\n"
    "Manganese: 0 - 0.1 mg/L\n"
    "Total Chlorine: 0 - 3 mg/L\n"
    "Free Chlorine: 0 - 3 mg/L\n"
    "Nitrate: 0 - 10 mg/L\n"
    "Nitrite: 0 - 1 mg/L\n"
    "Sulfate: 0 - 200 mg/L\n"
    "Zinc: 0 - 5 mg/L\n"
    "Sodium Chloride: 0 - 250 mg/L\n"
    "Fluoride: 0 - 4 mg/L"
)

# Best-effort formatter to convert any strip-related content to a plain-text summary
def _format_strip_context_text(obj: Dict[str, Any] | None) -> str:
    try:
        if not isinstance(obj, dict):
            return ""
        # Accept preformatted text if provided
        pre = (
            obj.get('strip_text')
            or (obj.get('strip') or {}).get('text')
            or (obj.get('strip') or {}).get('analysis_text')
            or (obj.get('strip') or {}).get('analysis')
        )
        if isinstance(pre, str) and pre.strip():
            return pre.strip()

        # Otherwise flatten any values into a readable single-line string
        values = (obj.get('strip') or {}).get('values')
        if isinstance(values, dict) and values:
            parts: List[str] = []
            for key, val in values.items():
                try:
                    parts.append(f"{str(key)}: {str(val)}")
                except Exception:
                    continue
            if parts:
                return "Strip test results — " + "; ".join(parts)
        return ""
    except Exception:
        return ""

# Setup
load_dotenv()
app = FastAPI(title="Water Judge", description="AI-powered water quality analysis")
logger = logging.getLogger(__name__)

# Initialize wallet
mnemonic = os.environ.get("MNEMONIC")
if not mnemonic:
    raise ValueError("MNEMONIC environment variable required")
Account.enable_unaudited_hdwallet_features()
account = Account.from_mnemonic(mnemonic)

# Reuse singletons to avoid re-initialization overhead on each request


@contextmanager
def suppress_logs_and_output():
    """
    No-op: allow normal logging and propagation.
    """
    yield


@contextmanager
def suppress_stdout_stderr():
    """
    No-op: keep stdout and stderr visible.
    """
    yield


_FINALIZE_CACHE = {}
_FINALIZE_ORDER = []

def finalize_report(combined: Dict[str, Any], use_case: str) -> Dict[str, Any]:
    """
    Use Cerebras to synthesize concise final JSON from combined analysis + user use-case.
    Returns a Python dict with the exact keys required by the UI.
    """
    combined_json = json.dumps(combined, ensure_ascii=False)

    # Create focused input for Cerebras
    input_parts = []
    input_parts.append(f"Water analysis data: {combined_json}")
    input_parts.append(f"Intended use case: {use_case}")

    # Extract location hint if available
    location_hint = ""
    if isinstance(combined, dict) and combined.get('location', {}).get('hint'):
        location_hint = combined['location']['hint']
        input_parts.append(f"Location context: {location_hint}")

    combined_input = ". ".join(input_parts)

    # Use Cerebras for finalization
    result = analyze_water(combined_input, use_case)

    # Transform Cerebras result to the expected format
    final_result = {
        'water_health_percent': f"{result.get('health_percentage', 50)}%",
        'current_water_use_cases': result.get('current_safety_analysis', 'Use with caution; treat before sensitive uses.'),
        'potential_dangers': result.get('risk_analysis', 'Possible microbial or chemical contaminants.'),
        'purify_for_selected_use': result.get('purification_instructions', 'Filter and disinfect before your selected use.'),
    }

    # Simple LRU cache
    cache_key = hashlib.sha256((combined_json + "\n" + (use_case or '')).encode('utf-8')).hexdigest()
    cached = _FINALIZE_CACHE.get(cache_key)
    if cached is not None:
        return cached

    # Update cache
    _FINALIZE_CACHE[cache_key] = final_result
    _FINALIZE_ORDER.append(cache_key)
    if len(_FINALIZE_ORDER) > 32:
        old = _FINALIZE_ORDER.pop(0)
        _FINALIZE_CACHE.pop(old, None)

    return final_result


def generate_detailed_plan(final_result: Dict[str, Any], analysis: Dict[str, Any] | None = None) -> List[Dict[str, str]]:
    """
    Generate a concise purification plan with 3-5 practical steps
    """
    # Build context for Cerebras
    ctx = {
        'final': final_result or {},
        'waterbody': (analysis or {}).get('waterbody') if isinstance(analysis, dict) else None,
        'location': (analysis or {}).get('location') if isinstance(analysis, dict) else None,
    }
    ctx_json = json.dumps(ctx, ensure_ascii=False)

    # Create focused input for concise plan
    input_parts = []
    input_parts.append(f"Context: {ctx_json}")
    input_parts.append("Generate 2-3 practical purification steps.")
    input_parts.append("Each step should have a clear title and brief description.")
    input_parts.append("Focus on effective, realistic methods.")

    combined_input = ". ".join(input_parts)

    # Use Cerebras to generate concise plan
    result = analyze_water(combined_input, final_result.get('selected_use', 'drinking'))

    # Parse the purification instructions into steps
    instructions = result.get('purification_instructions', '')

    # Simple parsing - split by numbered steps or common delimiters
    steps = []
    if instructions:
        # Try to split by step indicators
        import re
        step_pattern = r'(?:Step\s*\d+|^\d+\.|\n\s*\d+\.|\n\s*[-*]\s*)'
        parts = re.split(step_pattern, instructions)

        for i, part in enumerate(parts):
            if part.strip() and len(part.strip()) > 10:  # Only add meaningful steps
                title = f"Step {i+1}"
                description = part.strip()
                steps.append({'title': title, 'description': description})

    # Fallback if parsing fails
    if not steps or len(steps) < 2:
        steps = [
            {'title': 'Filter water', 'description': 'Use clean cloth or filter to remove visible particles.'},
            {'title': 'Disinfect', 'description': 'Boil for 1 minute or use purification tablets.'},
            {'title': 'Safe storage', 'description': 'Store in clean containers, avoid recontamination.'},
        ]

    return steps[:3]  # Limit to 3 steps max


def analyze_water(input_data: str, use_case: str = "drinking") -> dict:
    """
    Generate concise, actionable water analysis focused on the 4 required output fields
    """
    client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

    # Create focused, concise prompt for the 4 required fields
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

        # Extract JSON from response
        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return result
        else:
            return create_concise_fallback(input_data, use_case)

    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return create_concise_fallback(input_data, use_case, error=str(e))

def create_concise_fallback(input_data: str, use_case: str, error: str = None) -> dict:
    """Create concise fallback response when AI analysis fails"""
    return {
        "health_percentage": 50,
        "current_safety_analysis": f"Unable to fully assess safety for {use_case} use. Exercise caution and consider professional testing. Basic filtration and disinfection recommended.",
        "risk_analysis": "Potential risks include microbial contamination and chemical impurities. Professional water testing advised for accurate risk assessment.",
        "purification_instructions": "Filter through clean cloth, boil for 1 minute, or use purification tablets. Store in clean containers and avoid recontamination."
    }

def sign_decision(decision_text: str) -> str:
    """Sign water quality decision with wallet"""
    message = encode_defunct(text=decision_text)
    signed = account.sign_message(message)
    return signed.signature.hex()

# API Endpoints
@app.get("/")
async def root():
    """Service information"""
    return {
        "service": "Water Judge API",
        "version": "2.0-simplified", 
        "judge_address": account.address,
        "description": "AI-powered comprehensive water quality analysis with detailed explanations"
    }

@app.post("/judge")
async def judge_endpoint(data: dict):
    """
    Judge endpoint for water analysis.
    Receives structured JSON data and returns final water quality summary.
    """
    try:
        # The input data is already the combined analysis data
        combined = data
        use_case = data.get("use_case", "drinking")
        
        # Use finalize_report to get the final summary
        final_result = finalize_report(combined, use_case)
        
        # Generate detailed purification plan
        plan = generate_detailed_plan(final_result, combined)
        
        # Sign the decision
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
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Validate environment
    required_vars = ["MNEMONIC", "CEREBRAS_API_KEY"]
    for var in required_vars:
        if not os.environ.get(var):
            logger.error(f"{var} environment variable is required!")
            exit(1)
    
    # Configuration
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    logger.info(f"🚰 Water Judge API starting on {host}:{port}")
    logger.info(f"⚡ Judge Address: {account.address}")
    logger.info("📝 Endpoints: GET / | POST /judge")
    
    # Start server
    uvicorn.run(app, host=host, port=port, log_level="info")