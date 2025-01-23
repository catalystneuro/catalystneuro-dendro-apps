from dendro.sdk import App
from PhotonFlux import PhotonFluxProcessor


app = App(app_name="photon_flux", description="Run Photon Flux Estimation for two photon imaging data.")

app.add_processor(PhotonFluxProcessor)


if __name__ == "__main__":
    app.run()
