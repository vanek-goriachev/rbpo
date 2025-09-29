# from app.transport.rest.fast_api.common import ApiError
# from app.transport.rest.fast_api.public.app import public_api

# @public_api.post("/items")
# def create_item(name: str):
#     if not name or len(name) > 100:
#         raise ApiError(
#             code="validation_error", message="name must be 1..100 chars", status=422
#         )
#     item = {"id": len(_DB["items"]) + 1, "name": name}
#     _DB["items"].append(item)
#     return item
#
#
# @public_api.get("/items/{item_id}")
# def get_item(item_id: int):
#     for it in _DB["items"]:
#         if it["id"] == item_id:
#             return it
#     raise ApiError(code="not_found", message="item not found", status=404)
