import bot
from bot import Subject


subject_name = "ฟิสิกส์ 2"
subject_code = "ว30212"
subject_section = "4"
subject = Subject(
    name=subject_name,
    code=subject_code,
    section=subject_section
)

bot.BotWorker().enroll(
    subject=subject,
)


print("press enter to exit")
input()