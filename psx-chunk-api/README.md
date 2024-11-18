# Chunk API

## Dev Container

The project includes a dev container configuration that allows you to develop and run the project in a consistent and isolated environment. The dev container is defined using Docker and includes all the necessary dependencies and tools required for development. Adjust if needed per project's requirements.

## Taskfile

The project utilizes a Taskfile to define and automate common development tasks. The Taskfile is a simple and flexible task runner that allows you to define tasks using YAML syntax. It provides a convenient way to run commands, scripts, and other tasks related to your project.

Docs for Taskfile can be found [here](https://taskfile.dev/).

## Poetry

The project utilizes Poetry as a dependency management and packaging tool for Python projects. Poetry simplifies the process of managing project dependencies and ensures consistent and reproducible builds.

Please note that if you use the devcontainer, Poetry and Taskfile are not required to install locally.

Docs for Poetry can be found [here](https://python-poetry.org/docs/).

## Pkl

Pkl-lang files are used for configuring the application's config and its data model.
Docs for Pkl can be found [here](https://pkl-lang.org/).

---

Read more about [development](docs/development.md)


## API

### Documents endpoint

There is an endpoint available to chunk and store documents.

```
POST /documents
body:
{
    "inputType": "TEXT",
    "chunkType": "PARAGRAPH",
    "documents": ["some random text. with some sentences. \n\nwhich should be split"]
    "data_owner": "username"
    "metadata": [{"custom_md": "some metadata"}]
}
```

`inputType`, `chunkType`, `data_owner` and `documents` are mandatory fields. `documents` should contain a list of documents. The `data_owner` field contains the name of the owner of the added documents.
The possible values for inputType and chunkType are described below:

#### InputType

* `TEXT`: plain text
* `JSON`: json

#### ChunkType

* `OBJECT`: input list is split in objects
* `TOKENS`: every document in the list is split after 1000 tokens (characters). This can be set in config (`chunk_size_tokens`).
* `SENTENCE`: every document in the list is split on sentence (`.` -  period).
* `PARAGRAPH`: every document in the list is split in paragraphs (`\n` - new line).
