# from telegram import Bot
# import asyncio

# # Replace with your actual bot token
# BOT_TOKEN = "7641266224:AAEWEOCqTL2At1dCFfN3PV1_fB0jaMns2Is" 

# # Replace with the actual group chat ID (remember the minus sign)
# GROUP_CHAT_ID = -1002569804746 # Example - replace with your group chat ID

# async def send_vcard_to_group_standalone():
#     bot = Bot(token=BOT_TOKEN)
#     async with bot: # Use async with bot for async operations

#         phone_number = "+84568993709" 
#         first_name = "Jane"
#         last_name = "Doe"

#         vcard_string=f"BEGIN:VCARD\nVERSION:3.0\nFN:{first_name or ''} {last_name or ''}\nTEL:{phone_number}\nEND:VCARD" 

#         await bot.send_contact(
#             chat_id=GROUP_CHAT_ID, 
#             phone_number=phone_number, 
#             first_name=first_name, 
#             last_name=last_name,
#             vcard=vcard_string 
#         )
#         print("VCard sent to the group successfully!")

# # Example usage:
# if __name__ == "__main__":
#     asyncio.run(send_vcard_to_group_standalone())


from telegram import Bot
import asyncio

BOT_TOKEN = "7641266224:AAEWEOCqTL2At1dCFfN3PV1_fB0jaMns2Is"
GROUP_CHAT_ID = -1002569804746  # ID nhóm

async def send_contact_card():
    bot = Bot(token=BOT_TOKEN)
    async with bot:
        await bot.send_contact(
            chat_id=GROUP_CHAT_ID,
            phone_number="+84569977169",  # Số điện thoại thật
            first_name="Shutt",
            last_name="Calvin"
            # Không truyền vcard!
        )
        print("✅ Đã gửi contact card đúng định dạng!")

if __name__ == "__main__":
    asyncio.run(send_contact_card())
