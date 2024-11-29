---
sidebar_position: 2
---

# Adding data

The service responsible for adding and storing data is the `chunk-api`. This service can be used to add documents and vector embeddings to the vector database. The OpenAPI specs can be found [here](http://localhost:8001/docs).

The Chunk API gets it name from the ability to chunk (or split) the input documents in smaller sizes before storing them as vector embeddings in the database. This results in smaller parts (chunks) and greatly improves the speed of searching for embeddings. The link between all these chunks and the original document is stored as well, so the entire document can be retrieved when needed.

To access this API, you will have to go through the `keycloak-middleware` service, which acts as a gateway to the SOLID Pod. The OpenAPI spec of this service can be found [here](http://localhost:8002/docs).

**NOTE**
In this setup the `v2` endpoints should be used. The other endpoints are legacy and will be deprecated in the future.

## Chunk and store data

This call is an example for adding data that will be chunked and vectorized before storing in the vector database.

```bash
curl --location 'localhost:8002/v2/chunk-api/documents' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <ACCESS_TOKEN>' \
--data '{
    "inputType": "TEXT",
    "chunkType": "PARAGRAPH",
    "documents": ["some example document", "another example document\n\nwhich should be split in paragraphs"],
    "metadata": { "type": "calendar" }
}'
```

### Headers

`Content-Type` is a required header and only `application/json` is supported right now. The body of the request contains the expected JSON object.

`Authorization` header is also required and must contain the `access_token` requested in the previous step. (see [Authorization & Authentication](./authorization-authentication.mdx#request-access-token))

### Request body

```json
{
  "inputType": "TEXT",
  "chunkType": "PARAGRAPH",
  "documents": ["some example document", "another example document\n\nwhich should be split in paragraphs"],
  "metadata": { "type": "calendar" }
}
```

The body contains the different options for chunking and ingesting the documents. - `inputType`: This field contains the type of input. At the moment only `TEXT` and `JSON` are supported, for respectively plain text and json objects. - `chunkType`: This field contains the chunking strategy used to split the documents when storing. The currently supported strategies are: + `OBJECT`: Used to split a list of JSON objects. + `SENTENCE`: This will split a text on sentences (`.`). + `PARAGRAPH`: This will split a text on new paragraphs (`\n`). + `TOKENS`: This will split a text or json object on number of tokens. The size of the chunks can be set in the config (`psx-chunk-api/config.pkl`) of the chunk-api (`chunk_size_tokens`, default is 1000). - `documents`: The actual documents that need to be chunked and stored. This is always a list of either strings of json objects. - `metadata`: This is a field to add metadata to the stored documents/chunks. This could be used in the future to search for more specific documents. The current implementation uses the `type` field in the metadata to check the policies for the users.

#### Metadata Type object

This field might need some more explanation.
As mentioned in
**TODO**
