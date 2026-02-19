from aiogram import Bot, Dispatcher
from config import token
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler(), logging.FileHandler(
    "logs.log")])
logger = logging.getLogger(__name__)

bot = Bot(token=token)
dp = Dispatcher()
admins = {}
user_last_action = {}
dishes_info = []
message_cooldown = 2
callback_cooldown = 1
