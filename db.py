"""Competitive Torpedoes - Database connection and queries."""
import pandas as pd
from sqlalchemy import create_engine, text
from config import DATABASE_URL, TOP_N

_engine = None

def get_engine():
    global _engine
    if _engine is None and DATABASE_URL:
        _engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    return _engine


def get_platform_data(platform: str, top_n: int = TOP_N) -> dict:
    """
    Pull aggregated metrics for a platform's top N brands by LVI score.
    Adjust the SQL to match your actual table/column names.
    """
    engine = get_engine()
    if engine is None:
        return {}

    query = text("""
        SELECT
            COUNT(*)                            AS brand_count,
            :top_n                              AS top_n,
            AVG(lvi_score)                      AS lvi,
            AVG(search_score)                   AS search,
            AVG(reputation_score)               AS rep,
            AVG(social_score)                   AS social,
            AVG(ai_score)                       AS ai,
            AVG(google_claimed_pct)             AS gc,
            AVG(google_profile_complete_pct)    AS gpc,
            AVG(yelp_found_pct)                 AS yf,
            AVG(yelp_profile_complete_pct)      AS ypc,
            AVG(facebook_found_pct)             AS ff,
            AVG(facebook_profile_complete_pct)  AS fpc,
            AVG(google_review_count)            AS grc,
            AVG(yelp_review_count)              AS yrc,
            AVG(facebook_rec_count)             AS frc,
            AVG(google_rating)                  AS gr,
            AVG(yelp_rating)                    AS yr,
            AVG(facebook_rating)                AS fr,
            AVG(google_3pack_pct)               AS g3,
            AVG(google_local_page1_pct)         AS gl,
            AVG(yelp_page1_pct)                 AS yp,
            AVG(fb_followers)                   AS fbf,
            AVG(fb_engagements_per_post)        AS fbe,
            AVG(review_response_pct)            AS rrp,
            AVG(review_response_days)           AS rrd,
            AVG(engagement_rate)                AS er,
            AVG(waterfall_posting_pct)          AS wp
        FROM (
            SELECT *
            FROM brand_scores
            WHERE platform = :platform
            ORDER BY lvi_score DESC
            LIMIT :top_n
        ) sub
    """)

    with engine.connect() as conn:
        row = conn.execute(query, {"platform": platform, "top_n": top_n}).mappings().first()

    if row is None:
        return {}

    return {k: (round(float(v), 1) if v is not None else 0) for k, v in dict(row).items()}


def get_all_platforms() -> dict:
    engine = get_engine()
    if engine is None:
        return _fallback_data()

    platforms = ["SOCi", "Yext", "Birdeye", "Chatmeter",
                 "Reputation.com", "Uberall", "RioSEO"]
    result = {}
    for p in platforms:
        data = get_platform_data(p)
        if data:
            result[p] = data
    return result if result else _fallback_data()


def _fallback_data() -> dict:
    """Hard-coded fallback when DB is not connected (design mode)."""
    return {
        "SOCi":           {"brand_count":474,"top_n":50,"lvi":67.4,"search":77.7,"rep":58.6,"social":51.3,"ai":57.2,"gc":99.2,"gpc":96.8,"yf":95.1,"ypc":93.4,"ff":99.5,"fpc":94.7,"grc":698,"yrc":93,"frc":344,"gr":4.4,"yr":3.6,"fr":4.3,"g3":58,"gl":31,"yp":45,"fbf":2175,"fbe":441,"rrp":45,"rrd":2.3,"er":3.8,"wp":62},
        "Yext":           {"brand_count":391,"top_n":50,"lvi":67.6,"search":77.8,"rep":58.1,"social":54.5,"ai":56.8,"gc":96.1,"gpc":91.3,"yf":82.4,"ypc":85.7,"ff":98.9,"fpc":90.2,"grc":394,"yrc":37,"frc":76,"gr":4.2,"yr":3.1,"fr":3.8,"g3":20,"gl":9,"yp":21,"fbf":755,"fbe":253,"rrp":35,"rrd":4.1,"er":2.4,"wp":41},
        "Birdeye":        {"brand_count":57,"top_n":50,"lvi":52.0,"search":60.3,"rep":41.0,"social":34.6,"ai":44.2,"gc":94.3,"gpc":88.1,"yf":78.6,"ypc":80.2,"ff":96.4,"fpc":86.5,"grc":312,"yrc":28,"frc":58,"gr":4.1,"yr":3.0,"fr":3.9,"g3":15,"gl":5,"yp":16,"fbf":520,"fbe":180,"rrp":28,"rrd":5.6,"er":1.9,"wp":34},
        "Chatmeter":      {"brand_count":75,"top_n":50,"lvi":53.0,"search":65.1,"rep":45.5,"social":39.9,"ai":46.1,"gc":95.8,"gpc":90.4,"yf":80.1,"ypc":83.5,"ff":97.2,"fpc":88.9,"grc":358,"yrc":42,"frc":89,"gr":4.2,"yr":3.2,"fr":4.0,"g3":18,"gl":7,"yp":19,"fbf":680,"fbe":210,"rrp":32,"rrd":4.8,"er":2.1,"wp":38},
        "Reputation.com": {"brand_count":67,"top_n":50,"lvi":47.9,"search":60.4,"rep":40.6,"social":38.5,"ai":42.8,"gc":93.5,"gpc":87.2,"yf":76.3,"ypc":78.9,"ff":95.1,"fpc":84.3,"grc":285,"yrc":25,"frc":52,"gr":4.0,"yr":2.9,"fr":3.7,"g3":12,"gl":4,"yp":14,"fbf":430,"fbe":155,"rrp":25,"rrd":6.2,"er":1.6,"wp":29},
        "Uberall":        {"brand_count":48,"top_n":48,"lvi":50.0,"search":64.1,"rep":45.7,"social":46.9,"ai":43.5,"gc":95.1,"gpc":89.6,"yf":79.4,"ypc":82.1,"ff":97.0,"fpc":87.8,"grc":340,"yrc":35,"frc":72,"gr":4.1,"yr":3.1,"fr":3.9,"g3":16,"gl":6,"yp":18,"fbf":610,"fbe":195,"rrp":30,"rrd":5.1,"er":2.0,"wp":36},
        "RioSEO":         {"brand_count":5,"top_n":5,"lvi":61.3,"search":74.2,"rep":49.2,"social":51.8,"ai":52.6,"gc":97.4,"gpc":93.1,"yf":88.2,"ypc":89.7,"ff":98.6,"fpc":91.4,"grc":425,"yrc":55,"frc":128,"gr":4.3,"yr":3.4,"fr":4.1,"g3":28,"gl":15,"yp":30,"fbf":920,"fbe":310,"rrp":38,"rrd":3.5,"er":2.9,"wp":48},
    }
