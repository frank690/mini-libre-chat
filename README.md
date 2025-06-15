# mini-libre-chat
> My very own mini libre chat version

## Whats happening here?
I am developing a custom interface to interact with various LLM's from different providers. This is primarily a fun project for me to try out stuff and learn something along the way.
An (incomplete) roadmap can be found in the [TODO list](./TODO.md).

## How to run this?
```bash
cd mini-libre-chat
python -m venv venv
.\venv\Scripts\activate  # on windows
pip install poetry
poetry install
uvicorn src.mini_libre_chat.api.main:app
```
