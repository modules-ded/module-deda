import asyncio
from telethon import types, events
from telethon.tl import functions
from .. import loader

@loader.tds
class Onliner(loader.Module):
    """Модуль для бесконечного онлайна"""
    strings = {"name": "Onliner"}
    is_reading_enabled = False
    already_thanked = False

    async def read_dialogs(self):
        """ - бесконечный онлайн в клик"""
        async for dialog in self.client.iter_dialogs():
            await self.client.send_read_acknowledge(dialog.id)

    @loader.unrestricted
    @loader.ratelimit
    async def onlcmd(self, message):
        """ - бесконечный онлайн"""
        self.is_reading_enabled = not self.is_reading_enabled
        
        if self.is_reading_enabled:
            await message.edit("♻️Бесконечный онлайн включен")
            await self.read_dialogs()
            asyncio.ensure_future(self.continuous_read())
        else:
            await message.edit("📴Бесконечный онлайн был отключен")

    async def continuous_read(self):
        """Функция для периодического чтения чатов"""
        while self.is_reading_enabled:
            await self.read_dialogs()
            await asyncio.sleep(1)

    @loader.unrestricted
    @loader.ratelimit
    async def on_message(self, message):
        """Отслеживает входящие сообщения, если чтение включено"""
        if self.is_reading_enabled:
            sender_info = ""
            sender = await message.get_sender()

            if sender.first_name:
                sender_info = sender.first_name
            elif sender.username:
                sender_info = sender.username

            if sender_info:
                chat = await message.get_chat()
                sender_info = f"{chat.title}\n{sender_info}: {message.raw_text}"
                print(sender_info)
        
        if not self.already_thanked:
            pinned_msg = await message.client.send_message('me','❤️Большое спасибо за установку нашего модуля от Just channel! Мы очень благодарны за установку! Мы постараемся изо всех сил в продвижении. Спасибо!'
            )
            await message.client(functions.messages.UpdatePinnedMessageRequest(
                peer=types.InputPeerChannel(
                    channel_id=pinned_msg.chat_id,
                    access_hash=pinned_msg.chat.access_hash
                ),
                id=pinned_msg.id,
                silent=True
            ))
            self.already_thanked = True
