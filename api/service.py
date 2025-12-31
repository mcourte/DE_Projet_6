import bentoml
from pydantic import BaseModel, Field
import pandas as pd

# Charger le modèle (le Pipeline complet avec preprocessor)
model = bentoml.sklearn.load_model("energy_gb_model:latest")

# Liste ordonnée des colonnes utilisée lors du .fit()
# (Remplace par ta liste exacte 'features_to_keep')
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
        "populate_by_name": True  # Permet d'utiliser à la fois le nom Python et l'Alias
    }

@bentoml.service(resources={"cpu": "1"})
class EnergyService:
    
    @bentoml.api
    def predict(self, data: EnergyInput) -> dict:
        # AJOUT DE by_alias=True ICI :
        # Cela transforme 'PropertyGFABuilding_s' en 'PropertyGFABuilding(s)'
        df = pd.DataFrame([data.model_dump(by_alias=True)])
        
        # Maintenant, 'PropertyGFABuilding(s)' existe bien dans le df !
        df = df[FEATURES_ORDER]
        
        # Prédiction
        prediction = model.predict(df)
        
        return {
            "predicted_site_energy_use": round(float(prediction[0]), 2),
            "unit": "kBtu"
        }