# SOLID/RAG Toolbox

**NOTE**
This setup is created for a demo project for PSX. There are still some references present to have a basic setup of policies and user roles in keycloak. There are 3 personae: Adam, Blake and Sandra which have certain access rights on each others data. To add data for these personae see "Adding Data" in the documentation, but make sure to add a metadata field 'type' with one of the following: calendar, financial, medical. For these 3 types and the personae policies are created on startup.

## Setup and starting services

All services contain a Dockerfile and can be build and run using Docker.
The following commands will build all the services (vector-api, chunk-api, keycloak-middleware),
start all dependecies (keycloak, postgres for keycloak, chromadb) and run the services.

```bash
docker compose -f docker-compose.yaml --profile service build

docker compose -f docker-compose.yaml --profile dependencies up -d

docker compose -f docker-compose.yaml --profile service up

```

## Documentation

Explore our [documentation](./documentation/README.md) for more information on the project. You'll find detailed guides on how to effectively use our services.
