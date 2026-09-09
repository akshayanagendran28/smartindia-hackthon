import math
import json
from typing import Dict, Any, List, Optional
from app.models.partner import ChannelPartner

class GeospatialPartnerService:
    """
    Geospatial partner recommendation combining:
      1. Scheme compatibility (Does the partner handle the user's recommended scheme?)
      2. Geographic proximity (Haversine / spatial distance)
    """

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6371.0 # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return round(R * c, 2)

    @classmethod
    def evaluate_partner(
        cls, 
        partner: ChannelPartner, 
        user_lat: float, 
        user_lon: float, 
        target_scheme_code: Optional[str] = None
    ) -> Dict[str, Any]:
        dist_km = cls.haversine_distance(user_lat, user_lon, partner.latitude, partner.longitude)
        
        try:
            supported = json.loads(partner.supported_scheme_codes)
        except Exception:
            supported = []

        supported_lower = [s.lower() for s in supported]
        
        # Scheme compatibility calculation
        if target_scheme_code:
            target_lower = target_scheme_code.lower()
            if "all" in supported_lower or target_lower in supported_lower or any(target_lower in s for s in supported_lower):
                scheme_compat = 100.0
                reason_part = f"This partner is an authorized processing nodal centre for {target_scheme_code}."
            else:
                scheme_compat = 35.0
                reason_part = f"Partner offers general banking services; scheme {target_scheme_code} may require lead agency escalation."
        else:
            scheme_compat = 85.0
            reason_part = f"Authorized institutional partner supporting multiple MSME and education credit schemes."

        # Geographic proximity score (decay curve: 100 at 0km, 80 at 10km, 50 at 30km, 20 at 100km)
        proximity_score = max(10.0, 100.0 / (1.0 + (dist_km / 12.0) ** 1.3))

        # Combined suitability: Scheme compatibility (60%) + Proximity (40%)
        suitability_score = round((scheme_compat * 0.60) + (proximity_score * 0.40), 1)

        return {
            "id": partner.id,
            "name": partner.name,
            "partner_type": partner.partner_type,
            "address": partner.address,
            "state": partner.state,
            "district": partner.district,
            "pincode": partner.pincode,
            "latitude": partner.latitude,
            "longitude": partner.longitude,
            "contact_person": partner.contact_person,
            "contact_phone": partner.contact_phone,
            "contact_email": partner.contact_email,
            "website": partner.website,
            "verification_status": partner.verification_status,
            "supported_scheme_codes": supported,
            "distance_km": dist_km,
            "scheme_compatibility_score": round(scheme_compat, 1),
            "partner_suitability_score": suitability_score,
            "suitability_reason": f"{reason_part} Located {dist_km:.1f} km away from your search pin."
        }
