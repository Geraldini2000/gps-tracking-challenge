from tcp_gateway.factory.message_handler_factory import MessageHandlerFactory


def get_last_location(device_id: str):
    repo = MessageHandlerFactory._repository
    return repo.get_last_location(device_id)
