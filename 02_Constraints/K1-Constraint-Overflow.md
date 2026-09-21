---
title: "K1 — Constraint Overflow and the Discontinuity Limit"
aliases: ["K1 Overflow", "LIMEN K1"]
created: 2026-09-21
updated: 2026-09-21
tags: [limen-vacui, constraint, numerics]
status: "canonical"
license: "CC-BY-4.0"
---

# K1 — Constraint Overflow and the Discontinuity Limit

## قید ۱ — سرریز قید و حد انفصال خلا

> **Structural Causal Chain (LIMEN):**
> تقارن کامل → انباشت قید → **سرریز** → مرز ساکت (حد انفصال) + پسین پتانسیل‌دار

دو قیدِ به‌ارث‌رسیده از SPUMA-VACUI اینجا نقش آغازین دارند: **حد انفصال خلا** (ثبت در آستانه، بدون گذار پیوسته) و **عدم پیوستگی بی‌نهایت تنش** (سقف g_max). روایت اضافه می‌کند: این قیدها آن‌قدر انباشته می‌شوند که **سرریز** کنند — و سرریز، تولد مرز است.

## Testable Content — T1 (اجرا شده)

`tools/limen_core.py::t1_silence_overflow` — رجیستر با سقف سرعت + خاموشی رانش:

| کمیت | مقدار |
|---|---|
| کسر ثبت‌شده (مرز ساکت) | **0.912** |
| نرخ ثبت پس از خاموشی (۱۰۰ گام آخر) | **0.00** — سکوت کامل |
| معکوس (نوفهٔ پایا، بدون خاموشی) | duty پایا ~0.95 — مرز ساکت **نمی‌سازد** (رد شد) |

**جملهٔ بسته:** سرریز یک رویداد زایشی متناهی است؛ «مرز» همان جایی است که حرکت متوقف شد — و پس از آن ساکت می‌ماند. [دقیق — دینامیک با جذب‌شونده]

## Related

- [[A1-Silent-Boundary]] — تفسیر
- [[Popcorn-Vacuum-Birth]] — پیامد پسین
- [[Companion-Bridge]] — همتای SPUMA
- [[MOC-LIMEN-VACUI]]
