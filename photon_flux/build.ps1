# Build the Docker image
docker build -t ghcr.io/catalystneuro/dendro-photon_flux:latest .

# Prompt user to push to GitHub Container Registry
$response = Read-Host -Prompt "Do you want to push to GitHub Container Registry? (y/n)"
if ($response -eq 'y') {
    docker push ghcr.io/catalystneuro/dendro-photon_flux:latest
}
