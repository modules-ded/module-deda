from telethon import types, events
from telethon.tl import functions
from .. import loader

@loader.tds
class Onliner(loader.Module):
    """Бесконечный онлайн"""
    strings = {"name": "Onliner"}
    is_reading_enabled = False
    already_thanked = False

    @loader.unrestricted
    @loader.ratelimit
    async def onlcmd(self, message):
        """ - Бесконечный онлайн вкл/выкл"""
        self.is_reading_enabled = not self.is_reading_enabled
        
        if self.is_reading_enabled:
            await message.edit("❤‍🔥 Вы включили функцию Auto-Online! ")
            async for dialog in message.client.iter_dialogs():
                await message.client.send_read_acknowledge(dialog.id)
        else:
            await message.edit("♻️ Auto-Online успешно выключен!")

    @loader.unrestricted
    @loader.ratelimit
    async def on_message(self, message):
        """Слежка крч"""
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
            pinned_msg = await message.client.send_message(
                message.chat_id,
                "❤‍🔥Большое спасибо за установку нашего модуля от Just channel! Мы очень благодарны за установку! Мы постараемся изо всех сил в продвижении. Спасибо!"
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
