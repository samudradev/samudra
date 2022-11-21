"""The entrypoint to serve the API
"""

from typing import Dict

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from samudra.conf.server.cors_policy import ALLOWED_ORIGINS
from samudra.server import lemmas, auth, golongan_kata

SLEEP_TIME: int = 10

app = FastAPI()

# TODO: Add more server endpoints!
app.include_router(lemmas.router)
app.include_router(auth.router)
app.include_router(golongan_kata.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> Dict[str, str]:
    """Test"""
    return {"details": "Successfully connected!"}


if __name__ == "__main__":
    # TODO Bind to database
    uvicorn.run("serve:app", port=8000, reload=True)

# TODO: CLI
# TODO: Share lemma via picture
