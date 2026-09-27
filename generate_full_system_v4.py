# -*- coding: utf-8 -*-
"""
Full System Multilingual Generator V4
Generates frontend/src/context/LanguageContext.jsx and verifies frontend components.
"""
import json
import os
import sys

# Import base scheme definitions
from build_all_schemes_and_locales import SCHEMES_12_LANG

# Define aliases for all schemes
SCHEME_ALIASES = {
    "PMEGP": ["PMEGP", "PMEGP (Prime Minister Employment Generation Programme)", "Prime Minister's Employment Generation Programme (PMEGP)"],
    "MUDRA_SHISHU": ["MUDRA_SHISHU", "MUDRA-SHISHU", "MUDRASHISHU", "MUDRA SHISHU", "Pradhan Mantri MUDRA Yojana - Shishu", "Pradhan Mantri Mudra Yojana — Shishu (PMMY)", "Pradhan Mantri Mudra Yojana – Shishu (PMMY)"],
    "MUDRA_KISHORE": ["MUDRA_KISHORE", "MUDRA-KISHORE", "MUDRAKISHORE", "MUDRA KISHORE", "Pradhan Mantri MUDRA Yojana - Kishore", "Pradhan Mantri Mudra Yojana — Kishore (PMMY)", "Pradhan Mantri Mudra Yojana – Kishore (PMMY)"],
    "STANDUP_INDIA": ["STANDUP_INDIA", "STANDUP-IND", "STAND_UP_INDIA", "STANDUPIND", "STANDUP INDIA", "Stand-Up India Scheme for SC/ST and Women Entrepreneurs", "Stand-Up India Scheme (SC/ST & Women)"],
    "PM_SVANIDHI": ["PM_SVANIDHI", "SVANIDHI", "PM-SVANIDHI", "PMSVANIDHI", "PM SVANIDHI", "PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi)", "PM Street Vendor's AtmaNirbhar Nidhi", "PM SVANidhi (Street Vendors)"],
    "PM_VISHWAKARMA": ["PM_VISHWAKARMA", "VISHWAKARMA", "PM-VISHWAKARMA", "PMVISHWAKARMA", "PM VISHWAKARMA", "PM Vishwakarma Scheme", "PM Vishwakarma Scheme for Traditional Artisans", "PM Vishwakarma Scheme (Artisans & Craftsmen)"],
    "MAHILA_SAMRIDHI": ["MAHILA_SAMRIDHI", "MAHILA-SAMRIDHI", "MAHILASAMRIDHI", "MAHILA SAMRIDHI", "Mahila Samridhi Yojana", "Mahila Samridhi Yojana (NBCFDC)"],
    "NMDFC_TERM": ["NMDFC_TERM", "NMDFC-TERM", "NMDFC_TERM_LOAN", "NMDFCTERM", "NMDFC Term Loan Scheme for Minorities"],
    "ASIIM": ["ASIIM", "ASIIM_STUDENT", "ASIIMSTUDENT", "Ambedkar Social Innovation and Incubation Mission (ASIIM)", "Ambedkar Social Innovation & Incubation Mission (ASIIM)"],
    "COIR_UDYAMI": ["COIR_UDYAMI", "COIR-UDYAMI", "COIRUDYAMI", "Coir Udyami Yojana (MoMSME)", "Coir Udyami Yojana"],
    "NSSH_SCST": ["NSSH_SCST", "NSSH-SCST", "NSSHSCST", "National SC-ST Hub (NSSH) Support Scheme", "National SC-ST Hub Support Scheme"],
    "TN_NEEDS": ["TN_NEEDS", "TN-NEEDS", "TNNEEDS", "New Entrepreneur-cum-Enterprise Development Scheme (NEEDS) — Tamil Nadu", "New Entrepreneur-cum-Enterprise Development Scheme (NEEDS) – Tamil Nadu", "New Entrepreneur-cum-Enterprise Development Scheme (NEEDS)"],
    "KA_UDYOGINI": ["KA_UDYOGINI", "KA-UDYOGINI", "KAUDYOGINI", "Udyogini Scheme for Women Entrepreneurs — Karnataka", "Udyogini Scheme for Women Entrepreneurs – Karnataka", "Udyogini Scheme for Women Entrepreneurs"],
    "MH_CMEGP": ["MH_CMEGP", "MH-CMEGP", "MHCMEGP", "Chief Minister Employment Generation Programme (CMEGP) — Maharashtra", "Chief Minister Employment Generation Programme (CMEGP) – Maharashtra", "Chief Minister Employment Generation Programme (CMEGP)"],
    "KL_ESS": ["KL_ESS", "KL-ESS", "KLESS", "Entrepreneur Support Scheme (ESS) — Kerala", "Entrepreneur Support Scheme (ESS) – Kerala", "Entrepreneur Support Scheme (ESS)"],
    "UP_MMYSY": ["UP_MMYSY", "UP-MMYSY", "UPMMYSY", "Mukhyamantri Yuva Swarojgar Yojana (MMYSY) — Uttar Pradesh", "Mukhyamantri Yuva Swarojgar Yojana (MMYSY) – Uttar Pradesh", "Mukhyamantri Yuva Swarojgar Yojana (MMYSY)"],
    "WB_KARMA_SATHI": ["WB_KARMA_SATHI", "WB-KARMA-SATHI", "WBKARMASATHI", "Karma Sathi Prakalpa — West Bengal", "Karma Sathi Prakalpa – West Bengal", "Karma Sathi Prakalpa"],
    "CSIS": ["CSIS", "Central Sector Interest Subsidy (CSIS) on Higher Education Loans", "Central Sector Interest Subsidy Scheme (CSIS)"],
    "NSFDC_EDU": ["NSFDC_EDU", "NSFDC-EDU", "NSFDCEDU", "NSFDC Education Loan Scheme for Scheduled Caste Students"],
    "NBCFDC_EDU": ["NBCFDC_EDU", "NBCFDC-EDU", "NBCFDCEDU", "NBCFDC Education Loan Scheme for OBC Students"],
    "NMDFC_EDU": ["NMDFC_EDU", "NMDFC-EDU", "NMDFCEDU", "NMDFC Maulana Azad Education Loan Scheme for Minorities", "Maulana Azad Education Loan Scheme for Minorities"],
    "AMBEDKAR_EDU": ["AMBEDKAR_EDU", "AMBEDKAR-EDU", "AMBEDKAREDU", "Dr. Ambedkar Central Sector Scheme of Interest Subsidy on Overseas Studies"],
    "CGFSEL": ["CGFSEL", "Credit Guarantee Fund Scheme for Education Loans (CGFSEL / IBA)", "Credit Guarantee Fund Scheme for Education Loans"]
}

# Build Master SCHEME_MAP
master_scheme_map = {}
for base_key, lang_dict in SCHEMES_12_LANG.items():
    aliases = SCHEME_ALIASES.get(base_key, [base_key])
    for alias in aliases:
        master_scheme_map[alias] = lang_dict
        # Normalized key without hyphens or underscores
        norm = alias.upper().replace("-", "").replace("_", "").replace(" ", "")
        master_scheme_map[norm] = lang_dict

print(f"Master SCHEME_MAP compiled with {len(master_scheme_map)} lookup keys.")

# Save JSON representation to inspect
with open("master_scheme_map.json", "w", encoding="utf-8") as f:
    json.dump(master_scheme_map, f, ensure_ascii=False, indent=2)
