---
sidebar_position: 3
---

# Search embeddings

Searching vector embeddings is similar to adding data, but will require another resource to be used. In this implementation only the Vector API is available.

All requests to fetch data will also go through the keycloak middleware service, which will check policies and access rights of the requested data.

## Search request

The following snippet is an example of data request via the keycloak middleware service.

```bash
curl --location 'http://localhost:8002/vector-api/invoke' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <ACCESS_TOKEN>' \
--data-raw '{
    "question": "meetings on 15/11/2024",
    "user_data_requested": [
        "blake@psx.be"
    ],
    "type": "calendar",
    "full_document": "True"
}'
```

The URL contains the resource (`vector-api`) you are requesting data from. The middleware service first will check if the user logged in with the `access_token` has access to the resource. If not access will be denied.
Secondly the middleware will check the policies, to see if the logged in user has access on the requested data in the resource. In this example it will check if a policy exists that gives Adam (the logged in user, specified by the `access_token`) access to the calendar data of Blake. If such a policy is found, the request is forwarded to the Vector API to fetch the data.

### Request body

```json
{
    "question": "meetings on 15/11/2024",
    "user_data_requested": [
        "blake@psx.be"
    ],
    "type": "calendar",
    "full_document": "True"
}
```

This request body contains the information to search in the vector database.
    - `question`: The prompt/question that will be used to search the vector embeddings.
    - `user_data_requested`: A list of users for whom data is requested.
    - `type`: The type of data requested, this type is linked to the policies in the middleware, and can be set when adding data.
    - `full_document`: If set to `True` this will return the entire document where the question matched one of the chunks.

### Example response

```json
{
    "data": {
        "adam@psx.be": {
            "documents": {
                "ids": [
                    []
                ],
                "distances": [
                    []
                ],
                "embeddings": null,
                "documents": [
                    []
                ],
                "metadatas": [
                    []
                ],
                "uris": null,
                "data": null,
                "included": [],
                "highestScore": null
            },
            "user_data_requested": [
                "blake@psx.be"
            ],
            "question": "meetings on 15/11/2024"
        }
    },
    "errors": []
}
```

The response will have an object per user in `user_data_requested` with the retrieved documents from the vector database. This will contain the id's, the metadata, an highest scoring chunk and the actual documents (plus some extra data) retrieved from the database.
If something went wrong or access was denied the `errors` list will contain the errors or an access denied message.
