from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import MemoryRule, MemoryRuleKeyword

async def find_matching_rules(
    db: AsyncSession,
    text: str
):
    text = text.lower()

    print("INPUT TEXT:", text)

    stmt = (
        select(MemoryRuleKeyword)
        .join(MemoryRule)
        .where(MemoryRule.is_active == True)
    )

    result = await db.execute(stmt)

    keywords = result.scalars().all()

    print("KEYWORDS COUNT:", len(keywords))

    matches = []

    for keyword in keywords:

        print("CHECKING:", keyword.keyword)

        if keyword.keyword.lower() in text:

            print("MATCH FOUND:", keyword.keyword)

            matches.append(
                {
                    "rule": keyword.rule,
                    "keyword": keyword.keyword,
                    "weight": keyword.weight,
                }
            )

    return matches

async def find_matching_rules1(
    db: AsyncSession,
    text: str
):
    text = text.lower()

    stmt = (
        select(MemoryRuleKeyword)
        .join(MemoryRule)
        .where(MemoryRule.is_active == True)
    )

    result = await db.execute(stmt)

    keywords = result.scalars().all()

    matches = []

    for keyword in keywords:

        if keyword.keyword.lower() in text:

            matches.append(
                {
                    "rule": keyword.rule,
                    "keyword": keyword.keyword,
                    "weight": keyword.weight,
                }
            )

    

    return matches

def choose_best_rule(matches):

    if not matches:
        return None

    scores = {}

    for item in matches:

        rule_id = item["rule"].id

        scores.setdefault(rule_id, {
            "rule": item["rule"],
            "score": 0
        })

        scores[rule_id]["score"] += item["weight"]

    return max(
        scores.values(),
        key=lambda x: x["score"]
    )

