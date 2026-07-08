from dataclasses import dataclass

from app.discovery.pipeline import discover_best_website_candidate


@dataclass
class WebsiteDiscoveryResult:
    website: str = ""
    confidence: float = 0.0
    reason: str = ""


def discover_official_website(business_name, town, state="CT"):
    best, score, scored = discover_best_website_candidate(
        business_name,
        town,
    )

    if best is None:
        return WebsiteDiscoveryResult(
            website="",
            confidence=0.0,
            reason="No suitable official website found",
        )

    return WebsiteDiscoveryResult(
        website=best.url,
        confidence=min(score / 100.0, 1.0),
        reason=f"Selected by discovery pipeline with score {score}",
    )
