import bentoml
from pydantic import BaseModel, Field
import pandas as pd
model = bentoml.sklearn.load_model("energy_gb_model:latest")


FEATURES_ORDER = [
    'BuildingType', 'PrimaryPropertyType', 'Neighborhood', 'YearBuilt',
    'NumberofBuildings', 'NumberofFloors', 'PropertyGFATotal',
    'PropertyGFAParking', 'PropertyGFABuilding(s)',
    'LargestPropertyUseType', 'ListOfAllPropertyUseTypes',
    'LargestPropertyUseTypeGFA', 'SecondLargestPropertyUseType',
    'SecondLargestPropertyUseTypeGFA', 'ThirdLargestPropertyUseType',
    'ThirdLargestPropertyUseTypeGFA','DefaultData', 'ComplianceStatus',
    'Outlier'
]

class EnergyInput(BaseModel):
    # Variables numériques avec contraintes
    PropertyGFATotal: float = Field(..., gt=0, description="Surface totale")
    PropertyGFAParking: float = Field(default=0, ge=0)
    PropertyGFABuilding_s: float = Field(
        ..., 
        gt=0, 
        validation_alias="PropertyGFABuilding(s)", 
        serialization_alias="PropertyGFABuilding(s)"
    )    
    NumberofBuildings: int = Field(..., ge=1)
    NumberofFloors: int = Field(..., ge=0)
    YearBuilt: int = Field(..., ge=1850, le=2025)
    LargestPropertyUseTypeGFA: float = Field(..., ge=0)
    SecondLargestPropertyUseTypeGFA: float = Field(default=0, ge=0)
    ThirdLargestPropertyUseTypeGFA: float = Field(default=0, ge=0)
    
    # Variables catégorielles
    BuildingType: str
    PrimaryPropertyType: str
    Neighborhood: str
    LargestPropertyUseType: str
    ListOfAllPropertyUseTypes: str
    SecondLargestPropertyUseType: str = "None"
    ThirdLargestPropertyUseType: str = "None"
    DefaultData: str = "No"
    ComplianceStatus: str = "Compliant"
    Outlier: str = "None"

    model_config = {
        "extra": "forbid",
        "populate_by_name": True  
    }

@bentoml.service(resources={"cpu": "1"})
class EnergyService:
    
    @bentoml.api
    def predict(self, data: EnergyInput) -> dict:
        df = pd.DataFrame([data.model_dump(by_alias=True)])
        
        df = df[FEATURES_ORDER]
        
        prediction = model.predict(df)
        
        return {
            "predicted_site_energy_use": round(float(prediction[0]), 2),
            "unit": "kBtu"
        }