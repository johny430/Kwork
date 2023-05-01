# from telethon import TelegramClient, functions
# from telethon.tl.functions.messages import CreateChatRequest
#
#
# class SupportClientChat:
#
#     def __init__(self, api_id, api_hash):
#         self.client = TelegramClient(None, api_id, api_hash)
#
#     async def client_start(self):
#         await self.client.start(phone="+212 76 164 4011",password="9437")
#         # await self.client.run_until_disconnected()
#
#     async def create_group_chat_with_link(self, title):
#         result = await self.client(CreateChatRequest(users=[], title=title))
#         supergroup_chat_id = result.chats[0].id
#         result = await self.client(functions.messages.ExportChatInviteRequest(supergroup_chat_id))
#         return result.link
