"""Competitive Torpedoes - Database connection and queries."""
import streamlit as st
from sqlalchemy import create_engine, text, bindparam
from config import DATABASE_URL, TOP_N

_engine = None


def get_engine():
    global _engine
    if _engine is None and DATABASE_URL:
        _engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    return _engine


def _safe(v):
    return round(float(v), 1) if v is not None else 0


def _safe_pct(v):
    """Convert a 0-1 decimal percentage from the DB to a 0-100 display value."""
    return round(float(v) * 100, 1) if v is not None else 0


# Metric keys that the DB stores as 0-1 decimals and must be multiplied by 100
_PCT_100 = frozenset({
    "gc", "gpc", "g3", "gl",
    "yf", "ypc", "yp",
    "ff", "fpc",
    "rrp", "fr", "wp",
})


@st.cache_data(ttl=3600)
def get_platform_data(platform: str, top_n: int = TOP_N) -> dict:
    engine = get_engine()
    if engine is None:
        return _fallback_data().get(platform, {})

    with engine.connect() as conn:
        # Step 1 — top N brand IDs by LVI score
        top_rows = conn.execute(text("""
            SELECT s.brand_id
            FROM lvi_2026_brand_scores s
            JOIN lvi_2026_brand_platform_list p ON s.brand_id = p.brandid
            WHERE (p.platform_a = :platform OR p.platform_b = :platform)
              AND s.marketing_overall_total_score IS NOT NULL
            ORDER BY ((s.marketing_overall_total_score + s.performance_score) / 2) DESC
            LIMIT :top_n
        """), {"platform": platform, "top_n": top_n}).fetchall()

        if not top_rows:
            return {}

        brand_ids = [r[0] for r in top_rows]

        # Total brand count for this platform (no LIMIT)
        total_count = conn.execute(text("""
            SELECT COUNT(*)
            FROM lvi_2026_brand_scores s
            JOIN lvi_2026_brand_platform_list p ON s.brand_id = p.brandid
            WHERE (p.platform_a = :platform OR p.platform_b = :platform)
              AND s.marketing_overall_total_score IS NOT NULL
        """), {"platform": platform}).scalar()

        # Step 2 — granular metric averages for those brand IDs
        metrics_q = (
            text("""
                SELECT
                    AVG(google_perct_profile_claimed_and_linked)                AS gc,
                    AVG(google_avg_perct_profile_complete)                      AS gpc,
                    AVG(google_perct_in_3_pack)                                 AS g3,
                    AVG(google_perct_ranking_1st_page_organic)                  AS gl,
                    AVG(yelp_perct_profile_claimed)                             AS yf,
                    AVG(yelp_avg_perct_profile_complete)                        AS ypc,
                    AVG(yelp_perct_ranking_1st_page)                            AS yp,
                    AVG(facebook_perct_profile_found)                           AS ff,
                    AVG(facebook_avg_perct_profile_complete)                    AS fpc,
                    AVG(google_avg_rating)                                      AS gr,
                    AVG(google_avg_review_count)                                AS grc,
                    AVG(google_avg_perct_overall_review_response)               AS rrp,
                    AVG(google_avg_review_response_time_in_days_last_12_months) AS rrd,
                    AVG(yelp_avg_rating)                                        AS yr,
                    AVG(yelp_avg_review_count)                                  AS yrc,
                    AVG(facebook_avg_perct_positive_recommendations)            AS fr,
                    AVG(facebook_avg_recommendations)                           AS frc,
                    AVG(facebook_avg_page_followers)                            AS fbf,
                    AVG(facebook_avg_engagments_per_post)                       AS fbe,
                    AVG(facebook_perct_waterfall_posting)                       AS wp
                FROM lvi_2026_brand_metrics
                WHERE brandid IN :ids
            """).bindparams(bindparam("ids", expanding=True))
        )
        metrics_row = conn.execute(metrics_q, {"ids": brand_ids}).mappings().first()

        # Step 3 — composite score averages for those brand IDs
        scores_q = (
            text("""
                SELECT
                    AVG((marketing_overall_total_score + performance_score) / 2) AS lvi,
                    AVG(search_score)       AS search,
                    AVG(reputation_score)   AS rep,
                    AVG(social_score)       AS social,
                    AVG(ai_overall_score)   AS ai
                FROM lvi_2026_brand_scores
                WHERE brand_id IN :ids
            """).bindparams(bindparam("ids", expanding=True))
        )
        scores_row = conn.execute(scores_q, {"ids": brand_ids}).mappings().first()

    metrics = {
        k: (_safe_pct(v) if k in _PCT_100 else _safe(v))
        for k, v in dict(metrics_row).items()
    } if metrics_row else {}
    scores = {k: _safe(v) for k, v in dict(scores_row).items()} if scores_row else {}

    fbf = metrics.get("fbf", 0)
    fbe = metrics.get("fbe", 0)
    er  = round(fbe / fbf * 100, 1) if fbf > 0 else 0

    return {
        "count": int(total_count or 0),
        "topN":  len(brand_ids),
        **scores,
        **metrics,
        "er": er,
    }


@st.cache_data(ttl=3600)
def get_benchmark() -> dict:
    """Return benchmark averages mapped to the same short keys used in platform data."""
    engine = get_engine()
    if engine is None:
        return {}

    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT * FROM lvi_2026_brand_benchmark_overall_transposed")
        ).mappings().first()

    if row is None:
        return {}

    d = dict(row)
    fbf = _safe(d.get("facebook_avg_page_followers"))
    fbe = _safe(d.get("facebook_avg_engagments_per_post"))

    return {
        "gc":  _safe_pct(d.get("google_perct_profile_claimed_and_linked")),
        "gpc": _safe_pct(d.get("google_avg_perct_profile_complete")),
        "g3":  _safe_pct(d.get("google_perct_in_3_pack")),
        "gl":  _safe_pct(d.get("google_perct_ranking_1st_page_organic")),
        "yf":  _safe_pct(d.get("yelp_perct_profile_claimed")),
        "ypc": _safe_pct(d.get("yelp_avg_perct_profile_complete")),
        "yp":  _safe_pct(d.get("yelp_perct_ranking_1st_page")),
        "ff":  _safe_pct(d.get("facebook_perct_profile_found")),
        "fpc": _safe_pct(d.get("facebook_avg_perct_profile_complete")),
        "gr":  _safe(d.get("google_avg_rating")),
        "grc": _safe(d.get("google_avg_review_count")),
        "rrp": _safe_pct(d.get("google_avg_perct_overall_review_response")),
        "rrd": _safe(d.get("google_avg_review_response_time_in_days_last_12_months")),
        "yr":  _safe(d.get("yelp_avg_rating")),
        "yrc": _safe(d.get("yelp_avg_review_count")),
        "fr":  _safe_pct(d.get("facebook_avg_perct_positive_recommendations")),
        "frc": _safe(d.get("facebook_avg_recommendations")),
        "fbf": fbf,
        "fbe": fbe,
        "wp":  _safe_pct(d.get("facebook_perct_waterfall_posting")),
        "er":  round(fbe / fbf * 100, 1) if fbf > 0 else 0,
    }


@st.cache_data(ttl=3600)
def get_all_platforms() -> dict:
    engine = get_engine()
    if engine is None:
        return _fallback_data()

    result = {}
    for platform in ["SOCi", "Yext", "Birdeye", "Chatmeter", "Reputation.com", "Uberall", "RioSEO"]:
        data = get_platform_data(platform)
        if data:
            result[platform] = data

    return result if result else _fallback_data()


def _fallback_data() -> dict:
    """Hard-coded fallback when DB is not connected (design mode)."""
    return {
        "SOCi":           {"count":474,"topN":50,"lvi":67.4,"search":77.7,"rep":58.6,"social":51.3,"ai":57.2,"gc":99.2,"gpc":96.8,"yf":95.1,"ypc":93.4,"ff":99.5,"fpc":94.7,"grc":698,"yrc":93,"frc":344,"gr":4.4,"yr":3.6,"fr":4.3,"g3":58,"gl":31,"yp":45,"fbf":2175,"fbe":441,"rrp":45,"rrd":2.3,"er":3.8,"wp":62},
        "Yext":           {"count":391,"topN":50,"lvi":67.6,"search":77.8,"rep":58.1,"social":54.5,"ai":56.8,"gc":96.1,"gpc":91.3,"yf":82.4,"ypc":85.7,"ff":98.9,"fpc":90.2,"grc":394,"yrc":37,"frc":76,"gr":4.2,"yr":3.1,"fr":3.8,"g3":20,"gl":9,"yp":21,"fbf":755,"fbe":253,"rrp":35,"rrd":4.1,"er":2.4,"wp":41},
        "Birdeye":        {"count":57,"topN":50,"lvi":52.0,"search":60.3,"rep":41.0,"social":34.6,"ai":44.2,"gc":94.3,"gpc":88.1,"yf":78.6,"ypc":80.2,"ff":96.4,"fpc":86.5,"grc":312,"yrc":28,"frc":58,"gr":4.1,"yr":3.0,"fr":3.9,"g3":15,"gl":5,"yp":16,"fbf":520,"fbe":180,"rrp":28,"rrd":5.6,"er":1.9,"wp":34},
        "Chatmeter":      {"count":75,"topN":50,"lvi":53.0,"search":65.1,"rep":45.5,"social":39.9,"ai":46.1,"gc":95.8,"gpc":90.4,"yf":80.1,"ypc":83.5,"ff":97.2,"fpc":88.9,"grc":358,"yrc":42,"frc":89,"gr":4.2,"yr":3.2,"fr":4.0,"g3":18,"gl":7,"yp":19,"fbf":680,"fbe":210,"rrp":32,"rrd":4.8,"er":2.1,"wp":38},
        "Reputation.com": {"count":67,"topN":50,"lvi":47.9,"search":60.4,"rep":40.6,"social":38.5,"ai":42.8,"gc":93.5,"gpc":87.2,"yf":76.3,"ypc":78.9,"ff":95.1,"fpc":84.3,"grc":285,"yrc":25,"frc":52,"gr":4.0,"yr":2.9,"fr":3.7,"g3":12,"gl":4,"yp":14,"fbf":430,"fbe":155,"rrp":25,"rrd":6.2,"er":1.6,"wp":29},
        "Uberall":        {"count":48,"topN":48,"lvi":50.0,"search":64.1,"rep":45.7,"social":46.9,"ai":43.5,"gc":95.1,"gpc":89.6,"yf":79.4,"ypc":82.1,"ff":97.0,"fpc":87.8,"grc":340,"yrc":35,"frc":72,"gr":4.1,"yr":3.1,"fr":3.9,"g3":16,"gl":6,"yp":18,"fbf":610,"fbe":195,"rrp":30,"rrd":5.1,"er":2.0,"wp":36},
        "RioSEO":         {"count":5,"topN":5,"lvi":61.3,"search":74.2,"rep":49.2,"social":51.8,"ai":52.6,"gc":97.4,"gpc":93.1,"yf":88.2,"ypc":89.7,"ff":98.6,"fpc":91.4,"grc":425,"yrc":55,"frc":128,"gr":4.3,"yr":3.4,"fr":4.1,"g3":28,"gl":15,"yp":30,"fbf":920,"fbe":310,"rrp":38,"rrd":3.5,"er":2.9,"wp":48},
    }
