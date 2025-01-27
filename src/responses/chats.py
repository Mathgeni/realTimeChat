chat_create_responses = {
    201: {"description": "Created"},
    400: {"description": "Bad Request"},
    409: {"description": "Chat with the same name already exists"},
}
chat_create_participants = {
    200: {"description": "Added"},
    400: {"description": "Bad Request"},
    409: {"description": "User in this chat already exists"},
}
chat_retrieve_responses = {
    200: {"description": "Successful response"},
    400: {"description": "Bad Request"},
    404: {"description": "Chat does not exist"},
}
chat_list_responses = {
    200: {"description": "Successful response"},
    400: {"description": "Bad Request"},
}
