from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

class EmissionFactor(BaseModel):
    ef_id: int
    ipcc_category_1996: Optional[str] = None
    ipcc_category_2006: Optional[str] = None
    gas: Optional[str] = None
    fuel_1996: Optional[str] = None
    fuel_2006: Optional[str] = None
    c_pool: Optional[str] = None
    type_of_parameter: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[str] = None
    parameters_conditions: Optional[str] = Field(None, alias="Parameters / Conditions")
    region: Optional[str] = None
    abatement_tech: Optional[str] = None
    other_properties: Optional[str] = Field(None, alias="Other properties")
    value: Optional[str] = None
    unit: Optional[str] = None
    equation: Optional[str] = None
    ipcc_worksheet: Optional[str] = None
    technical_reference: Optional[str] = None
    source_of_data: Optional[str] = None
    data_provider: Optional[str] = None
    vector: List[float] = []
    
    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "ef_id": 234747,
                "ipcc_category_2006": "2.G.2.b - Accelerators",
                "gas": "Sulphur Hexafluoride",
                "description": "Tier 2 SF6 Emission Factor from industrial and medical particle accelerators",
                "value": "2",
                "unit": "Fraction of SF6/year"
            }
        }
    }

class EmissionFactorQuery(BaseModel):
    query: str = Field(..., description="The query text to search for similar emission factors")
    top_k: int = Field(5, description="Number of top results to return")

class EmissionFactorResponse(BaseModel):
    results: List[Dict[str, Any]]
    query_vector: List[float] 