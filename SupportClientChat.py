from telethon import TelegramClient, functions
from telethon.tl.functions.messages import CreateChatRequest, EditChatAdminRequest

from config import phone_number, cloud_password, bot_username, bot_id


class SupportClientChat:

    def __init__(self, api_id, api_hash):
        self.client = TelegramClient(None, api_id, api_hash)

    async def client_start(self):
        await self.client.start(phone=phone_number, password=cloud_password)

    async def create_group_chat_with_link(self, title):
        result = await self.client(CreateChatRequest(users=[bot_username], title=title))
        supergroup_chat_id = result.chats[0].id
        await self.client(EditChatAdminRequest(supergroup_chat_id, bot_id, True))
        url_result = await self.client(functions.messages.ExportChatInviteRequest(supergroup_chat_id))
        print(supergroup_chat_id)
        return url_result.link, -supergroup_chat_id
