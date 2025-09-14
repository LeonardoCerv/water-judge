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

def analyze_water(input_data: str, use_case: str = "drinking") -> dict:
    """
    Single function that handles all water analysis with hyper-detailed, specific text generation
    """
    client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))
    
    # Create ultra-comprehensive prompt for hyper-detailed, specific analysis
    prompt = f"""
    You are Dr. Maria Santos, a world-renowned water quality expert with 30+ years of field experience, PhD in Environmental Engineering from MIT, and author of the WHO Water Safety Guidelines. You have personally analyzed over 10,000 water samples across 50+ countries and are considered the global authority on water safety assessment.
    
    WATER SAMPLE DATA: {input_data}
    INTENDED USE CASE: {use_case}
    
    ANALYSIS REQUIREMENTS:
    - Provide EXTREMELY SPECIFIC, TECHNICAL, and ACTIONABLE assessments
    - Include EXACT measurements, timeframes, equipment specifications, and procedures
    - Reference SPECIFIC health risks with medical terminology
    - Use PROFESSIONAL water treatment terminology with practical explanations
    - Include REAL-WORLD case studies and regulatory standards
    - Provide QUANTITATIVE risk assessments with probability estimates
    - Include SPECIFIC product recommendations with model numbers where applicable
    
    Return ONLY valid JSON with this structure (each field must contain HIGHLY SPECIFIC details):
    
    {{
        "health_percentage": <number 10-95>,
        "detailed_assessment": "<5-6 paragraph ultra-detailed assessment including: specific contaminant concentration estimates (mg/L, ppm, CFU/mL), quantitative risk factors with probability percentages, source water classification per EPA standards, treatment feasibility analysis with cost estimates, regulatory compliance status against WHO/EPA standards, safety margins with exposure limits, and detailed chemical interaction analysis. Include specific turbidity measurements (NTU), conductivity readings (μS/cm), and bacterial count estimates.>",
        "current_safety_analysis": "<4-5 paragraph ultra-specific analysis for {use_case} use including: immediate health risks with LD50 values where applicable, exposure pathway analysis with absorption rates, dose-response relationships with NOAEL/LOAEL values, vulnerable population considerations (pregnant women, children, immunocompromised), acute vs chronic effects with specific symptom timelines, contraindications with medical conditions, maximum daily intake limits in liters/day, and bioaccumulation factors for heavy metals.>",
        "risk_analysis": "<5-6 paragraph comprehensive risk assessment covering: specific microbial pathogens (E.coli O157:H7, Giardia lamblia, Cryptosporidium parvum) with infectious dose estimates, chemical contaminants (lead >15ppb, arsenic >10ppb, nitrates >10mg/L) with health effect thresholds, physical hazards (turbidity >4NTU, TDS >500mg/L), radiological concerns with becquerel measurements, pesticide residues with ADI values, endocrine disruptors with ng/L detection limits, and cumulative exposure calculations. Include probability estimates (low/moderate/high risk percentages) and population-specific vulnerability assessments.>",
        "purification_instructions": "<Ultra-detailed 10-12 step purification protocol with: exact equipment specifications (filter pore sizes in microns, UV lamp wattage, contact time calculations), precise chemical dosages (chlorine 1-2mg/L, alum 10-30mg/L), temperature requirements (60°C minimum for pasteurization), contact times (CT values for disinfection), flow rates (L/min), quality verification methods (turbidity <1NTU, chlorine residual 0.2-0.5mg/L), troubleshooting procedures for common failures, safety precautions with PPE requirements, performance indicators with acceptance criteria, specific product recommendations (brand names, model numbers), installation diagrams, maintenance schedules, and cost estimates per 1000L treated.>",
        "environmental_context": "<4-5 paragraph analysis including: specific source water classification (surface/groundwater/springs), watershed characteristics with drainage area calculations, seasonal contamination patterns with monthly variation data, upstream pollution sources with distance measurements, geological influences (limestone/granite/clay formations), climate factors (rainfall patterns, temperature effects), regional water quality trends with 5-year data comparisons, specific environmental indicators (dissolved oxygen >5mg/L, pH 6.5-8.5), monitoring station locations with GPS coordinates, and regulatory compliance history.>",
        "scientific_rationale": "<5-6 paragraph explanation including: analytical methodology per Standard Methods 22nd Edition, data interpretation criteria with statistical confidence intervals, uncertainty factors with measurement error ranges, quality assurance protocols (QA/QC procedures), regulatory standards comparison (WHO vs EPA vs local), peer-reviewed research citations (specific journal articles), testing protocol validation (USEPA Method 200.8 for metals), detection limits (MDL/PQL values), interference analysis, calibration procedures, and measurement traceability to NIST standards.>",
        "long_term_considerations": "<4-5 paragraph analysis including: chronic exposure effects with PBPK modeling results, cumulative health impacts over 20+ year exposure periods, treatment system maintenance schedules (monthly/quarterly/annual tasks), monitoring frequencies (daily/weekly/monthly parameters), cost-benefit analysis with NPV calculations over 10 years, sustainability factors including energy consumption (kWh/m³), carbon footprint assessments, upgrade recommendations with technology lifecycle analysis, replacement schedules for components (filters every 6 months, UV lamps annually), and regulatory compliance monitoring requirements.>",
        "emergency_protocols": "<Ultra-detailed emergency response including: specific symptom recognition (gastroenteritis onset 6-72 hours, neurological symptoms, skin reactions), immediate treatment steps with medical protocols, medical consultation criteria (when to call poison control vs emergency room), alternative water source specifications (minimum 4L/person/day), emergency contact information (local health dept, water utility, poison control), documentation requirements for health authorities, recovery protocols with timeline expectations, medical intervention procedures (IV fluid replacement, antibiotic protocols), laboratory testing requirements (stool culture, blood chemistry), and legal notification requirements for waterborne illness outbreaks.>",
        "classification": "<safe_for_drinking|agricultural_only|recreational_only|unsafe|requires_purification>",
        "confidence_score": <0.0-1.0>,
        "use_case": "{use_case}",
        "detailed_parameters": {{
            "ph_analysis": "<Ultra-specific pH assessment including: exact measurement with ±0.1 accuracy, optimal ranges for {use_case} (6.5-8.5 for drinking), corrosion potential calculations, buffering capacity analysis, adjustment methods with lime/acid dosing calculations, health implications of pH extremes, monitoring frequency requirements, and temperature correction factors>",
            "turbidity_analysis": "<Exact turbidity measurement in NTU, filtration requirements for different levels (>4NTU requires coagulation/flocculation), clarity standards for {use_case}, aesthetic considerations, pathogen correlation factors, treatment efficiency indicators, and continuous monitoring protocols>", 
            "chemical_analysis": "<Comprehensive analysis including: heavy metals screening (Pb, Hg, Cd, As) with detection limits, organic compounds identification, pesticide residue analysis, industrial chemical screening, treatment removal efficiencies (>99% for activated carbon), regulatory limit comparisons, and health risk calculations with reference doses>",
            "biological_analysis": "<Detailed microbial assessment including: total coliform counts (CFU/100mL), E.coli enumeration, pathogen screening (Giardia/Crypto oocysts per 10L), virus detection protocols, disinfection CT requirements, chlorine demand testing, biological stability analysis, and regrowth potential assessment>",
            "physical_analysis": "<Complete physical characterization including: color analysis (Hazen units), odor threshold detection, taste panel results, temperature measurements, electrical conductivity (μS/cm), total dissolved solids (mg/L), suspended solids quantification, and aesthetic quality scoring>"
        }}
    }}
    
    CRITICAL REQUIREMENTS:
    - Every field must contain 400+ words with specific technical details
    - Include exact numbers, measurements, and quantitative assessments
    - Reference specific equipment models, chemical names, and regulatory standards
    - Provide step-by-step procedures with precise instructions
    - Include safety margins, quality control measures, and verification methods
    - Use professional terminology but explain technical concepts clearly
    """
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are Dr. Maria Santos, world's leading water quality expert with 30+ years experience. Provide ULTRA-DETAILED, TECHNICAL assessments with specific measurements, exact procedures, and quantitative analysis. Each response field must contain 400+ words with precise technical details, specific equipment recommendations, exact chemical dosages, and comprehensive safety protocols."},
                {"role": "user", "content": prompt}
            ],
            model="qwen-3-235b-a22b-thinking-2507",
            max_completion_tokens=8000,  # Maximum tokens for ultra-detailed responses
            temperature=0.1,  # Lower temperature for more consistent technical accuracy
        )
        
        ai_response = response.choices[0].message.content
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            
            # Ensure ultra-detailed response requirements
            if len(result.get("detailed_assessment", "")) < 800:  # Minimum 800 characters for ultra-detailed
                result = enhance_response(result, input_data, use_case)
            
            return result
        else:
            return create_detailed_fallback(input_data, use_case)
            
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return create_detailed_fallback(input_data, use_case, error=str(e))

def enhance_response(result: dict, input_data: str, use_case: str) -> dict:
    """Enhance responses that don't meet minimum detail requirements"""
    
    # Default detailed assessments based on use case
    detailed_assessments = {
        "drinking": f"Based on the provided water analysis data '{input_data}', this water source requires comprehensive evaluation before consumption. The assessment considers multiple factors including visual clarity, chemical composition, potential microbial contamination, and source reliability. For drinking water purposes, safety standards are extremely strict as waterborne illnesses can cause serious health complications. The evaluation process examines pH levels, turbidity, chemical contaminants, and biological indicators to determine potability. Environmental factors such as source location, seasonal variations, and upstream activities significantly impact water quality and must be considered in the final safety determination.",
        
        "irrigation": f"The water sample analysis for irrigation purposes reveals several important considerations for agricultural use. Irrigation water quality directly impacts soil health, crop yield, and long-term agricultural sustainability. Key factors include salt content, pH levels, and potential chemical contaminants that could accumulate in soil over time. The assessment evaluates the water's suitability for different crop types, as some plants are more sensitive to water quality variations than others. Proper irrigation practices and ongoing monitoring are essential to prevent soil degradation and ensure optimal plant health.",
        
        "human": f"For hygiene and cleaning applications, this water source presents specific considerations related to skin contact and indirect exposure risks. While standards for hygiene water are less stringent than drinking water, certain contaminants can still cause skin irritation, allergic reactions, or other health issues. The assessment examines bacterial content, chemical residues, and physical contaminants that might affect cleaning effectiveness or pose contact risks. Proper treatment and handling procedures can significantly improve safety for personal hygiene use.",
        
        "animals": f"Animal water consumption requirements vary significantly by species, size, and sensitivity levels. This assessment considers the specific needs and tolerances of different animals, as some species are more resilient to water quality variations while others require nearly potable-quality water. Factors such as heavy metals, bacterial contamination, and chemical residues are evaluated for their potential impact on animal health, reproduction, and productivity. Long-term exposure effects and species-specific vulnerabilities are important considerations in the safety determination."
    }
    
    # Enhance the response with detailed content
    result.update({
        "detailed_assessment": detailed_assessments.get(use_case, detailed_assessments["drinking"]),
        "current_safety_analysis": f"For {use_case} use, the current safety profile shows moderate concerns that require attention. The primary considerations include potential contamination risks, treatment requirements, and monitoring protocols. Based on available data, immediate use may present risks that can be mitigated through appropriate treatment methods. The safety assessment considers both acute and chronic exposure scenarios to provide comprehensive guidance.",
        "risk_analysis": f"The comprehensive risk assessment identifies several categories of potential hazards. Microbial risks include bacteria, viruses, and parasites that could cause immediate illness. Chemical risks encompass both natural minerals and artificial contaminants that may accumulate over time. Physical contaminants such as sediment and debris can affect taste, appearance, and equipment function. The likelihood and severity of each risk category varies based on source characteristics and intended use patterns.",
        "purification_instructions": get_detailed_purification_steps(use_case),
        "environmental_context": f"Environmental factors significantly influence water quality and treatment requirements. Source location, seasonal weather patterns, upstream activities, and local geology all contribute to water characteristics. Understanding these environmental influences helps predict quality variations and plan appropriate treatment strategies. Regional water quality trends and local contamination sources provide important context for ongoing monitoring and safety protocols.",
        "scientific_rationale": f"The assessment methodology combines visual inspection, available test data, and established water quality standards to generate safety recommendations. Confidence levels reflect data completeness and measurement reliability. Scientific principles guide the interpretation of chemical indicators, biological markers, and physical characteristics. The analysis follows established protocols while acknowledging limitations in available data and testing capabilities.",
        "long_term_considerations": f"Long-term water use patterns require ongoing monitoring and periodic reassessment. Health effects from chronic exposure may differ significantly from acute risks. System maintenance, source protection, and quality verification protocols help ensure sustained safety over time. Regular testing schedules and treatment system updates are essential components of comprehensive water management strategies.",
        "emergency_protocols": f"In case of suspected water-related illness, immediately discontinue use and seek medical attention. Alternative water sources should be identified and maintained as backup options. Emergency contact information for water quality professionals and health authorities should be readily available. Documentation of symptoms, exposure duration, and treatment methods helps medical professionals provide appropriate care."
    })
    
    return result

def get_detailed_purification_steps(use_case: str) -> str:
    """Generate detailed purification instructions for each use case"""
    steps = {
        "drinking": """Step 1: Initial Assessment - Examine water visually for color, clarity, odor, and visible contaminants. Allow turbid water to settle for 30-60 minutes to separate sediment. Record observations for treatment planning.

Step 2: Pre-filtration - Use clean cloth, coffee filter, or sand/gravel filter to remove visible particles. For cloth filtration, use tightly woven fabric and filter slowly. Replace or clean filter material between uses.

Step 3: Primary Disinfection - Boil water at rolling boil for 1 minute at sea level (3 minutes above 6,500 feet elevation). Alternatively, use water purification tablets following manufacturer instructions exactly. UV sterilization requires clear water and proper exposure time.

Step 4: Chemical Treatment - If chlorine taste is strong, use activated carbon filter or let water sit uncovered for 30 minutes to reduce chlorine levels. Carbon filters must be replaced regularly to maintain effectiveness.

Step 5: Final Storage - Store treated water in clean, covered containers made of food-grade materials. Label with treatment date and use within 24 hours if unrefrigerated. Avoid recontamination during storage and dispensing.""",

        "irrigation": """Step 1: Sediment Management - Allow water to settle in holding tank or pond for 2-4 hours minimum. Remove settled particles using bottom drain or pumping from upper levels. Install coarse mesh screens to prevent large debris entry.

Step 2: pH Testing and Adjustment - Test pH using digital meter or test strips. Most crops prefer pH 6.0-7.5. Add agricultural lime to raise pH or sulfur to lower pH. Mix thoroughly and retest after 30 minutes.

Step 3: Filtration System - Install appropriate filtration based on water quality and crop sensitivity. Sand filters work for particle removal, while activated carbon removes chemicals. Size filter system for flow rate requirements.

Step 4: Application Method - Use drip irrigation or subsurface application when possible to minimize plant contact with untreated water. Avoid overhead watering on leafy vegetables or crops consumed raw.

Step 5: Monitoring Protocol - Test soil pH and nutrient levels monthly. Flush irrigation lines weekly with clean water. Monitor plants for signs of stress or contamination. Keep detailed records of water source and treatment methods.""",

        "human": """Step 1: Basic Filtration - Remove visible particles using cloth filter or settling process. This improves appearance and reduces skin irritation potential. Use multiple filter layers for heavily contaminated water.

Step 2: Temperature Preparation - Heat water to appropriate temperature for intended use. Hot water (120-140°F) improves cleaning effectiveness and kills some pathogens. Cool to comfortable temperature before use.

Step 3: Light Disinfection - For bathing water, add 1-2 drops of unscented chlorine bleach per quart of water. Mix thoroughly and let stand 30 minutes before use. Not necessary for laundry or general cleaning.

Step 4: Safe Usage Practices - Avoid splashing water in eyes, nose, or mouth during use. Use clean containers and utensils for water handling. Limit storage time to prevent bacterial growth in treated water.

Step 5: Waste Management - Dispose of used water appropriately to prevent contamination of clean water sources. Do not allow runoff into food preparation areas or drinking water supplies.""",

        "animals": """Step 1: Debris Removal - Filter out visible particles, debris, and contaminants that could harm animals. Use mesh straining or settling process appropriate for water volume requirements.

Step 2: Basic Treatment - Consider mild chlorination for livestock (consult veterinarian for species-specific dosage). Some animals are more sensitive to chemicals than others. Test small amounts first.

Step 3: Container Preparation - Clean all water troughs and containers thoroughly with appropriate disinfectants. Rinse completely to remove cleaning residues that could harm animals.

Step 4: Distribution Setup - Provide water in clean, elevated containers when possible. Ensure easy access but prevent contamination from animal waste. Install drainage to prevent standing water around containers.

Step 5: Health Monitoring - Watch animals closely for signs of illness, reluctance to drink, or changes in behavior. Maintain alternative clean water source as backup. Document any health issues for veterinary consultation."""
    }
    
    return steps.get(use_case, steps["drinking"])

def create_detailed_fallback(input_data: str, use_case: str, error: str = None) -> dict:
    """Create detailed fallback response when AI analysis fails"""
    return {
        "health_percentage": 45,
        "detailed_assessment": f"Limited analysis available for the provided water data: '{input_data}'. Due to processing constraints, this assessment relies on basic safety protocols and conservative estimates. For {use_case} use, professional water testing is strongly recommended to obtain accurate safety determinations. The evaluation considers general water safety principles and common contamination patterns, but cannot provide specific risk assessments without comprehensive laboratory analysis.",
        "current_safety_analysis": f"Current safety for {use_case} use cannot be fully determined without additional testing data. Conservative safety measures are recommended until proper analysis is completed. Basic treatment methods should be applied as precautionary measures, with professional consultation sought for definitive safety guidance.",
        "risk_analysis": "Risk assessment is limited due to insufficient data. Potential hazards include microbial contamination, chemical contaminants, and physical impurities. The severity and likelihood of these risks cannot be accurately determined without proper testing. Conservative treatment approaches are recommended to minimize potential exposure.",
        "purification_instructions": get_detailed_purification_steps(use_case),
        "environmental_context": "Environmental factors affecting water quality cannot be fully assessed with available information. Source characteristics, seasonal variations, and local contamination sources should be investigated to improve safety determinations. Local water quality reports and professional consultation can provide valuable additional context.",
        "scientific_rationale": f"Assessment methodology is limited by available data constraints. {f'Processing error encountered: {error}. ' if error else ''}Standard safety protocols are applied as precautionary measures. Confidence levels are reduced due to insufficient information for comprehensive analysis. Professional water testing is strongly recommended for accurate safety assessment.",
        "long_term_considerations": "Long-term safety cannot be determined without ongoing monitoring and periodic testing. Regular water quality assessments are essential for sustained safe use. Treatment systems require maintenance and periodic updates to ensure continued effectiveness. Professional consultation is recommended for long-term water management planning.",
        "emergency_protocols": "If any adverse health effects occur after water use, discontinue immediately and seek medical attention. Alternative water sources should be identified and prepared for emergency use. Contact local health authorities if multiple people experience similar symptoms. Keep detailed records of water sources and treatment methods for medical reference.",
        "classification": "requires_purification",
        "confidence_score": 0.3,
        "use_case": use_case,
        "detailed_parameters": {
            "ph_analysis": "pH level unknown - testing required for accurate assessment",
            "turbidity_analysis": "Turbidity level unknown - visual inspection and testing recommended",
            "chemical_analysis": "Chemical composition unknown - laboratory testing required",
            "biological_analysis": "Microbial content unknown - biological testing essential for safety",
            "physical_analysis": "Physical characteristics require professional evaluation"
        },
        "processing_limitation": True
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

@app.post("/analyze")
async def analyze_water_endpoint(data: dict):
    """
    Main endpoint for comprehensive water analysis
    Accepts any water data and returns detailed assessment
    """
    try:
        # Extract all available data
        scene_description = data.get("scene_description", "")
        input_text = data.get("input_text", "")
        strip_values = data.get("strip_values", {})
        waterbody = data.get("waterbody", {})
        location = data.get("location", {})
        use_case = data.get("use_case", "drinking")
        
        # Combine all data into comprehensive input
        input_parts = []
        
        if scene_description:
            input_parts.append(f"Scene: {scene_description}")
        if input_text:
            input_parts.append(f"Measurements: {input_text}")
        if strip_values:
            strip_data = ", ".join([f"{k}:{v}" for k, v in strip_values.items() if v])
            input_parts.append(f"Test strips: {strip_data}")
        if waterbody:
            body_data = ", ".join([f"{k}:{v}" for k, v in waterbody.items() if v])
            input_parts.append(f"Visual assessment: {body_data}")
        if location:
            loc_data = ", ".join([f"{k}:{v}" for k, v in location.items() if v])
            input_parts.append(f"Location: {loc_data}")
        
        combined_input = ". ".join(input_parts) if input_parts else "General water quality assessment requested"
        
        # Run comprehensive analysis
        result = analyze_water(combined_input, use_case)
        
        # Transform to Django-compatible format
        django_format = {
            "water_health_percent": f"{result['health_percentage']}%",
            "current_water_use_cases": result["current_safety_analysis"],
            "potential_dangers": result["risk_analysis"],
            "purify_for_selected_use": result["purification_instructions"],
            "selected_use": use_case,
            "purify_title": f"Purify for {use_case.title()} Use",
            "detailed_assessment": result["detailed_assessment"],
            "environmental_context": result["environmental_context"],
            "scientific_rationale": result["scientific_rationale"],
            "long_term_considerations": result["long_term_considerations"],
            "emergency_protocols": result["emergency_protocols"],
            "detailed_parameters": result["detailed_parameters"],
            "confidence": result["confidence_score"],
            "classification": result["classification"]
        }
        
        # Sign the decision
        signature = sign_decision(json.dumps(result, ensure_ascii=False))
        
        return {
            "judge_address": account.address,
            "result": django_format,
            "signature": signature,
            "comprehensive_analysis": result,
            "input_processed": combined_input
        }
        
    except Exception as e:
        logger.error(f"Analysis endpoint error: {str(e)}")
        
        fallback = create_detailed_fallback(
            str(data), 
            data.get("use_case", "drinking"), 
            str(e)
        )
        
        return {
            "judge_address": account.address,
            "result": {
                "water_health_percent": f"{fallback['health_percentage']}%",
                "current_water_use_cases": fallback["current_safety_analysis"],
                "potential_dangers": fallback["risk_analysis"],
                "purify_for_selected_use": fallback["purification_instructions"],
                "error": str(e)
            },
            "error": str(e)
        }

# Legacy endpoint compatibility
@app.post("/judge")
async def judge_legacy(data: dict):
    """Legacy endpoint - redirects to main analyze endpoint"""
    return await analyze_water_endpoint(data)

@app.post("/finalize")
async def finalize_legacy(data: dict):
    """Legacy endpoint - redirects to main analyze endpoint"""
    return await analyze_water_endpoint(data)

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
    logger.info("📝 Endpoints: GET / | POST /analyze")
    
    # Start server
    uvicorn.run(app, host=host, port=port, log_level="info")