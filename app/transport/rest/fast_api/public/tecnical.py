from app.transport.rest.fast_api.public.app import public_api


@public_api.get("/health")
def health():
    return {"status": "ok"}
