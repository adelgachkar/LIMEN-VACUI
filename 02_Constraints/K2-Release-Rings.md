---
title: "K2 — Constraint-Release Rings Around the Void"
aliases: ["K2 Rings", "Toroidal Release Ladder"]
created: 2026-09-21
updated: 2026-09-21
tags: [limen-vacui, constraint, rings, topological]
status: "canonical"
license: "CC-BY-4.0"
---

# K2 — Constraint-Release Rings Around the Void

## قید ۲ — ویدهای پیرامونی به نجیر حلقوی؛ پوش تراوایی حاصل

> **Structural Causal Chain (LIMEN):**
> وید مرکزی (قید رهاشده) → قیود همسایه به نجیر حلقوی درمی‌آیند → **نردبان حلقه‌ای** + پوش تراوایی

روایت تصویر پیوست (void-structured-axial-field.png) را چنین خواندنی می‌کند: قیدِ رهاشده در مرکز (محل سرریز) یک **عیب محوری آزاد** است؛ قیود پیرامونی که دیگر «هم‌ترازِ» تقارن کامل نیستند، به‌مثابه **نجیرهای حلقوی** (شکل‌های چنبره‌ای دور محور) ثبت می‌شوند. نردبان کمّیِ این ثبت:

$$\mathcal{C}_\alpha = \oint_{\alpha} \vec{A}\cdot d\vec{\ell} = n\,\Phi_0 \;\longrightarrow\; \text{پوش نجیر } k:\; \mathcal{C}_k \sim \frac{\Phi_0}{r_k^2},\quad r_k = k\,\Delta r$$

## Testable Content — T5 (اجرا شده)

`tools/limen_core.py::t5_rings` (n=8 پوش، شار دیپل واقعی روی کره‌های بسته):

| آزمون | نتیجه | حکم |
|---|---|---|
| نردبان پوش‌ها | C(r) ~ r^−2.00 (دقیقاً هدف) | نردبان گردش گسسته = آنالوگ C_α = n·Φ₀ [ساختاری] |
| افت خون رادیال | B_r ~ r^−3.00 | قطبی — بدون انتشار مونوپل [ساختاری] |
| **شار خالص از سطح بسته** (R=0.5, 1, 2) | **0.00، 0.00، 0.00** | رهایش، **حلقه می‌سازد نه برون‌ریز** — «پوش تراوایی» [ساختاری] |

نسبت‌های نردبان: C_k/C_1 = 1, 0.250, 0.111, … (1, ¼, 1/9) — پوش‌ها نجیرهای هم‌ریخت با قدرت 1/k².

## تصویر

![Structured void: axial chain, toroidal vector-potential rings, radial bleed, constraint region](../attachments/void-structured-axial-field.png)

## Related

- [[K1-Constraint-Overflow]] — خاستگاه وید مرکزی
- [[Companion-Bridge]] — نگاشت به SPUMA K2
- [[MOC-LIMEN-VACUI]]
