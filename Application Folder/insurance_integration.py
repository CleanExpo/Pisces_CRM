import os
import requests
from typing import Dict, Any, Optional, List

class InsuranceIntegration:
    def __init__(self):
        self.crm_api_key = os.environ.get('INSURANCE_API_KEY')  # This is actually the CRM API key
        self.crm_api_url = os.environ.get('INSURANCE_API_URL', 'https://api.crm-company.com/v1')

    def prepare_claim_data(self, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare the claim data in a format that can be easily adapted for future insurance company integration.
        
        :param claim_data: Dictionary containing the claim information
        :return: Dictionary containing the formatted claim data
        """
        # This is a placeholder implementation. Adjust based on your specific requirements.
        formatted_claim = {
            'inspection_id': claim_data.get('inspection_id'),
            'location': claim_data.get('location'),
            'date': claim_data.get('date'),
            'damage_description': claim_data.get('damage_description'),
            'estimated_cost': claim_data.get('estimated_cost'),
            'photos': claim_data.get('photos', []),
            'ssra': claim_data.get('ssra', [])
        }
        return formatted_claim

    def store_claim_in_crm(self, claim_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Store the claim data in the company's CRM system.
        
        :param claim_data: Dictionary containing the formatted claim information
        :return: Dictionary containing the response from the CRM system, or None if the request failed
        """
        headers = {
            'Authorization': f'Bearer {self.crm_api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(f'{self.crm_api_url}/claims', json=claim_data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error storing claim in CRM: {e}")
            return None

def format_inspection_for_claim(inspection) -> Dict[str, Any]:
    """
    Format the inspection data for future submission to the insurance company.
    
    :param inspection: Inspection object from the database
    :return: Dictionary containing formatted claim data
    """
    claim_data = {
        'inspection_id': inspection.id,
        'location': inspection.location,
        'date': inspection.timestamp.isoformat(),
        'damage_description': inspection.description,
        'estimated_cost': calculate_estimated_cost(inspection),
        'photos': get_photo_urls(inspection),
        'ssra': format_ssra(inspection),
    }
    return claim_data

def calculate_estimated_cost(inspection) -> float:
    # Placeholder function to calculate estimated cost based on inspection data
    # Implement this based on your business logic
    return 1000.0  # Example fixed cost

def get_photo_urls(inspection) -> List[str]:
    # Placeholder function to get URLs of photos associated with the inspection
    # Implement this based on how you're storing photos
    return []

def format_ssra(inspection) -> List[Dict[str, str]]:
    # Format Site-Specific Risk Assessment data
    return [
        {
            'hazard': ssra.hazard,
            'risk_level': ssra.risk_level,
            'control_measure': ssra.control_measure
        }
        for ssra in inspection.ssra_entries
    ]
