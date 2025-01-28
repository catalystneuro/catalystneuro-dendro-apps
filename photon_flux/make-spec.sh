#!/bin/bash

# Generate spec.json from processor
python -c "
from PhotonFlux import PhotonFluxProcessor
from dendro.sdk import ProcessorBase
import json

spec = {
    'name': 'photon_flux',
    'description': 'Photon Flux Estimation processors',
    'processors': [ProcessorBase.get_spec(PhotonFluxProcessor)]
}

with open('spec.json', 'w') as f:
    json.dump(spec, f, indent=4)
"
