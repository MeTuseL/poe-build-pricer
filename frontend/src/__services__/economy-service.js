// Récupère la ligue active et le taux 1 Divine -> X Chaos via poe.ninja
const NINJA_BASE = "https://poe.ninja/api/data";
const TRADE_BASE = "https://www.pathofexile.com/api/trade/data";

const LS_KEY = "poe:divineRate";        // { league, chaosPerDivine, ts }
const TTL_MS = 30 * 60 * 1000;          // 30 min de cache

export async function getCurrentLeague() {
    const res = await fetch(`${TRADE_BASE}/leagues`, { credentials: "omit" });
    if (!res.ok) throw new Error("Failed to load leagues");
    const data = await res.json();
    const ids = (data?.result || data).map(x => x.id || x);
    // prend la première "challenge" non-HC si dispo, sinon Standard
    const challenge = ids.find(id => !/Standard|Hardcore/i.test(id));
    return challenge || "Standard";
}

export async function getDivineRate(leagueName) {
    // cache
    try {
        const cached = JSON.parse(localStorage.getItem(LS_KEY) || "null");
        if (cached && cached.league === leagueName && Date.now() - cached.ts < TTL_MS) {
            return cached.chaosPerDivine;
        }
    } catch {}

    const url = `${NINJA_BASE}/currencyoverview?league=${encodeURIComponent(leagueName)}&type=Currency`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to load poe.ninja");
    const json = await res.json();
    const line = (json?.lines || []).find(l => l.currencyTypeName === "Divine Orb");

    const chaosPerDivine =
        line?.chaosEquivalent ??
        (line?.receive?.value ? 1 / line.receive.value : null);

    if (!Number.isFinite(chaosPerDivine)) {
        throw new Error("Divine rate not found");
    }

    try {
        localStorage.setItem(LS_KEY, JSON.stringify({ league: leagueName, chaosPerDivine, ts: Date.now() }));
    } catch {}

    return chaosPerDivine;
}

export async function getLiveDivineRate() {
    const league = await getCurrentLeague();
    const chaosPerDivine = await getDivineRate(league);
    return { league, chaosPerDivine, divinePerChaos: 1 / chaosPerDivine };
}
