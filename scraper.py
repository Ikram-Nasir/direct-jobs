SOURCES = [
    # --- UAE & MENA Tech / Super-Apps ---
    {"company": "Careem", "ats": "lever", "token": "careem"},
    {"company": "dubizzle Group", "ats": "lever", "token": "dubizzlegroup"},
    {"company": "Tabby", "ats": "ashby", "token": "tabby"},
    {"company": "Tamara", "ats": "lever", "token": "tamara"},
    {"company": "Kitopi", "ats": "lever", "token": "kitopi"},
    {"company": "Rain", "ats": "lever", "token": "rain"},
    {"company": "Mamo", "ats": "ashby", "token": "mamo"},
    {"company": "Huspy", "ats": "ashby", "token": "huspy"},

    # --- UAE Banking & Enterprise (Workday) ---
    {"company": "First Abu Dhabi Bank (FAB)", "ats": "workday", "tenant": "fab", "site_id": "FABCareers", "wd_num": "wd1"},
    {"company": "Majid Al Futtaim", "ats": "workday", "tenant": "maf", "site_id": "MAF_Careers", "wd_num": "wd3"},
    {"company": "Chalhoub Group", "ats": "workday", "tenant": "chalhoubgroup", "site_id": "ChalhoubCareers", "wd_num": "wd3"},

    # --- Pakistan Tech & Global Teams Hiring in PK ---
    {"company": "S&P Global (Islamabad/Global)", "ats": "workday", "tenant": "spgi", "site_id": "SPGI_Careers", "wd_num": "wd5"},
    {"company": "Bazaar Technologies", "ats": "lever", "token": "bazaartech"},
    {"company": "SadaPay", "ats": "lever", "token": "sadapay"},
    {"company": "Motive (KeepTruckin)", "ats": "greenhouse", "token": "gomotive"},
    {"company": "Turing", "ats": "lever", "token": "turing"},

    # --- High-Volume Remote-First Tech Companies ---
    {"company": "GitLab", "ats": "greenhouse", "token": "gitlab"},
    {"company": "Cloudflare", "ats": "greenhouse", "token": "cloudflare"},
    {"company": "Deel", "ats": "ashby", "token": "deel"},
    {"company": "Remote", "ats": "ashby", "token": "remote"},
    {"company": "Automattic", "ats": "greenhouse", "token": "automattic"},
    {"company": "Zapier", "ats": "greenhouse", "token": "zapier"},
    {"company": "Canonical", "ats": "greenhouse", "token": "canonical"},
    {"company": "Kraken", "ats": "lever", "token": "kraken"}
]

def post_to_telegram(new_jobs, existing_jobs):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_id:
        print("Telegram secrets not configured, skipping alert.")
        return

    existing_urls = {j["url"] for j in existing_jobs}
    brand_new = [j for j in new_jobs if j["url"] not in existing_urls][:10]

    if not brand_new:
        print("No brand-new jobs to post today.")
        return

    lines = ["🚨 *New Verified Direct Jobs Today*\n"]
    for j in brand_new:
        lines.append(f"• *{j['title']}* — {j['company']} ({j['location']})\n  [Apply Official Portal]({j['url']})\n")

    lines.append("🔎 Browse all verified roles: https://github.io")
    message = "\n".join(lines)

    url = f"https://telegram.org{bot_token}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }, timeout=15)
    print(f"Posted {len(brand_new)} new jobs to Telegram!")
