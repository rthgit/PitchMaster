"""Pitch Master — Template Library.

Pre-built pitch templates for common scenarios.
"""

TEMPLATES = {
    "seed_saas": {
        "name": "Seed SaaS",
        "description": "B2B SaaS at seed stage, pre-revenue or early revenue",
        "fields": {
            "company_name": "",
            "one_liner": "We help [customer] solve [problem] with [solution]",
            "problem": " Businesses waste [X hours/$Y] on [manual process]. Current solutions are [slow/expensive/complex].",
            "solution": "Our [platform/tool] automates [process] using [technology]. Users save [X%] time/cost.",
            "why_now": " [Trend/regulation] is creating a window. [Trigger event] is forcing adoption.",
            "market": " TAM: $[X]B ([growing Y% YoY]). SAM: $[X]M. We target [segment].",
            "business_model": " Subscription: $[X]/mo per seat. Unit economics: LTV $[X], CAC $[Y], payback [Z] months.",
            "traction": " [X] paying customers, $[Y] MRR, [Z]% MoM growth. [Key logo or pilot].",
            "team": " Founder: [Name], [relevant experience]. Co-founder: [Name], [technical background].",
            "ask": " Raising $[X]M seed. Use: [60%] product, [25%] sales, [15%] ops.",
        },
    },
    "series_a_b2c": {
        "name": "Series A B2C",
        "description": "Consumer product with strong traction, raising Series A",
        "fields": {
            "company_name": "",
            "one_liner": "[Product] for [audience] who want to [benefit]",
            "problem": " [X] million people struggle with [problem]. Existing options are [frustrating/limited].",
            "solution": " [Product] makes [benefit] effortless through [key feature]. [X] clicks vs [Y] steps.",
            "why_now": " [Cultural shift/technology change] is creating mass adoption moment.",
            "market": " TAM: $[X]B. [Z] million target users growing [Y%] annually.",
            "business_model": " Freemium: free tier + $[X]/mo premium. [X]% conversion rate, $[Y] ARPU.",
            "traction": " [X]M users, [Y]K DAU, [Z]% retention D30. Revenue $[X]K/mo, growing [Y%] MoM.",
            "team": " CEO: [Name], ex-[Big Tech]. CTO: [Name], built [previous product]. [X]M+ users scaled.",
            "ask": " Raising $[X]M Series A. Goal: [X]M users, $[Y]M ARR in 18 months.",
        },
    },
    "pre_seed_deep_tech": {
        "name": "Pre-Seed Deep Tech",
        "description": "Technical moat, research-heavy, pre-product",
        "fields": {
            "company_name": "",
            "one_liner": "We are building [technology] to solve [hard problem]",
            "problem": " [Domain] is stuck with [outdated approach]. The cost of [problem] is $[X]B/year.",
            "solution": " Our [novel approach/algorithm/material] achieves [X] improvement over state-of-art. [Patent/paper].",
            "why_now": " [Recent breakthrough] makes this possible for the first time. [Regulation] creates demand.",
            "market": " TAM: $[X]B in [industry]. Current solutions capture <[Y]% of need.",
            "business_model": " Licensing to [industry players] + SaaS platform for [end users].",
            "traction": " [X] papers published. [Y] patent applications. LOI from [Z] enterprise partners.",
            "team": " PhD team from [Top University]. [X] years combined research in [domain].",
            "ask": " Raising $[X]M pre-seed. 18-month runway to [milestone: prototype/first customer/patent].",
        },
    },
    "growth_marketplace": {
        "name": "Growth Marketplace",
        "description": "Marketplace with network effects, raising growth round",
        "fields": {
            "company_name": "",
            "one_liner": "The marketplace for [vertical] connecting [supply] with [demand]",
            "problem": " [Supply side] waste [X%] time finding customers. [Demand side] overpay by [Y%]. Middlemen take [Z]%. ",
            "solution": " Our marketplace uses [matching algorithm/trust system] to connect [supply] with [demand] instantly.",
            "why_now": " [Industry] is moving online post-[event]. [X] million [users] are underserved.",
            "market": " TAM: $[X]B GMV. We process $[Y]M GMV, taking [Z]% take rate.",
            "business_model": " Take rate: [X]% from supply side. [Y]% from demand side. Net revenue: $[Z]M.",
            "traction": " $[X]M GMV, [Y]K transactions/month, [Z]% MoM growth. NPS: [X]. LTV/CAC: [Y]x.",
            "team": " CEO: ex-[Marketplace unicorn]. COO: [X] years in [vertical]. Built [previous marketplace].",
            "ask": " Raising $[X]M Series B. Expand to [X] new cities, grow GMV to $[Y]M.",
        },
    },
}


def get_template(template_id: str) -> dict | None:
    """Get a template by ID."""
    return TEMPLATES.get(template_id)


def list_templates() -> list[dict]:
    """List all templates with id, name, description."""
    return [
        {"id": tid, "name": t["name"], "description": t["description"]}
        for tid, t in TEMPLATES.items()
    ]


def get_template_fields(template_id: str) -> dict:
    """Get the pre-filled fields for a template."""
    template = get_template(template_id)
    if not template:
        return {}
    return template.get("fields", {})
