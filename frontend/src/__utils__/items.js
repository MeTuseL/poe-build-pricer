export function isGem(entry) {
    return Boolean(
        entry?.gemId ||
        entry?.skillId ||
        entry?.nameSpec ||
        entry?._kind === "gem" ||
        entry?.type === "Gem" ||
        entry?.level != null
    );
}

export function getItemTitleVariant(entry) {
    if (isGem(entry)) return "Gem";
    const r = String(entry?.rarity || "").toUpperCase();
    if (r === "UNIQUE") return "Unique";
    if (r === "RARE")   return "Rare";
    if (r === "MAGIC")  return "Magic";
    return "Normal";
}
