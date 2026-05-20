#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import sys
import os

# حل مشكلة event loop في Python 3.14+
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# توكن البوت - تأكد من تغييره
TOKEN = "8308362115:AAFj9WDYSjF0YYlvo1r1bgkRPyXi49h1VJ4"

# محاولة استيراد المكتبات
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
    logger.info("✅ تم استيراد مكتبة python-telegram-bot بنجاح")
except ImportError as e:
    logger.error(f"❌ فشل استيراد المكتبات: {e}")
    sys.exit(1)

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إرسال رسالة ترحيبية عند أمر /start"""
    user = update.effective_user
    await update.message.reply_text(
        f"مرحباً {user.first_name}! 👋\n\n"
        f"✅ البوت يعمل بنجاح على Render.com\n"
        f"🤖 تم تشغيل البوت بدون أخطاء\n\n"
        f"📱 الأوامر المتاحة:\n"
        f"/start - بدء البوت\n"
        f"/help - المساعدة\n"
        f"/ping - اختبار البوت\n"
        f"/about - معلومات عن البوت"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إرسال رسالة المساعدة"""
    await update.message.reply_text(
        "🆘 المساعدة:\n\n"
        "هذا بوت تجريبي يعمل على Render.com\n\n"
        "الأوامر:\n"
        "/start - بدء البوت\n"
        "/help - عرض هذه المساعدة\n"
        "/ping - اختبار الاتصال\n"
        "/about - معلومات عن البوت"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """اختبار أن البوت يعمل"""
    await update.message.reply_text("🏓 Pong! البوت يعمل بنجاح ✅")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معلومات عن البوت"""
    await update.message.reply_text(
        "🤖 بوت تجريبي\n"
        f"📦 الإصدار: 1.0.0\n"
        f"🐍 Python: {sys.version}\n"
        f"⚙️ يعمل على: Render.com\n"
        f"✅ الحالة: نشط"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """رد على الرسائل النصية"""
    text = update.message.text
    await update.message.reply_text(f"أنت قلت: {text}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """معالج الأخطاء"""
    logger.error(f"حدث خطأ: {context.error}")
    if update and hasattr(update, 'effective_chat'):
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⚠️ عذراً، حدث خطأ داخلي. تم تسجيل الخطأ وإبلاغ المطور."
            )
        except:
            pass

def main():
    """الوظيفة الرئيسية لتشغيل البوت"""
    print("=" * 50)
    print("🤖 AOU Telegram Bot (نسخة مبسطة)")
    print("=" * 50)
    print(f"📱 التوكن: {TOKEN[:10]}...{TOKEN[-5:]}")
    print(f"🐍 Python: {sys.version}")
    print("=" * 50)
    print("✅ جاري تشغيل البوت...")
    print("📊 انتظر حتى تظهر رسائل التشغيل")
    print("=" * 50)
    
    # إنشاء التطبيق
    try:
        app = Application.builder().token(TOKEN).build()
        logger.info("✅ تم إنشاء التطبيق بنجاح")
    except Exception as e:
        logger.error(f"❌ فشل إنشاء التطبيق: {e}")
        sys.exit(1)
    
    # إضافة معالجات الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("about", about))
    
    # إضافة معالج للرسائل النصية
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # إضافة معالج الأخطاء
    app.add_error_handler(error_handler)
    
    # تشغيل البوت
    try:
        print("🚀 بدء polling...")
        app.run_polling(drop_pending_updates=True)
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف البوت بواسطة المستخدم")
    except Exception as e:
        logger.error(f"❌ خطأ فادح: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
