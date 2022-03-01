import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Filters
from tenacity import retry, wait_fixed, stop_after_attempt
import wof_db

TOKEN = '1881355037:AAG8ttFhTeQzCm_cyjqD-bZ_Yf5DwTQMCj8'

##test token : 1858625868:AAHxsfbOYTux-gSCWTDg2sDRWiTq8gmmykE
# main bot : 1881355037:AAG8ttFhTeQzCm_cyjqD-bZ_Yf5DwTQMCj8

bot = telebot.TeleBot(token=TOKEN, num_threads=10)

creators = [1686875746, 638994540,134933697]

achv = '''🛡  ۵ دفـاع مـوفـق 
⟮ 1000 XP ⟯

‌  ⚔️  ۵ حـمـلـه مـوفـق
 ⟮ 1000 XP ⟯

برد حریف با سناریوی کمتر...🗡 
⟮ 2000 XP ⟯

‌  💸  مجموع خرید از شـاپـ⟮ ۱,۰۰۰,۰۰۰ ﷼ ⟯
 ⟮ 2000 XP ⟯

‌  💸  مجموع خرید از شـاپـ⟮ ۵,۰۰۰,۰۰۰ ﷼ ⟯
 ⟮ 5000 XP ⟯

‌  💸  مجموع خرید از شـاپـ⟮ ۱۰,۰۰۰,۰۰۰ ﷼ ⟯
 ⟮ 10000 XP ⟯ 

تکمیل یک فـصـل کامـل بدون خرید و گرفتن رتبه‌ی بـرتـریـن پلیر فصل...📸
⟮ 10000 XP ⟯

「🤖」موفقیت در ربات استوری 
⟮ 2000 XP ⟯

کشتن شوالیه آتش 🔥 
⟮ 2000 XP ⟯

「🤖」رسیدن به روز سوم در ربات استوری
 ⟮ 2000 XP ⟯

‌  ➰  رفتن به نـیـمـه نـهـایـی در تـورنـمـنـتـ
⟮ 3000 XP ⟯

‌  ➰  رفتن به فـیـنـال در تـورنـمـنـتـ
⟮ 3500 XP ⟯

‌  ➰  رسیدت به پیروزی نهایی در تـورنـمـنـتـ 
⟮ 4500 XP ⟯


کشتن هیروی حـریـف...⚔️
⟮ 6000 XP ⟯

پـیـروز شدن در برابر ارتش سومین شخص قدرتمند بازی🪓
⟮ 5000 XP ⟯

پیروز شدن در برابر ارتش دومین شخص قدرتمند بازی🪓
⟮ 6000 XP ⟯

پیروز شدن در برابر ارتش اولین شخص قدرتمند بازی🪓
⟮ 10000 XP ⟯

پیروز شدن در برابر ارتش شخصی که خرید زده در حالی که شما خریدی نزده‌اید🛍
⟮ 5000 XP ⟯

پیروز شدن با ارتش کمتر در برابر حریف⛓
⟮ 5000 XP ⟯

تصرف قلعه‌ی حریف با تلفات کمتر از یک سوم🗡
⟮ 3000 XP ⟯

تصرف قلعه‌ی حریف با ارتش کمتر🤺
⟮ 5000 XP ⟯

انجام دادن ۱۰ تـسـکـ🎯
⟮ 2500 XP ⟯

به پایان رساندن ۵ ایـونـتـ🎮
⟮ 5000 XP ⟯

تلفات زدن ۱۰۰ درصدی به حریف...💣
⟮ 10000 XP ⟯'''

achives = ['🛡  ۵ دفـاع مـوفـق', '‌  ⚔️  ۵ حـمـلـه مـوفـق', 'برد حریف با سناریوی کمتر...🗡',
           '‌  💸  مجموع خرید از شـاپـ⟮ ۱,۰۰۰,۰۰۰ ﷼ ⟯', '‌  💸  مجموع خرید از شـاپـ⟮ ۵,۰۰۰,۰۰۰ ﷼ ⟯',
           '‌  💸  مجموع خرید از شـاپـ⟮ ۱۰,۰۰۰,۰۰۰ ﷼ ⟯',
           'تکمیل یک فـصـل کامـل بدون خرید و گرفتن رتبه‌ی بـرتـریـن پلیر فصل...📸', '「🤖」موفقیت در ربات استوری',
           'کشتن شوالیه آتش که تنها در فصل سوم هست...🔥', '「🤖」رسیدن به روز سوم در ربات استوری',
           '‌  ➰  رفتن به نـیـمـه نـهـایـی در تـورنـمـنـتـ', '‌  ➰  رفتن به فـیـنـال در تـورنـمـنـتـ',
           '‌  ➰  رسیدت به پیروزی نهایی در تـورنـمـنـتـ', 'کشتن هیروی حـریـف...⚔️',
           'پـیـروز شدن در برابر ارتش سومین شخص قدرتمند بازی🪓', 'پیروز شدن در برابر ارتش دومین شخص قدرتمند بازی🪓',
           'پیروز شدن در برابر ارتش اولین شخص قدرتمند بازی🪓',
           'پیروز شدن در برابر ارتش شخصی که خرید زده در حالی که شما خریدی نزده‌اید🛍',
           'پیروز شدن با ارتش کمتر در برابر حریف⛓', 'تصرف قلعه‌ی حریف با تلفات کم🗡', 'تصرف قلعه‌ی حریف با ارتش کمتر🤺',
           'انجام دادن ۱۰ تـسـکـ🎯', 'به پایان رساندن ۵ ایـونـتـ🎮', 'تلفات زدن ۱۰۰ درصدی به حریف...💣']
prices = [1000, 1000, 2000, 2000, 5000, 10000, 10000, 2000, 2000, 2000, 3000, 3500, 4500, 6000, 5000, 6000, 10000, 5000,
          5000, 3000, 5000, 2500, 5000, 10000]


def check_admin(user_id):
    admins = wof_db.load_admins()
    if not admins:
        return False
    elif user_id in admins:
        return True
    else:
        return False


def reginmarkup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('「📝」ثـبـت‌نـام', callback_data='signup'))
    markup.add(InlineKeyboardButton('「🤹🏻」ورود', callback_data='signin'))
    return markup


def reg(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'لطفا انـتـخـاب كنيد...🏷', reply_markup=reginmarkup())


def userpanel(message):
    bot.send_message(message.from_user.id, f'''「🤍」خوش‌ا‌ومدی.!
لطفا انـتـخـاب کنید.
        ━━•✜•━━
{get_hyperlink()}''', reply_markup=panelmarkup(), parse_mode='markdown', disable_web_page_preview=True)


def panelmarkup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('‌  🧾  نـمـایـشـ𝚇𝙿', callback_data='show xp'))
    markup.add(InlineKeyboardButton('📊」 𝙻𝚎𝚟𝚎𝚕|...نمـایش سطـحـ', callback_data='show level'))
    markup.add(InlineKeyboardButton('「📋」اسـتـیـت', callback_data='showstate'))
    markup.add(InlineKeyboardButton('「📃」اچـیـومـنـت‌هـا', callback_data='showach'))
    markup.add(InlineKeyboardButton('「📃」اچـیـومـنـت‌هـای روزانه', callback_data='daily achive'))
    markup.add(InlineKeyboardButton('「📋」اچیومنت‌های مـن', callback_data='myachves'))
    markup.add(InlineKeyboardButton('شـهـرهـای من...🏢', callback_data='mytowns'))
    markup.add(
        InlineKeyboardButton('🗄」 𝚂𝚑𝚘𝚠 𝙸𝚗𝚏𝚘𝚛𝚖𝚊𝚝𝚒𝚘𝚗|...نـمایش اطلاعـاتـ', callback_data='show info'))
    markup.add(InlineKeyboardButton('𝙻𝚘𝚐𝙾𝚞𝚝...📲', callback_data='logout'))
    return markup


def set_level(xp):
    j = 0
    for i in range(0, 11):
        if (i + j) * 1000 <= xp < (2 * i + j + 1) * 1000:
            return i + 1
        j += i
    return 11


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global achives
    data = call.data
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    if data == 'signup':
        if wof_db.checksignup(user_id):
            bot.edit_message_text(
                '''「🚧」اخطار!
شما یکبار با این اکانت ثبت نام کرده‌اید لطفا با دکمه ورود به اکانت خود وارد شوید.!''',
                call.message.chat.id, call.message.message_id, reply_markup=reginmarkup())
            return
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
        markup.add('cancel')
        name = bot.send_message(user_id, '「✏️」لطفا اسم خود وارد كنيد.', reply_markup=markup)
        bot.register_next_step_handler(name, checkname)
        return
    elif 'useraccept' in data:
        data = data.split(' ')
        user_id = int(data[1])
        info = wof_db.load_information(user_id)
        name = info[0]
        username = info[1]
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('「✔️」تـائـيـد', callback_data=f'adminaccept {user_id}'),
                   InlineKeyboardButton('「✖️」عـدم تـائـيـد', callback_data=f'adminunaccept {user_id}'))
        bot.send_message(-1001477365209, f'''「🗽」𝙽𝚎𝚠 𝚄𝚜𝚎𝚛
𝚄𝚜𝚎𝚛 𝙸𝚍: `{user_id}`
𝙽𝚊𝚖𝚎: `{name}`
𝚄𝚜𝚎𝚛𝙽𝚊𝚖𝚎: `{username}`
آيا ثـبـت‌نـام كاربر را تائيد می‌كنيد:''', reply_markup=markup, parse_mode='markdown')
        bot.edit_message_text('لطفا منتظر تاييد ثبت‌نام شما توسط ادمين‌ها باشيد.💬', call.message.chat.id,
                              call.message.message_id)
    elif 'userunaccept' in data:
        data = data.split(' ')
        user_id = int(data[1])
        wof_db.del_tuple(user_id)
        bot.edit_message_text('‌ 🔖 لطفا با زدن ثبت‌نام نسبت به ثبت‌نام مجدد خود اقدام كنيد.!', call.message.chat.id,
                              call.message.message_id, reply_markup=reginmarkup())
    elif 'adminaccept' in data:
        if not check_admin(user_id):
            bot.answer_callback_query(call.id, 'شما ادمین ربات نیستید.!', show_alert=True)
            return
        data = data.split(' ')
        user_id = int(data[1])
        wof_db.acceptacc(user_id)
        bot.send_message(user_id, '''ثبت‌نام شما تائید شد...🔝
لطفا از قسمت ورود وارد اكانت خود شويد.!''', reply_markup=reginmarkup())
        info = wof_db.load_information(user_id)
        name = info[0]
        username = info[1]
        bot.edit_message_text(f'''「📇」ثـبـت‌نـام كاربر تـائـيـد شد.
𝙽𝚊𝚖𝚎: `{name}`
𝚄𝚜𝚎𝚛𝙽𝚊𝚖𝚎: `{username}`
𝚄𝚜𝚎𝚛 𝙸𝚍: `{user_id}`''', call.message.chat.id, call.message.message_id, parse_mode='markdown')
    elif 'adminunaccept' in data:
        if not check_admin(user_id):
            bot.answer_callback_query(call.id, 'شما ادمین ربات نیستید.!', show_alert=True)
            return
        data = data.split(' ')
        user_id = int(data[1])
        wof_db.del_tuple(user_id)
        bot.edit_message_text('「✖️」ثبت‌نام كاربر رد شد.', call.message.chat.id, call.message.message_id)
        try:
            bot.send_message(user_id, '''「📱」توجه...
ثبت نام شما تاييد نشد لطفا نسبت به ثبت نام مجدد خود اقدام كنيد.!''', reply_markup=reginmarkup())
        except:
            pass

    elif data == 'signin':
        load = wof_db.loadactives()
        users = load[0]
        if user_id in users:
            bot.edit_message_text('شما هم اکنون با یک اکانت وارد شده‌اید.!', call.message.chat.id,
                                  call.message.message_id, reply_markup=reginmarkup())
            return
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
        markup.add('cancel')
        username = bot.send_message(user_id, 'لطفا يوزرنيم خود را وارد كنيد...⌨️', reply_markup=markup)
        bot.register_next_step_handler(username, signinusername)
        return
    elif data == 'show xp':
        if not wof_db.check_active(user_id):
            bot.edit_message_text('''شما با اکانتی وارد نشده‌اید. 
لطفا نسبت به ثبت‌نام یا ورود اقدام کنید!''', user_id,
                                  call.message.message_id, reply_markup=reginmarkup())
            return
        usr = wof_db.load_username(user_id)
        xp = wof_db.loadxp(usr[0])
        bot.edit_message_text(f'''`「📊」مـقـدار 𝚇𝙿 شمـا: {xp[0]}`''', user_id, call.message.message_id,
                              reply_markup=panelmarkup(), parse_mode='markdown')
    elif data == 'show level':
        if not wof_db.check_active(user_id):
            bot.edit_message_text('''شما با اکانتی وارد نشده‌اید. 
لطفا نسبت به ثبت‌نام یا ورود اقدام کنید!''', user_id,
                                  call.message.message_id, reply_markup=reginmarkup())
            return
        usr = wof_db.load_username(user_id)
        xp = wof_db.loadxp(usr[0])
        level = set_level(xp[0])
        bot.edit_message_text(f'''📇  𝐘𝐨𝐮𝐫 𝐋𝐞𝐯𝐞𝐥  `{level}`''', user_id, call.message.message_id,
                              reply_markup=panelmarkup(), parse_mode='markdown')
    elif data == 'showach':
        bot.edit_message_text(achv, user_id, call.message.message_id, reply_markup=panelmarkup())
    elif data == 'myachves':
        if not wof_db.check_active(user_id):
            bot.edit_message_text('''شما با اکانتی وارد نشده‌اید. 
لطفا نسبت به ثبت‌نام یا ورود اقدام کنید!''', user_id,
                                  call.message.message_id, reply_markup=reginmarkup())
            return
        username = wof_db.load_username(user_id)
        achivs = wof_db.load_achvs(username[0])
        if achivs == '':
            bot.edit_message_text('شما اچـيـومـنـتـی نداريد.!✖️', user_id, call.message.message_id,
                                  reply_markup=panelmarkup())
        else:
            ach = ''
            achvs = achivs.split(" ")
            for i in achvs:
                ach += f'{achives[int(i) - 1]}\n'
            bot.edit_message_text(ach, user_id, call.message.message_id, reply_markup=panelmarkup())
    elif data == 'mytowns':
        if not wof_db.check_active(user_id):
            bot.edit_message_text('''شما با اکانتی وارد نشده‌اید. 
لطفا نسبت به ثبت‌نام یا ورود اقدام کنید!''', user_id,
                                  call.message.message_id, reply_markup=reginmarkup())
            return
        username = wof_db.load_username(user_id)
        towns = wof_db.load_towns(username[0])
        if towns == '':
            bot.edit_message_text('✖️ شما شهری نداريد.!', user_id, call.message.message_id, reply_markup=panelmarkup())
        else:
            town = ''
            ton = towns.split(",")
            for i in ton:
                town += f'{i}\n'
            bot.edit_message_text(town, user_id, call.message.message_id, reply_markup=panelmarkup())
    elif data == 'show info':
        if not wof_db.check_active(user_id):
            bot.edit_message_text('''شما با اکانتی وارد نشده‌اید. 
لطفا نسبت به ثبت‌نام یا ورود اقدام کنید!''', user_id,
                                  call.message.message_id, reply_markup=reginmarkup())
            return
        load = wof_db.load_information(user_id)
        name = load[0]
        username = load[1]
        towns = load[3].replace(',', ', ')
        achvs = load[4]
        msg = f'''⤷𝚄𝚜𝚎𝚛 𝙸𝚍: `{user_id}`
        ━━•✜•━━
⤷𝙽𝚊𝚖𝚎: `{name}`
        ━━•✜•━━
⤷𝚄𝚜𝚎𝚛𝚗𝚊𝚖𝚎: `{username}`
        ━━•✜•━━
⤷𝚃𝚘𝚠𝚗𝚜: `{towns}`
        ━━•✜•━━
⤷𝙰𝚌𝚑𝚒𝚟𝚎𝚜 𝙽𝚞𝚖𝚋𝚎𝚛: `{achvs}`
        ━━•✜•━━
{get_hyperlink()}'''
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('📝Edιт Name|ویرایش اسم', callback_data='edit name'))
        markup.add(InlineKeyboardButton('📝Edιт UserName|ویرایش یوزنیم', callback_data='edit user'))
        markup.add(InlineKeyboardButton('📝Edιт PassWord|ویرایش پسورد', callback_data='edit pass'))
        markup.add(InlineKeyboardButton('🔙  Bᴀᴄᴋ|بـازگشـتـ', callback_data='main menu'))
        bot.edit_message_text(msg, user_id, call.message.message_id, reply_markup=markup, parse_mode='markdown',
                              disable_web_page_preview=True)

    elif data == 'edit name':
        if not wof_db.check_active(user_id):
            bot.edit_message_text('''شما با اکانتی وارد نشده‌اید. 
        لطفا نسبت به ثبت‌نام یا ورود اقدام کنید!''', user_id,
                                  call.message.message_id, reply_markup=reginmarkup())
            return
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
        markup.add('cancel')
        name = bot.send_message(user_id, 'لطفا اسم جدید خود را وارد كنيد...⌨️', reply_markup=markup)
        bot.register_next_step_handler(name, updatename)
        return
    elif data == 'edit pass':
        if not wof_db.check_active(user_id):
            bot.edit_message_text('''شما با اکانتی وارد نشده‌اید. 
        لطفا نسبت به ثبت‌نام یا ورود اقدام کنید!''', user_id,
                                  call.message.message_id, reply_markup=reginmarkup())
            return
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
        markup.add('cancel')
        password = bot.send_message(user_id, 'لطفا رمز جدید خود را وارد كنيد...⌨️', reply_markup=markup)
        bot.register_next_step_handler(password, updatepass)
        return
    elif data == 'edit user':
        if not wof_db.check_active(user_id):
            bot.edit_message_text('''شما با اکانتی وارد نشده‌اید. 
        لطفا نسبت به ثبت‌نام یا ورود اقدام کنید!''', user_id,
                                  call.message.message_id, reply_markup=reginmarkup())
            return
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
        markup.add('cancel')
        username = bot.send_message(user_id, 'لطفا یوزنیم جدید خود را وارد كنيد...⌨️', reply_markup=markup)
        bot.register_next_step_handler(username, updateuser)
        return

    elif data == 'main menu':
        if not wof_db.check_active(user_id):
            bot.edit_message_text('''شما با اکانتی وارد نشده‌اید. 
        لطفا نسبت به ثبت‌نام یا ورود اقدام کنید!''', user_id,
                                  call.message.message_id, reply_markup=reginmarkup())
            return
        bot.edit_message_text(f'''「🤍」خوش‌ا‌ومدی.!
لطفا انـتـخـاب کنید.
        ━━•✜•━━
{get_hyperlink()}''', user_id, call.message.message_id, reply_markup=panelmarkup(), parse_mode='markdown',
                              disable_web_page_preview=True)

    elif data == 'logout':
        if not wof_db.check_active(user_id):
            bot.edit_message_text('''شما با اکانتی وارد نشده‌اید. 
لطفا نسبت به ثبت‌نام یا ورود اقدام کنید!''', user_id,
                                  call.message.message_id, reply_markup=reginmarkup())
            return
        if wof_db.check_active(user_id):
            wof_db.deactive(user_id)
            bot.edit_message_text('''「🗳」شما از اكانت خود خارج شديد.
لطفا انـتـخـابـ كنيد!''', user_id, call.message.message_id, reply_markup=reginmarkup())
        else:
            bot.edit_message_text('''「🚧」شما داخل اكانتی نيستيد لطفا انتخاب كنيد...''', user_id,
                                  call.message.message_id, reply_markup=reginmarkup())

#     elif 'winn' in data:
#         if not check_admin(user_id):
#             bot.answer_callback_query(call.id, 'شما ادمین ربات نیستید.!', show_alert=True)
#             return
#         text = data.split(" ")
#         username = text[1]
#         town = text[2]
#         att_username = text[3]
#         att_town = text[4]
#         markup = InlineKeyboardMarkup()
#         markup.add(
#             InlineKeyboardButton('「✔️」تـائـيـد', callback_data=f'catt {username} {town} {att_username} {att_town} win'),
#             InlineKeyboardButton('「✖️」عـدم تـائـيـد', callback_data=f'unconfirmattack'))
#         bot.edit_message_text(f"""𝚄𝚜𝚎𝚛𝙽𝚊𝚖𝚎: `{username}`
# 𝚃𝚘𝚠𝚗: `{town}`
# 𝙰𝚝𝚝𝚊𝚌𝚔𝚎𝚍 𝚝𝚘 𝚞𝚜𝚎𝚛𝚗𝚊𝚖𝚎: `{att_username}`
# 𝚃𝚘𝚠𝚗: `{att_town}` 𝚊𝚗𝚍 𝚆𝚒𝚗 𝚝𝚑𝚎 𝚠𝚊𝚛...✖️""", chat_id,
#                               call.message.message_id,
#                               reply_markup=markup, parse_mode='markdown')
#
#     elif 'losee' in data:
#         if not check_admin(user_id):
#             bot.answer_callback_query(call.id, 'شما ادمین ربات نیستید.!', show_alert=True)
#             return
#         text = data.split(" ")
#         username = text[1]
#         town = text[2]
#         att_username = text[3]
#         att_town = text[4]
#         markup = InlineKeyboardMarkup()
#         markup.add(
#             InlineKeyboardButton('「✔️」تـائـيـد',
#                                  callback_data=f'catt {username} {town} {att_username} {att_town} lose'),
#             InlineKeyboardButton('「✖️」عـدم تـائـيـد', callback_data=f'unconfirmattack'))
#         bot.edit_message_text(f"""𝚄𝚜𝚎𝚛𝙽𝚊𝚖𝚎: `{username}`
# 𝚃𝚘𝚠𝚗: `{town}`
# 𝙰𝚝𝚝𝚊𝚌𝚔𝚎𝚍 𝚝𝚘 𝚞𝚜𝚎𝚛𝚗𝚊𝚖𝚎: `{att_username}`
# 𝚃𝚘𝚠𝚗: `{att_town}` 𝚊𝚗𝚍 𝚕𝚘𝚜𝚎 𝚝𝚑𝚎 𝚠𝚊𝚛...✔️""", chat_id,
#                               call.message.message_id,
#                               reply_markup=markup, parse_mode='markdown')
#
#     elif 'catt' in data:
#         if not check_admin(user_id):
#             bot.answer_callback_query(call.id, 'شما ادمین ربات نیستید.!', show_alert=True)
#             return
#         text = data.split(" ")
#         if text[5] == 'win':
#             text[5] = True
#         else:
#             text[5] = False
#         wof_db.record_war(text[1], text[3], text[2], text[4], text[5])
#         if text[5]:
#             status = '𝚆𝚒𝚗'
#         else:
#             status = '𝚕𝚘𝚜𝚎'
#         bot.edit_message_text(f'''اتک با موفقيت ثبـت شد.⚔️
# 𝚄𝚜𝚎𝚛𝙽𝚊𝚖𝚎: `{text[1]}`
# 𝚃𝚘𝚠𝚗: `{text[2]}`
# 𝙰𝚝𝚝𝚊𝚌𝚔𝚎𝚍 𝚝𝚘 𝚞𝚜𝚎𝚛𝚗𝚊𝚖𝚎: `{text[3]}`
# 𝚃𝚘𝚠𝚗: `{text[4]}` 𝚊𝚗𝚍 {status} 𝚝𝚑𝚎 𝚠𝚊𝚛...✔️''', chat_id, call.message.message_id, parse_mode='markdown')
#     elif data == 'unconfirmattack':
#         if not check_admin(user_id):
#             bot.answer_callback_query(call.id, 'شما ادمین ربات نیستید.!', show_alert=True)
#             return
#         bot.edit_message_text('اتک لغـو شد.⚔️', chat_id, call.message.message_id)

    elif data == 'showstate':
        if not wof_db.check_active(user_id):
            bot.edit_message_text('''شما با اکانتی وارد نشده‌اید. 
لطفا نسبت به ثبت‌نام یا ورود اقدام کنید!''', user_id,
                                  call.message.message_id, reply_markup=reginmarkup())
            return
        username = wof_db.load_username(user_id)
        data = wof_db.load_state(username[0])
        state = f'''
`{data[0]}` ᴀᴛᴛᴀᴄᴋs
`{data[1]}` ᴡɪɴs
`{data[2]}` ʟᴏssᴇs 
`{data[3]}` ᴅᴇғᴇɴsᴇs
`{data[4]}` sᴜᴄᴄᴇssғᴜʟ ᴅᴇғᴇɴsᴇs
`{data[5]}` ᴜɴsᴜᴄᴄᴇssғᴜʟ ᴅᴇғᴇɴsᴇs'''
        attackto = wof_db.get_attackto(username[0])
        usr = attackto[0]
        num = attackto[1]
        state += f'''\n「🤺 ᴘʟᴀʏᴇʀs ʏᴏᴜ ᴀᴛᴛᴀᴄᴋᴇᴅ ᴍᴏsᴛ...'''
        j = 0
        for i in usr:
            state += f'''\n     `{num[j]}`    `{i}`'''
            j += 1
        attackfrom = wof_db.get_attackfrom(username[0])
        j = 0
        usr = attackfrom[0]
        num = attackfrom[1]
        state += f'''\n\n「🤺 ᴘʟᴀʏᴇʀs ᴡʜᴏ ᴀᴛᴛᴀᴄᴋᴇᴅ ʏᴏᴜ ᴍᴏsᴛ...'''
        for i in usr:
            state += f'''\n     `{num[j]}`    `{i}`'''
            j += 1
        xp = wof_db.loadxp(username[0])
        state += f'\n📇  𝐋𝐞𝐯𝐞𝐥 `{set_level(xp[0])}`'
        state += f'''\n        ━━•✜•━━
        {get_hyperlink()}'''
        bot.edit_message_text(state, user_id, call.message.message_id, reply_markup=panelmarkup(),
                              parse_mode='markdown', disable_web_page_preview=True)
    elif data == 'daily achive':
        if not wof_db.check_active(user_id):
            bot.edit_message_text('''شما با اکانتی وارد نشده‌اید. 
        لطفا نسبت به ثبت‌نام یا ورود اقدام کنید!''', user_id,
                                  call.message.message_id, reply_markup=reginmarkup())
            return
        load = wof_db.load_ach()
        ids = load[0]
        achvss = load[1]
        prices = load[2]
        if len(ids) == 0:
            bot.edit_message_text('اچیو روزانه ایی ثبت نشده است.!✖️', user_id, call.message.message_id,
                                  reply_markup=panelmarkup())
            return
        i = 0
        achvv = '''𝖣𝖺𝗂𝗅𝗒 𝖠𝖼𝗁𝗂𝗏𝖾 𝖫𝗂𝗌𝗍🗞
            ━━•✜•━━\n'''
        for ach in achvss:
            achvv += f'''{ach} 
        ( `{prices[i]}` 𝚇𝚙🪙 )
                ━━•✜•━━\n'''
            i += 1
        achvv += get_hyperlink()
        bot.edit_message_text(achvv, user_id, call.message.message_id, reply_markup=panelmarkup(),
                              parse_mode='markdown', disable_web_page_preview=True)


def updatename(message):
    name = message.text
    user_id = message.from_user.id
    if message.text == 'cancel':
        bot.reply_to(message, '''کنسل شد''')
        if wof_db.check_active(user_id):
            userpanel(message)
        else:
            reg(message)
        return
    if len(name) < 5 or len(name) > 20:
        name = bot.send_message(message.from_user.id,
                                '「📟」اسم بايد بيشتر از 5 و کمتر از 20 حرف باشد لطفا مجددا وارد نمایید.!')
        bot.register_next_step_handler(name, updatename)
        return
    wof_db.update_name(user_id, name)
    bot.send_message(user_id, 'نام شما با موفقیت تغییر کرد...🤖')
    if wof_db.check_active(user_id):
        userpanel(message)


def updatepass(message):
    password = message.text
    user_id = message.from_user.id
    if message.text == 'cancel':
        bot.reply_to(message, '''کنسل شد''')
        if wof_db.check_active(user_id):
            userpanel(message)
        else:
            reg(message)
        return
    if len(password) < 5 or len(password) > 20:
        password = bot.send_message(message.from_user.id,
                                    '「📟」رمـز بايد بيشتر از 5 و کمتر از 20 حرف باشد لطفا مجددا وارد نمایید.!')
        bot.register_next_step_handler(password, updatepass)
        return
    if ' ' in password:
        password = bot.send_message(message.from_user.id, 'رمز حاوی فاصله نباشد لطفا مجددا وارد نمایید.!')
        bot.register_next_step_handler(password, updatepass)
        return
    wof_db.update_pass(user_id, password)
    bot.send_message(user_id, 'پسورد شما با موفقیت تغییر کرد...🤖')
    if wof_db.check_active(user_id):
        userpanel(message)


def updateuser(message):
    username = message.text.lower()
    user_id = message.from_user.id
    if message.text == 'cancel':
        bot.reply_to(message, '''کنسل شد''')
        if wof_db.check_active(user_id):
            userpanel(message)
        else:
            reg(message)
        return
    if len(username) < 5 or len(username) > 20:
        username = bot.send_message(message.from_user.id,
                                    'يوزرنيم بايد بيشتر از 5 و کمتر از 20 حرف باشد لطفا مجددا وارد نمایید.!')
        bot.register_next_step_handler(username, updateuser)
        return
    if '@' in username:
        username = bot.send_message(message.from_user.id,
                                    ' 🪧 يوزرنيم حاوی فاصله و [ @ ] نباشد لطفا مجددا وارد نمایید.!')
        bot.register_next_step_handler(username, updateuser)
        return
    if ' ' in username:
        username = bot.send_message(message.from_user.id,
                                    ' 🪧 يوزرنيم حاوی فاصله و [ @ ] نباشد لطفا مجددا وارد نمایید.!')
        bot.register_next_step_handler(username, updateuser)
        return
    all_users = wof_db.load_usernames()
    all_users = [x.lower() for x in all_users]
    if username in all_users:
        username = bot.send_message(message.from_user.id,
                                    '「👤」اين ايدی توسط شخص ديگر استفاده شده است لطفا يك ايدی ديگر وارد كنيد.!')
        bot.register_next_step_handler(username, updateuser)
        return
    ld = wof_db.load_information(user_id)
    oldid = ld[1]
    wof_db.update_username(user_id, username, oldid)
    bot.send_message(user_id, 'یوزرنیم شما با موفقیت تغییر کرد...🤖')
    if wof_db.check_active(user_id):
        userpanel(message)


def signinusername(message):
    username = message.text.lower()
    users = wof_db.load_usernames()
    if message.text == 'cancel':
        bot.reply_to(message, '''canceled''')
        return
    if username not in users:
        bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                         text='''「📌」ايدی وارد شده اشتباه است!
لطفا مجددا تلاش كنيد.''',
                         reply_markup=reginmarkup())
        return
    check = wof_db.checkacc(username)
    try:
        if not check[0]:
            bot.reply_to(message, 'اکانت شما هنوز مورد تائید ادمین‌ها قرار نگرفته است لطفا منتظر تائید باشید...🔖')
            return
    except:
        bot.reply_to(message, 'اکانت شما هنوز مورد تائید ادمین‌ها قرار نگرفته است لطفا منتظر تائید باشید...🔖')
        return
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
    markup.add('cancel')
    password = bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                text='لطفا رمز خود را وارد كنيد...⌨️', reply_markup=markup)
    bot.register_next_step_handler(password, signinpass, username)
    return


def signinpass(message, username):
    password = message.text
    realpass = wof_db.load_pass(username)
    if message.text == 'cancel':
        bot.reply_to(message, '''canceled''')
        return
    if realpass[0] != password:
        bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                         text='''「🚧」اخطار پسورد وارد شده اشتباه است.
لطفا مجددا تلاش كنيد.!''',
                         reply_markup=reginmarkup())
        return

    wof_db.recordactive(message.from_user.id, username)
    usr = wof_db.load_uid(username)
    if usr[0] != message.from_user.id:
        wof_db.updateuid(message.from_user.id, username)
    userpanel(message)


def checkname(message):
    name = message.text
    if message.text == 'cancel':
        bot.reply_to(message, '''canceled''')
        return
    if len(name) < 5 or len(name) > 20:
        name = bot.send_message(message.from_user.id, '「📟」اسم بايد بيشتر از 5 و کمتر از 20 حرف باشد.!')
        bot.register_next_step_handler(name, checkname)
        return
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
    markup.add('cancel')
    username = bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                text='لطفا يوزرنيم خود را وارد كنيد...⌨️', reply_markup=markup)
    bot.register_next_step_handler(username, checkusername, name)
    return


def checkusername(message, name):
    username = message.text
    username = username.lower()
    if message.text == 'cancel':
        bot.reply_to(message, '''canceled''')
        return
    if len(username) < 5 or len(username) > 20:
        username = bot.send_message(message.from_user.id,
                                    'يوزرنيم بايد بيشتر از 5 و کمتر از 20 حرف باشد لطفا مجددا وارد نمایید.!')
        bot.register_next_step_handler(username, checkusername, name)
        return
    if '@' in username:
        username = bot.send_message(message.from_user.id,
                                    ' 🪧 يوزرنيم حاوی فاصله و [ @ ] نباشد لطفا مجددا وارد نمایید.!')
        bot.register_next_step_handler(username, checkusername, name)
        return
    if ' ' in username:
        username = bot.send_message(message.from_user.id,
                                    ' 🪧 يوزرنيم حاوی فاصله و [ @ ] نباشد لطفا مجددا وارد نمایید.!')
        bot.register_next_step_handler(username, checkusername, name)
        return
    all_users = wof_db.load_usernames()
    all_users = [x.lower() for x in all_users]
    if username in all_users:
        username = bot.send_message(message.from_user.id,
                                    '「👤」اين ايدی توسط شخص ديگر استفاده شده است لطفا يك ايدی ديگر وارد كنيد.!')
        bot.register_next_step_handler(username, checkusername, name)
        return
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
    markup.add('cancel')
    password = bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                text='لطفا رمز خود را وارد كنيد...⌨️', reply_markup=markup)
    bot.register_next_step_handler(password, checkpass, name, username)
    return


def checkpass(message, name, username):
    user_id = message.from_user.id
    password = message.text
    if message.text == 'cancel':
        bot.reply_to(message, '''canceled''')
        return
    if len(password) < 5 or len(password) > 20:
        password = bot.send_message(message.from_user.id, '「📟」رمـز بايد بيشتر از 5 و کمتر از 20 حرف باشد.!')
        bot.register_next_step_handler(password, checkpass, name, username)
        return
    if ' ' in password:
        password = bot.send_message(message.from_user.id, 'رمز حاوی فاصله نباشد.!')
        bot.register_next_step_handler(password, checkpass, name, username)
        return
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('「✔️」تـائـيـد', callback_data=f'useraccept {user_id}'),
               InlineKeyboardButton('ويـرايـش...📝', callback_data=f'userunaccept {user_id}'))
    bot.send_message(user_id, f'''𝚈𝚘𝚞𝚛 𝙽𝚊𝚖𝚎: `{name}`
𝚈𝚘𝚞𝚛 𝚄𝚜𝚎𝚛𝚗𝚊𝚖𝚎: `{username}`
𝚈𝚘𝚞𝚛 𝙿𝚊𝚜𝚜𝚠𝚘𝚛𝚍: `{password}`
آيا اطلاعات بالا را تاييد ميكنيد؟''', reply_markup=markup, parse_mode='markdown')
    wof_db.recording_info(user_id, name, username, password)


@bot.message_handler(regexp='addadmin', func=Filters.user(creators))
def add_admin(message):
    if not message.reply_to_message:
        return
    rep_id = message.reply_to_message.from_user.id
    wof_db.add_admin(rep_id)
    bot.reply_to(message,
                 f'✦| [{message.reply_to_message.from_user.first_name}](tg://user?id={rep_id}) با موفقیت به لیست ادمین ها اضافه شد✔️',
                 parse_mode='Markdown')


@bot.message_handler(regexp='remadmin', func=Filters.user(creators))
def rem_admin(message):
    if not message.reply_to_message:
        return
    rep_id = message.reply_to_message.from_user.id
    wof_db.rem_admin(rep_id)
    bot.reply_to(message,
                 f'✦| [{message.reply_to_message.from_user.first_name}](tg://user?id={rep_id}) با موفقیت از لیست ادمین ها حذف شد✔️',
                 parse_mode='Markdown')


@bot.message_handler(commands=['delplayer'], func=Filters.user(creators))
def add_admin(message):
    user_id = message.text.split(' ')[1]
    try:
        user_id = int(user_id)
    except:
        bot.reply_to(message, 'ایدی عددی را درست وارد کنید')
        return
    wof_db.del_tuple(user_id)
    wof_db.deactive(user_id)
    bot.reply_to(message, 'سیکشو زدم')


@bot.message_handler(commands=['addach'])
def adddach(message):
    user_id = message.from_user.id
    if not check_admin(user_id):
        bot.reply_to(message, 'شما ادمین ربات نیستید.!')
        return
    text = message.text
    text = text.split(" ")
    try:
        username = str(text[1]).lower()
        num = int(text[2])
    except:
        bot.reply_to(message, 'ورودی هارا درست وارد کنید')
        return
    load = wof_db.load_ach()
    length = load[0]
    if num > len(length) or num == 0:
        bot.reply_to(message, 'لطفا عدد اچیو را درست وارد کنید')
        return
    usrs = wof_db.load_usernames()
    if username not in usrs:
        bot.reply_to(message, '✖️كاربری با اين ايدی پیدا نشد.!')
        return
    prices = load[2]
    achh = load[1]
    wof_db.add_xp(username, prices[num - 1])
    userid = wof_db.load_uid(username)
    try:
        bot.send_message(userid[0], f'''🎨اچیو روزانه 
        ━━•✜•━━
{achh[num - 1]}
        ━━•✜•━━
به ارزش {prices[num - 1]} 𝚇𝚙🪙 را کسب کردید
        ━━•✜•━━
{get_hyperlink()}''', parse_mode='markdown', disable_web_page_preview=True)
    except:
        pass
    bot.reply_to(message, f'''🎨𝙰𝚌𝚑𝚒𝚟𝚎
        ━━•✜•━━
{achh[num - 1]}
        ━━•✜•━━
𝙰𝚍𝚍𝚎𝚍 𝚝𝚘 𝚝𝚑𝚎 {username}.!
{prices[num - 1]} 𝚇𝚙🪙 𝚊𝚍𝚍𝚎𝚍 𝚃𝚘 𝚝𝚑𝚎 `{username}` .!➕''', parse_mode='markdown')


@bot.message_handler(commands=['addachive'])
def addach(message):
    global prices
    global achives
    user_id = message.from_user.id
    if not check_admin(user_id):
        bot.reply_to(message, 'شما ادمین ربات نیستید.!')
        return
    text = message.text
    text = text.split(" ")
    try:
        username = str(text[1]).lower()
        num = int(text[2])
    except:
        bot.reply_to(message, 'ورودی هارا درست وارد کنید')
        return
    if num > 24 or num == 0:
        bot.reply_to(message, 'لطفا عدد اچیو را درست وارد کنید')
        return
    usrs = wof_db.load_usernames()
    if username not in usrs:
        bot.reply_to(message, '✖️كاربری با اين ايدی پیدا نشد.!')
        return
    achv = wof_db.load_achvs(username)
    a = achv.split(" ")
    if str(num) in a:
        bot.reply_to(message, 'كاربر اين اچيو را دارد')
        return
    if achv == '':
        achvs = f'{num}'
    else:
        achvs = f'{achv} {num}'
    wof_db.add_ach(username, achvs)
    wof_db.add_xp(username, prices[num - 1])
    userid = wof_db.load_uid(username)
    try:
        bot.send_message(userid[0], f'''🎨اچیو 
        ━━•✜•━━
{achives[num - 1]}
        ━━•✜•━━
برای شما به ارزش {prices[num - 1]} 𝚇𝚙🪙 باز شد
        ━━•✜•━━
{get_hyperlink()}''', parse_mode='markdown', disable_web_page_preview=True)
    except:
        pass
    bot.reply_to(message, f'''🎨𝙰𝚌𝚑𝚒𝚟𝚎 {num} 𝙰𝚍𝚍𝚎𝚍 𝚝𝚘 𝚝𝚑𝚎 {username}.!
{prices[num - 1]} 𝚇𝚙🪙 𝚊𝚍𝚍𝚎𝚍 𝚃𝚘 𝚝𝚑𝚎 {username}.!➕''')


@bot.message_handler(commands=['addtown'])
def addtown(message):
    user_id = message.from_user.id
    if not check_admin(user_id):
        bot.reply_to(message, 'شما ادمین ربات نیستید.!')
        return
    text = message.text
    text = text.split(" ")
    try:
        username = str(text[1]).lower()
        town = " ".join(text[2:])
    except:
        bot.reply_to(message, 'ورودی هارا درست وارد کنید')
        return
    usrs = wof_db.load_usernames()
    if username not in usrs:
        bot.reply_to(message, '✖️كاربری با اين ايدی پیدا نشد.!')
        return
    achv = wof_db.load_towns(username)
    a = achv.split(",")
    if str(town) in a:
        bot.reply_to(message, 'كاربر اين شـهـر را دارد.!🏭')
        return
    towns = f'{achv}{town},'
    wof_db.add_town(username, towns)
    bot.reply_to(message, f'🏡𝚌𝚒𝚝𝚢 {town} 𝚊𝚍𝚍𝚎𝚍 𝚃𝚘 𝚝𝚑𝚎 {username}.!')


@bot.message_handler(commands=['remtown'])
def remtown(message):
    user_id = message.from_user.id
    if not check_admin(user_id):
        bot.reply_to(message, 'شما ادمین ربات نیستید.!')
        return
    text = message.text
    text = text.split(" ")
    try:
        username = str(text[1]).lower()
        town = " ".join(text[2:])
    except:
        bot.reply_to(message, 'ورودی هارا درست وارد کنید')
        return
    usrs = wof_db.load_usernames()
    if username not in usrs:
        bot.reply_to(message, '✖️كاربری با اين ايدی پیدا نشد.!')
        return
    townn = wof_db.load_towns(username)
    a = townn.split(",")
    if str(town) not in a:
        bot.reply_to(message, '「🏠」كاربر اين شـهـر را ندارد.!')
        return
    towns = townn.replace(f'{town},', '')
    wof_db.add_town(username, towns)
    bot.reply_to(message, f'🏡𝙲𝚒𝚝𝚢 {town} 𝙳𝚎𝚌𝚛𝚎𝚊𝚜𝚎𝚍 𝚏𝚛𝚘𝚖 {username}.!')


@bot.message_handler(commands=['addxp'])
def addxp(message):
    user_id = message.from_user.id
    if not check_admin(user_id):
        bot.reply_to(message, 'شما ادمین ربات نیستید.!')
        return
    text = message.text
    text = text.split(" ")
    try:
        username = str(text[1]).lower()
        num = int(text[2])
    except:
        bot.reply_to(message, 'ورودی هارا درست وارد کنید')
        return
    usrs = wof_db.load_usernames()
    if username not in usrs:
        bot.reply_to(message, '✖️كاربری با اين ايدی پیدا نشد.!')
        return
    wof_db.add_xp(username, num)
    bot.reply_to(message, f'{num} 𝚇𝚙🪙 𝚊𝚍𝚍𝚎𝚍 𝚃𝚘 𝚝𝚑𝚎 {username}.!➕')


@bot.message_handler(commands=['subxp'])
def remxp(message):
    user_id = message.from_user.id
    if not check_admin(user_id):
        bot.reply_to(message, 'شما ادمین ربات نیستید.!')
        return
    text = message.text
    text = text.split(" ")
    try:
        username = str(text[1]).lower()
        num = int(text[2])
        num = -1 * num
    except:
        bot.reply_to(message, 'ورودی هارا درست وارد کنید')
        return
    usrs = wof_db.load_usernames()
    if username not in usrs:
        bot.reply_to(message, '✖️كاربری با اين ايدی پیدا نشد.!')
        return
    wof_db.add_xp(username, num)
    bot.reply_to(message, f'{num} 𝚇𝚙🪙 𝙳𝚎𝚌𝚛𝚎𝚊𝚜𝚎𝚍 𝚏𝚛𝚘𝚖 {username}.!➖')


@bot.message_handler(commands=['war'])
def recwar(message):
    if not check_admin(message.from_user.id):
        bot.reply_to(message, 'شما ادمین ربات نیستید.!')
        return
    chat_id = message.chat.id
    input = message.text.split(" ")
    str = " ".join(input[1:])
    towns = str.split(',')
    if len(towns) == 0 or len(towns) == 1:
        bot.reply_to(message, 'لطفا دستور را در فرمت درست وارد کنید')
        return
    attack_town = towns[:-2]
    attacked_town = towns[-2]
    result = towns[-1]
    attack_username = []
    for tw in attack_town:
        if wof_db.ret_usertown(tw):
            attack_username.append(wof_db.ret_usertown(tw))
    if len(attack_username) != len(attack_town):
        bot.reply_to(message, '''شهر برخی کاربران یافت نشد...🏢
        لطفا مجددا تلاش كنيد!''')
        return
    if wof_db.ret_usertown(attacked_town):
        attacked_username = wof_db.ret_usertown(attacked_town)
    else:
        bot.reply_to(message, '''هيچ كاربری اين شهر را ندارد...🏢
لطفا مجددا تلاش كنيد!''')
        return

    if result == 'win':
        result = True
    else:
        result = False
    attack_town = ",".join(attack_town)
    attack_username = ",".join(attack_username)
    wof_db.record_war(attack_username, attacked_username, attack_town, attacked_town, result)
    if result:
        status = '𝚆𝚒𝚗'
    else:
        status = '𝚕𝚘𝚜𝚎'
    bot.reply_to(message, f'''اتک با موفقيت ثبـت شد.⚔️
𝚄𝚜𝚎𝚛𝙽𝚊𝚖𝚎: `{attack_username}`
𝚃𝚘𝚠𝚗: `{attack_town}`
𝙰𝚝𝚝𝚊𝚌𝚔𝚎𝚍 𝚝𝚘 𝚞𝚜𝚎𝚛𝚗𝚊𝚖𝚎: `{attacked_username}`
𝚃𝚘𝚠𝚗: `{attacked_town}` 𝚊𝚗𝚍 {status} 𝚝𝚑𝚎 𝚠𝚊𝚛...✔️''',parse_mode='markdown')

    # markup = InlineKeyboardMarkup()
    # markup.add(
    #     InlineKeyboardButton('𝚆𝚒𝚗...🏆',
    #                          callback_data=f'winn {attack_username} {attack_town} {attacked_username} {attacked_town}'),
    #     InlineKeyboardButton('𝙻𝚘𝚜𝚎...🃏',
    #                          callback_data=f'losee {attack_username} {attack_town} {attacked_username} {attacked_town}'))
    # bot.send_message(chat_id, '↲ايا جنگ را بـرده يا بـاخـتـه؟', reply_to_message_id=message.message_id,
    #                  reply_markup=markup)


@bot.message_handler(commands=['tops'], func=Filters.group)
def top(message):
    bests = wof_db.get_best()
    numb = ['𝟏', '𝟐', '𝟑', '𝟒', '𝟓']
    usrs = bests[0]
    xps = bests[1]
    msg = '🪓  Tᴏᴘ ғɪᴠᴇ Pʟᴀʏᴇʀs\n\n'
    j = 0
    for i in usrs:
        msg += f'{numb[j]} `{i}` 🤹🏻‍♂️ 𝗟𝗲𝘃𝗲𝗹 `{set_level(xps[j])}` - 𝗫𝗽 `{xps[j]}`🪙\n'
        j += 1
    msg += f'''      ━━•✜•━━
{get_hyperlink()}'''
    bot.reply_to(message, msg, parse_mode='markdown', disable_web_page_preview=True)


@bot.message_handler(commands=['info'])
def info(message):
    if not check_admin(message.from_user.id):
        bot.reply_to(message, 'شما ادمین ربات نیستید.!')
        return
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        load = wof_db.load_information(user_id)
        if not load:
            bot.reply_to(message, 'این کاربر در ربات ثبت‌نام نشده است.!🤖')
            return
        name = load[0]
        username = load[1]
        towns = load[3].replace(',', ', ')
        achvs = load[4]
    else:
        try:
            text = message.text.split(' ')
            username = str(text[1])
            load = wof_db.load_info(username)
            if not load:
                bot.reply_to(message, 'این کاربر در ربات ثبت‌نام نشده است.!🤖')
                return
            name = load[0]
            user_id = load[1]
            towns = load[3].replace(',', ', ')
            achvs = load[4]
        except:
            bot.reply_to(message, '⌨️دستور را در فرمت درست وارد کنید.!')
            return
    msg = f'''⤷𝚄𝚜𝚎𝚛 𝙸𝚍: `{user_id}`
        ━━•✜•━━
⤷𝙽𝚊𝚖𝚎: `{name}`
        ━━•✜•━━
⤷𝚄𝚜𝚎𝚛𝚗𝚊𝚖𝚎: `{username}`
        ━━•✜•━━
⤷𝚃𝚘𝚠𝚗𝚜: `{towns}`
        ━━•✜•━━
⤷𝙰𝚌𝚑𝚒𝚟𝚎𝚜 𝙽𝚞𝚖𝚋𝚎𝚛: `{achvs}`\n\n'''
    msg += f'{get_hyperlink()}'
    bot.reply_to(message, msg, parse_mode='markdown', disable_web_page_preview=True)


@bot.message_handler(commands=['allplayers'])
def allp(message):
    if not check_admin(message.from_user.id):
        bot.reply_to(message, 'شما ادمین ربات نیستید.!')
        return
    all = wof_db.load_all()
    if not all:
        bot.reply_to(message, '💬پـلـیـری ثبت‌نام نکرده است.!')
        return
    msg = ''
    names = all[0]
    usernames = all[1]
    user_ids = all[2]
    towns = all[3]
    achivs = all[4]
    i = 0
    j = 0
    for name in names:
        if j == 25:
            msg += '🌍」  𝐕𝐢𝐯𝐚 𝐖𝐨𝐫𝐥𝐝 𝐨𝐧 𝐅𝐢𝐫𝗲...'
            bot.reply_to(message, msg, parse_mode='markdown')
            msg = ''
            j = 0
        msg += f'''📍{i + 1}
⤷𝙽𝚊𝚖𝚎: `{name}`
⤷𝚄𝚜𝚎𝚛𝙽𝚊𝚖𝚎: `{usernames[i]}`
⤷𝚄𝚜𝚎𝚛𝙸𝚍: `{user_ids[i]}`
⤷𝚃𝚘𝚠𝚗𝚜: `{towns[i].replace(',', ', ')}`
⤷𝙰𝚌𝚑𝚒𝚟𝚎𝚜 𝙽𝚞𝚖𝚋𝚎𝚛: `{achivs[i]}`
        ━━•✜•━━\n'''
        i += 1
        j += 1
    if msg:
        msg += f'{get_hyperlink()}'
        bot.reply_to(message, msg, parse_mode='markdown', disable_web_page_preview=True)


@bot.message_handler(commands=['wallet'], func=Filters.group)
def wallet(message):
    user_id = message.from_user.id
    if not wof_db.check_active(user_id):
        bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                         text='''شما با اکانتی وارد نشده‌اید. 
لطفا نسبت به ثبت‌نام یا ورود اقدام کنید!''',
                         reply_markup=start_markup())
        return
    username = wof_db.load_username(user_id)
    xp = wof_db.loadxp(username[0])
    bot.reply_to(message, f'''「📊」مـقـدار 𝚇𝙿 شمـا {xp[0]}
📇  𝐘𝐨𝐮𝐫 𝐋𝐞𝐯𝐞𝐥 {set_level(xp[0])}
        ━━•✜•━━
{get_hyperlink()}''', disable_web_page_preview=True, parse_mode='markdown')


@bot.message_handler(commands=['wofadminlist'], func=Filters.user(creators))
def adminlist(message):
    admins = wof_db.load_admins()
    if not admins:
        bot.reply_to(message, 'no admin')
        return
    msg = 'wof admins : '
    for admin in admins:
        try:
            x = bot.get_chat_member(chat_id=message.chat.id, user_id=admin)
            msg += f'\n[{x.user.first_name}](tg://user?id={x.user.id}) `{admin}`'
        except:
            wof_db.rem_admin(admin)
    bot.send_message(message.chat.id, msg, parse_mode='markdown')


@bot.message_handler(commands=['wofstats'], func=Filters.group)
def state(message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.from_user.id
    if not wof_db.check_active(user_id):
        bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                         text='''شما با اکانتی وارد نشده‌اید. 
لطفا نسبت به ثبت‌نام یا ورود اقدام کنید!''',
                         reply_markup=start_markup())
        return
    username = wof_db.load_username(user_id)
    data = wof_db.load_state(username[0])
    #     state = f'''
    # ⚔↵ ᴀᴛᴛᴀᴄᴋs `{data[0]}`
    # 💣↵ ᴡɪɴs `{data[1]}`
    # 🚬↵ ʟᴏssᴇs `{data[2]}`
    # 🗡↵ ᴅᴇғᴇɴsᴇs `{data[3]}`
    # 🛡✔️↵ sᴜᴄᴄᴇssғᴜʟ ᴅᴇғᴇɴsᴇs `{data[4]}`
    # 🛡✖️↵ ᴜɴsᴜᴄᴄᴇssғᴜʟ ᴅᴇғᴇɴsᴇs `{data[5]}`'''
    state = f'''
`{data[0]}` ᴀᴛᴛᴀᴄᴋs
`{data[1]}` ᴡɪɴs
`{data[2]}` ʟᴏssᴇs 
`{data[3]}` ᴅᴇғᴇɴsᴇs
`{data[4]}` sᴜᴄᴄᴇssғᴜʟ ᴅᴇғᴇɴsᴇs
`{data[5]}` ᴜɴsᴜᴄᴄᴇssғᴜʟ ᴅᴇғᴇɴsᴇs'''
    attackto = wof_db.get_attackto(username[0])
    usr = attackto[0][:3]
    num = attackto[1][:3]
    state += f'''\n「🤺 ᴘʟᴀʏᴇʀs ʏᴏᴜ ᴀᴛᴛᴀᴄᴋᴇᴅ ᴍᴏsᴛ'''
    j = 0
    for i in usr:
        state += f'''\n     `{num[j]}`    `{i}`'''
        j += 1
    attackfrom = wof_db.get_attackfrom(username[0])
    j = 0
    usr = attackfrom[0][:3]
    num = attackfrom[1][:3]
    state += f'''\n\n「🤺 ᴘʟᴀʏᴇʀs ᴡʜᴏ ᴀᴛᴛᴀᴄᴋᴇᴅ ʏᴏᴜ ᴍᴏsᴛ'''
    for i in usr:
        state += f'''\n     `{num[j]}`    `{i}`'''
        j += 1
    xp = wof_db.loadxp(username[0])
    state += f'\n📇  𝐋𝐞𝐯𝐞𝐥 `{set_level(xp[0])}`'
    state += f'''\n        ━━•✜•━━
{get_hyperlink()}'''
    bot.reply_to(message, state, parse_mode='markdown', disable_web_page_preview=True)


@bot.message_handler(commands=['attacks'], func=Filters.group)
def attks(message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.from_user.id
    if not wof_db.check_active(user_id):
        bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                         text='''شما با اکانتی وارد نشده‌اید. 
لطفا نسبت به ثبت‌نام یا ورود اقدام کنید!''',
                         reply_markup=start_markup())
        return
    username = wof_db.load_username(user_id)
    attackto = wof_db.get_attackto(username[0])
    usr = attackto[0]
    num = attackto[1]
    state = f'''「🤺 ᴘʟᴀʏᴇʀs `{username[0]}` ᴀᴛᴛᴀᴄᴋᴇᴅ ᴍᴏsᴛ'''
    j = 0
    for i in usr:
        state += f'''\n     `{num[j]}`    `{i}`'''
        j += 1
    state += f'''\n        ━━•✜•━━
{get_hyperlink()}'''
    bot.reply_to(message, state, parse_mode='markdown', disable_web_page_preview=True)


@bot.message_handler(commands=['attackedby'], func=Filters.group)
def attkby(message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.from_user.id
    if not wof_db.check_active(user_id):
        bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                         text='''شما با اکانتی وارد نشده‌اید. 
لطفا نسبت به ثبت‌نام یا ورود اقدام کنید!''',
                         reply_markup=start_markup())
    username = wof_db.load_username(user_id)
    attackfrom = wof_db.get_attackfrom(username[0])
    j = 0
    usr = attackfrom[0]
    num = attackfrom[1]
    state = f'''\n\n「🤺 ᴘʟᴀʏᴇʀs ᴡʜᴏ ᴀᴛᴛᴀᴄᴋᴇᴅ `{username[0]}` ᴍᴏsᴛ'''
    for i in usr:
        state += f'''\n     `{num[j]}`    `{i}`'''
        j += 1
    state += f'''\n        ━━•✜•━━
{get_hyperlink()}'''
    bot.reply_to(message, state, parse_mode='markdown', disable_web_page_preview=True)


@bot.message_handler(commands=['send'], func=Filters.group)
def send(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not check_admin(user_id):
        bot.reply_to(message, 'شما ادمین ربات نیستید.!')
        return
    input = message.text.split(" ")
    str = " ".join(input[1:])
    if str == '':
        bot.reply_to(message, '❕لطفا مقابل دستور متن موردنظر خود را وارد كنيد❕')
        return
    pm = bot.send_message(chat_id, 'در حال ارسال به پلیرها...')
    str += f'''
            ━━•✜•━━
{get_hyperlink()}'''
    all = wof_db.load_all()
    users = all[2]
    for id in users:
        try:
            bot.send_message(id, str, disable_web_page_preview=True, parse_mode='markdown')
        except:
            pass
    bot.edit_message_text('به تمام پلیرها ارسال شد', chat_id, pm.message_id)


@bot.message_handler(commands=['dailyachive'], func=Filters.group)
def dach(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not check_admin(user_id):
        bot.reply_to(message, 'شما ادمین ربات نیستید.!')
        return
    input = message.text.split(" ")
    str = " ".join(input[1:])
    if str == '':
        bot.reply_to(message, '❕لطفا مقابل دستور متن موردنظر خود را وارد كنيد❕')
        return
    str = str.replace('/dailyachive ', '')
    str = str.split('\n')
    wof_db.del_achvs()
    id = 1
    ach = '''𝖣𝖺𝗂𝗅𝗒 𝖠𝖼𝗁𝗂𝗏𝖾 𝖫𝗂𝗌𝗍🗞
        ━━•✜•━━\n'''
    for achive in str:
        achive = achive.split(' ')
        price = achive[len(achive) - 1:][0]
        dachive = ''
        for i in achive[:len(achive) - 1]:
            dachive += f'{i} '
        try:
            wof_db.add_dailyach(id, dachive, int(price))
            ach += f'''{dachive} 
    ( {price} 𝚇𝚙🪙 )
        ━━•✜•━━\n'''
            id += 1
        except:
            pass
    ach += get_hyperlink()
    bot.reply_to(message, ach, parse_mode='markdown', disable_web_page_preview=True)
    pm = bot.send_message(chat_id, 'در حال ارسال اچیوها به پلیرها...')
    all = wof_db.load_all()
    users = all[2]
    for id in users:
        try:
            bot.send_message(id, ach, disable_web_page_preview=True, parse_mode='markdown')
        except:
            pass
    bot.edit_message_text('به تمام پلیرها ارسال شد', chat_id, pm.message_id)


@bot.message_handler(commands=['delachive'], func=Filters.group)
def dach(message):
    user_id = message.from_user.id
    if not check_admin(user_id):
        bot.reply_to(message, 'شما ادمین ربات نیستید.!')
        return
    wof_db.del_achvs()
    bot.reply_to(message, 'خالی شد')


def get_hyperlink():
    name = '  🌍」  𝐕𝐢𝐯𝐚 𝐖𝐨𝐫𝐥𝐝 𝐨𝐧 𝐅𝐢𝐫𝐞...'
    link = 'https://t.me/World_On_Fire_Game'
    return f'[{name}]({link})'


def start_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('register 🤖 sign in', url='https://t.me/wofstate_bot?start=start'))
    return markup


@bot.message_handler(commands=['start'], func=Filters.private)
def start(message):
    user_id = message.from_user.id
    if wof_db.check_active(user_id):
        userpanel(message)
    else:
        reg(message)


@retry(wait=wait_fixed(2), stop=stop_after_attempt(10))
def poll():
    if __name__ == "__main__":
        try:
            bot.polling(none_stop=True, timeout=234)
            bot.send_message(134933697, 'wof state is up')
        except Exception as e:
            bot.send_message(chat_id=134933697, text=e)
            raise e


poll()

while True:
    pass
