const LS_KEY = "poe:priceOverridesDivine"; // { [key]: number|null }

export function loadOverrides() {
    try { return JSON.parse(localStorage.getItem(LS_KEY) || "null") || {}; } catch { return {}; }
}
export function saveOverrides(map) {
    try { localStorage.setItem(LS_KEY, JSON.stringify(map)); } catch {}
}
export function setOverrideDivine(map, key, value) {
    const num = value === "" ? null : Number(value);
    map[key] = Number.isFinite(num) ? num : null;
    saveOverrides(map);
    return map;
}

/** Retourne la valeur à afficher pour un item/gemme en Divine, ou null si inconnue */
export function getDivinePrice(entry, overrides) {
    if (!entry) return null;
    if (overrides[entry._key] != null) return overrides[entry._key];
    if (entry.priceDivine != null) return entry.priceDivine; // pris du JSON d’entrée
    return null; // inconnu
}

/** Somme en Divine (ignore null) */
export function sumDivine(list, overrides) {
    return list.reduce((acc, e) => {
        const v = getDivinePrice(e, overrides);
        return acc + (v != null ? v : 0);
    }, 0);
}
