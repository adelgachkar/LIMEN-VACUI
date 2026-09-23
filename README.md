# LIMEN-VACUI

**مرزِ خلأ** — A Conservative Genesis Narrative: the Silent Boundary, Constraint Overflow, and the Birth of the Arrow

> *LIMEN-VACUI* (Latin: *limen* = threshold/boundary, *vacui* = of the vacuum) is the third
> sister project of the family — after
> [Emergence-SDF-Vault](https://github.com/adelgachkar/Emergence-SDF-Vault) (phenomenology)
> and [SPUMA-VACUI](https://github.com/adelgachkar/SPUMA-VACUI) (foam genesis from two
> constraints). LIMEN asks the question **before** SPUMA:

> **چرا اصلاً مرزی هست که فوم در آن متولد شود؟**

## Core Claim

$$\text{LIMEN} = \underbrace{\text{سکوت}}_{\text{پیشا-مرز}} + \underbrace{K1}_{\text{سرریز قیدی از تقارن کامل}} + \underbrace{\vec{\mathcal{A}}}_{\text{پیکان پیشین}\to\text{پسین}} + \underbrace{K3}_{\text{بالشتک بالانس}} + \underbrace{K4}_{\text{زایش پاپ‌کورنی}} + \underbrace{K2}_{\text{حلقه‌های رهایش}}$$

- **A1 — مرز، محل سکوت است:** پس از سرریز، «مرز» همان جایی است که حرکت متوقف شد — و ساکت می‌ماند.
- **A2 — سرریز از تقارن کامل:** نه پیشینی نه پسینی؛ سرریز خودش پیشین به پسین را **می‌سازد**.
- **A3 — پیکان از ثبت:** قانونِ میکروسکوپی بی‌پیکان است؛ پیکان زمان اثرِ کتابداریِ یک‌سویه است («خراش روی عینک»).
- **K1 — حد انفصال:** سرریز رویدادی متناهی است، نه نشتی پیوسته.
- **K2 — حلقه‌های رهایش:** قید رهاشده به‌جای برون‌ریز، نجیرهای حلقوی می‌سازد (شار خالص صفر).
- **Balancer — بالشتک:** تورم بی‌نهایت در مدل کشسانیِ محدود-سرعت ممنوع است.
- **Popcorn — زایش خلا:** نوفهٔ خاموش + حد انفصال → هسته‌زایی پراکندهٔ کاواک‌ها.

## Executed Verification (tools/limen_core.py)

| Test | Result | Label |
|---|---|---|
| T1 silent boundary | registered fraction 0.912; late registration rate 0.00 (SILENT) | exact |
| T2 arrow from undirected law | monotone record, 100% of steps; +0.4369 reg/site/step | test-specified |
| T3 balancer | front speed 0.75 ≤ c = 1.00; equalization to exactly −0.25 | exact |
| T4 popcorn | mean cavity 2.34 cells (= SPUMA K1, cross-check consistent) | structural |
| T5 release rings | C(r) ~ r^−2.00 ladder; net dipole flux 0.00 through closed spheres | structural |

## وضعیت معرفتی

این یک **سازهٔ روایی-کمّی** است، نه فیزیک تثبیت‌شده: T1/T2 دینامیک ثبت سبک‌سازی‌شده‌اند (قانون واقعی پیشا-مرز از عنوان‌سازی، غیرگفتنی است)؛ T3 گزارهٔ دقیق کشسانی است؛ T4 نقشهٔ K1 اسپوما را به ارث می‌برد؛ T5 نردبان استاتیک چندقطبی است؛ T7 شکل‌گیری همان نردبان را از دینامیک رهایش سبک‌سازی‌شده اشتقاق می‌کند (سقف‌ها = ظرفیت سطح؛ سلول‌های ثبت‌شده = فتیل‌های اشباع). هیچ ادعایی کیهان‌شناسی رصدی را حل نمی‌کند. MIT.

**سه‌گانهٔ معرفتی هر عدد — هر عدد این مخزن دقیقاً در یکی از سه کلاس است:**

| کلاس | معنا | اعداد این مخزن |
|---|---|---|
| **هندسهٔ بسته** | ریاضیِ دقیق *مدل*؛ روی کاغذ اشتقاق‌پذیر؛ **نه** کمیتی اندازه‌گیری‌شدهٔ طبیعت | کران جبههٔ کشسانی c=1 و سرعت 0.75≤c؛ تراز متعادل دقیق −0.25؛ توان نردبان چندقطبی −2؛ فرم نردبان C_α = n·Φ₀ |
| **شبیه‌سازی‌های خودمان** | بازتولیدپذیر در `tools/`؛ هیچ اعتبارسنجی تجربی بیرونی ندارند | T1 (p_f=0.912)، T2 (+0.4369 ثبت/سایت/گام)، T4 (میانگین کاواک 2.34 سلول)، T7 (ترتیب درون‌به‌بیرون، k*~t^0.65، بستار 0.0245 rad)، پل (p_f=0.2992، R∈[0.90,0.98])، رجیستر واحد (هویت p_U، فروپاشی دوز RMSE 0.0050) |
| **پدیدهٔ تجربی واقعی** | در جهان واقعی توسط دیگران اندازه‌گیری شده | **هیچ‌کدام — این مخزن هیچ ورودی تجربی ندارد**؛ نزدیک‌ترین لنگر واقعی (آزمایش گرافن) در SPUMA-VACUI زندگی می‌کند و فقط سازوکار K2 آن‌جا را لنگر می‌زند، نه این روایت را |
