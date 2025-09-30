from fastapi import FastAPI

from app.domain.services.post import PostService
from app.domain.services.post_tag import PostTagService
from app.storage.memory.post import MemoryPostStorage
from app.storage.memory.post_tag import MemoryPostTagStorage
from app.transport.rest.fast_api.public import PublicAPI

# storage
post_repository = MemoryPostStorage()
post_tags_repository = MemoryPostTagStorage()

# domain
post_service = PostService(post_repository, post_tags_repository)
post_tags_service = PostTagService(post_tags_repository)

# transport
fastapi_app = FastAPI(title="SimpleBlog public API", version="0.1.0")

public_api = PublicAPI(fastapi_app)
public_api.set_domain_services(
    post_service,
    post_tags_service,
)
public_api.register()
