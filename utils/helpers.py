"""
Agronomic Helpers and Advisory Logic for AGRI-MITRA
Provides basic fertilizer recommendations per crop and explanatory rationales
for fertilizer model outputs.
"""

from typing import Dict, Any

# Standard agronomic baseline fertilizer guidelines for crops
CROP_BASIC_FERTILIZER_MAP: Dict[str, str] = {
    'rice': "NPK 120:60:60 kg/ha with basal Urea/DAP and top-dressing of Urea at tillering and panicle initiation.",
    'maize': "NPK 120:60:40 kg/ha plus 25 kg/ha Zinc Sulfate; split Nitrogen at knee-high and tasseling stages.",
    'chickpea': "NPK 20:50:20 kg/ha basal dose with Rhizobium seed inoculation for biological nitrogen fixation.",
    'kidneybeans': "NPK 40:60:30 kg/ha; requires balanced phosphorus for healthy nodulation and pod filling.",
    'pigeonpeas': "NPK 25:50:25 kg/ha; apply DAP at sowing and spray 2% Urea at flowering to prevent pod drop.",
    'mothbeans': "NPK 15:40:10 kg/ha; low nitrogen requirement; thrives with light single superphosphate (SSP).",
    'mungbean': "NPK 20:40:20 kg/ha; apply sulfur 20 kg/ha to enhance grain protein and resistance.",
    'blackgram': "NPK 25:50:25 kg/ha; use biofertilizers (Phosphobacteria) alongside moderate DAP application.",
    'lentil': "NPK 20:40:20 kg/ha; emphasize phosphorus for root vigor and Rhizobium nodule count.",
    'pomegranate': "FYM 25 kg/tree plus NPK 250:125:125 g/plant in divided doses; micronutrient zinc and boron spray.",
    'banana': "NPK 200:60:300 g/plant; high Potassium feeder; split into 4-5 applications throughout vegetative phase.",
    'mango': "FYM 50 kg/tree plus NPK 500:250:500 g/tree/year; apply during post-harvest rest period.",
    'grapes': "NPK 500:500:1000 kg/ha; high Potassium required for sugar accumulation, berry size, and skin firmness.",
    'watermelon': "NPK 100:50:50 kg/ha; split nitrogen into basal and vine growth stages; apply soluble potash near fruit set.",
    'muskmelon': "NPK 80:50:50 kg/ha; balanced NPK with foliar potassium nitrate sprays during fruit maturation.",
    'apple': "NPK 700:350:700 g/mature tree; zinc and boron sprays at pre-pink and petal fall stages.",
    'orange': "NPK 600:200:300 g/plant/year; apply in 3 splits along with zinc sulfate and magnesium foliar feeds.",
    'papaya': "NPK 250:250:500 g/plant; apply bimonthly; heavy potassium feeder for continuous fruiting.",
    'coconut': "NPK 500:320:1200 g/palm/year; split in pre-monsoon and post-monsoon doses with magnesium sulfate.",
    'cotton': "NPK 120:60:60 kg/ha; split Nitrogen at square formation and peak boll development stages.",
    'jute': "NPK 60:30:30 kg/ha; top dress Urea in two equal splits at 3 and 5 weeks after sowing.",
    'coffee': "NPK 120:90:120 kg/ha; split into pre-blossom, post-blossom, and post-monsoon applications.",
}

# Explanations for dedicated Fertilizer Recommendation Model outputs
FERTILIZER_EXPLANATIONS: Dict[str, Dict[str, str]] = {
    'Urea': {
        'nutrient_profile': "46% Nitrogen (46-0-0)",
        'primary_use': "Rapid vegetative foliage growth and leaf chlorophyll synthesis.",
        'why': "Your soil test shows a high nitrogen deficit relative to target crop demands. Urea provides immediate water-soluble ammoniacal/amide nitrogen to accelerate leaf area index and stem vigor.",
        'application_tips': "Apply in splits (basal and top-dressing) to prevent leaching. Avoid broadcasting on wet soil surfaces without soil incorporation."
    },
    'DAP': {
        'nutrient_profile': "18% Nitrogen, 46% Phosphorus (18-46-0)",
        'primary_use': "Early root establishment, seedling vigor, and strong tillering.",
        'why': "The diagnostic indicates high phosphorus demand with moderate initial nitrogen need. DAP (Diammonium Phosphate) provides soluble phosphate that promotes vigorous root proliferation during early vegetative stages.",
        'application_tips': "Place fertilizer 5 cm below and beside the seed line during sowing. Do not broadcast directly on seed to prevent osmotic shock."
    },
    '14-35-14': {
        'nutrient_profile': "14% Nitrogen, 35% Phosphorus, 14% Potassium",
        'primary_use': "Phosphate-rich balanced compound fertilizer for robust root and crown establishment.",
        'why': "Recommended for soils needing substantial phosphorus supplementation while maintaining a steady baseline of nitrogen and potash for balanced cellular development.",
        'application_tips': "Ideal as a basal application before harrowing or at transplanting."
    },
    '28-28': {
        'nutrient_profile': "28% Nitrogen, 28% Phosphorus, 0% Potassium (28-28-0)",
        'primary_use': "High nitrogen and phosphorus dual-action fertilizer.",
        'why': "Selected because your soil potassium levels are adequate, but both nitrogen (for canopy development) and phosphorus (for energy transfer and rooting) require significant simultaneous replenishment.",
        'application_tips': "Best applied during early active growth phases. Ensure adequate soil moisture."
    },
    '17-17-17': {
        'nutrient_profile': "17% Nitrogen, 17% Phosphorus, 17% Potassium (Equal Ratio NPK)",
        'primary_use': "Complete all-round balanced fertilization for mixed and maintenance feeding.",
        'why': "Your soil analysis indicates uniform nutrient consumption across all three macro-elements. Complex 17-17-17 ensures harmonious plant nutrition without risking nutrient antagonism.",
        'application_tips': "Suitable for basal application or split broadcast prior to inter-cultivation."
    },
    '20-20': {
        'nutrient_profile': "20% Nitrogen, 20% Phosphorus, 0% or low Potassium (Ammonium Phosphate Sulfate)",
        'primary_use': "Balanced vegetative starter fertilizer with sulfur benefits.",
        'why': "Recommended for early-stage crops where nitrogen and phosphorus are needed in equal moderate concentrations to promote strong stalks and healthy early branching.",
        'application_tips': "Incorporate into top 5-10 cm of root zone during seedbed preparation."
    },
    '10/26/2026': {
        'nutrient_profile': "10% Nitrogen, 26% Phosphorus, 26% Potassium (High PK Complex 10-26-26)",
        'primary_use': "High Phosphorus & Potassium booster for root strength, flowering, and drought resistance.",
        'why': "Recommended when soil has adequate nitrogen or nitrogen-fixing capacity, but requires strong potassium and phosphorus for disease resilience, fruit filling, and osmotic water regulation.",
        'application_tips': "Apply during sowing/planting and at pre-flowering stages. Water well after application."
    },
    '10-26-26': {
        'nutrient_profile': "10% Nitrogen, 26% Phosphorus, 26% Potassium (High PK Complex)",
        'primary_use': "High Phosphorus & Potassium booster for root strength and flowering.",
        'why': "Selected to replenish critical phosphorus and potassium reservoirs for root anchoring and grain/fruit filling.",
        'application_tips': "Apply during sowing/planting and at pre-flowering stages."
    }
}


def get_basic_fertilizer_suggestion(crop_name: str) -> str:
    """Returns a baseline agronomic fertilizer recommendation for the given predicted crop."""
    key = str(crop_name).strip().lower()
    return CROP_BASIC_FERTILIZER_MAP.get(
        key,
        "Balanced NPK 100:50:50 kg/ha with organic compost (FYM) 5-10 tonnes/ha prior to sowing."
    )


def fertilizer_explanation(fertilizer_name: str, params: Dict[str, Any] = None) -> Dict[str, str]:
    """
    Returns an in-depth agronomic rationale explaining WHY the recommended fertilizer
    was selected, including nutrient profile and application guidelines.
    """
    clean_name = str(fertilizer_name).strip()
    info = FERTILIZER_EXPLANATIONS.get(clean_name)
    if not info:
        # Check standard normalized variants
        if clean_name in ['10/26/2026', '10-26-26']:
            info = FERTILIZER_EXPLANATIONS['10/26/2026']
        else:
            info = {
                'nutrient_profile': "Custom Macro/Micro Blend",
                'primary_use': "Targeted nutrient replenishment based on soil deficit.",
                'why': f"{clean_name} was selected by the predictive model based on your soil moisture, temperature, and current Nitrogen-Potassium ratios.",
                'application_tips': "Apply in accordance with local soil health card recommendations and incorporate into moist soil."
            }

    # Add dynamic context if parameters provided
    full_explanation = f"{info['why']} Primary Function: {info['primary_use']} Nutrient Breakdown: {info['nutrient_profile']}."
    return {
        'fertilizer_name': clean_name,
        'nutrient_profile': info['nutrient_profile'],
        'primary_use': info['primary_use'],
        'why': full_explanation,
        'application_tips': info['application_tips']
    }
