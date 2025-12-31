import bentoml
import pandas as pd
from schemas import EnergyInput
from typing import List

# Chargement du modèle
model_ref = bentoml.sklearn.get("energy_gb_model:latest")
model = model_ref.load_model()

feature_names = model_ref.custom_objects["feature_names"]

svc = bentoml.Service("energy_consumption_api")
