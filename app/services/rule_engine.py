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

    print("value1")
    print("KEYWORDS COUNT:", len(keywords))

    matches = []

    for keyword in keywords:

        print("CHECKING:", keyword.keyword)

        if keyword.keyword.lower() in text:

            print("MATCH FOUND:", keyword.keyword)

            print("RULE_ID:", keyword.rule_id)

            matches.append(
                {
                    "rule_id": str(keyword.rule_id),
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

        rule_id = item["rule_id"]

        scores.setdefault(
            rule_id,
            {
                "rule_id": rule_id,
                "score": 0
            }
        )

        scores[rule_id]["score"] += item["weight"]

    return max(
        scores.values(),
        key=lambda x: x["score"]
    )
    

