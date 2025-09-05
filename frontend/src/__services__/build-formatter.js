// Formatte le PoB en sections prêtes pour l'UI (équipements, jewels, gems, flasks…)

const keyOf = (it, extra = "") => {
    const uid = it?.properties?.find(p => p.name === "Unique ID")?.values || "";
    return [
        it.type || "",
        it.subType || "",
        it.name || it.itemBase || "",
        uid,
        extra
    ].join("|");
};

const tag = (it) => ({
    ...it,
    _key: it._key || keyOf(it)
});

export function formatBuild(pob) {
    const data = pob?.data || {};
    const items = Array.isArray(data.items) ? data.items.map(tag) : [];

    // --- Classes
    const classes = {
        characterClass: data.class || "",
        ascendancy: data.ascendClass || ""
    };

    // --- Armour (slots)
    const armour = {
        helmet: null,
        bodyArmour: null,
        gloves: null,
        boots: null
    };

    // --- Weapons
    const weapons = {
        mainHand: null,
        offHand: null
    };

    // --- Jewellery (belts / amulets / rings)
    const jewellery = {
        belt: null,
        amulet: null,
        rings: []
    };

    // --- Flasks
    const flasks = [];

    // --- Jewels (arbre / timeless / cluster / abyss…)
    const jewels = {
        base: [],
        timeless: [],
        abyss: [],
        cluster: { large: [], medium: [], small: [] }
    };

    // --- Parcours des items
    for (const it of items) {
        const t = it.type || "";
        const st = it.subType || "";

        // Armour slots
        if (t === "Armour") {
            if (st === "Helmet" && !armour.helmet) armour.helmet = it;
            else if (st === "Body Armour" && !armour.bodyArmour) armour.bodyArmour = it;
            else if (st === "Gloves" && !armour.gloves) armour.gloves = it;
            else if (st === "Boots" && !armour.boots) armour.boots = it;
            continue;
        }

        // Weapons / Offhand
        if (t === "Weapon") {
            if (!weapons.mainHand) weapons.mainHand = it;
            else if (!weapons.offHand) weapons.offHand = it;
            continue;
        }
        if (t === "Offhand") {
            if (!weapons.offHand) weapons.offHand = it;
            continue;
        }

        // Jewellery
        if (t === "Jewelry") {
            if (st === "Belts" && !jewellery.belt) jewellery.belt = it;
            else if (st === "Amulets" && !jewellery.amulet) jewellery.amulet = it;
            else if (st === "Rings") jewellery.rings.push(it);
            continue;
        }

        // Flasks (dans ton JSON: type/subType null => on filtre via rarity MAGIC + nom contient "Flask")
        if (!t && (it.rarity === "MAGIC" || /Flask/i.test(it.name || ""))) {
            flasks.push(it);
            continue;
        }

        // Jewels d’arbre
        if (t === "Jewel") {
            if (st === "Timeless Jewel") jewels.timeless.push(it);
            else if (st === "Abysmal Jewel") jewels.abyss.push(it);
            else if (st === "Cluster Jewel") {
                // Essai de taille via texte
                const base = (it.itemBase || "").toLowerCase();
                if (base.includes("large")) jewels.cluster.large.push(it);
                else if (base.includes("medium")) jewels.cluster.medium.push(it);
                else jewels.cluster.small.push(it);
            } else {
                jewels.base.push(it);
            }
            continue;
        }
    }

    // --- Gems (via data.skills)
    const gemsBySlot = {};
    const skills = Array.isArray(data.skills) ? data.skills : [];
    for (const s of skills) {
        const slot = s.slot || "Unknown";
        if (!gemsBySlot[slot]) gemsBySlot[slot] = [];
        const gems = Array.isArray(s.gems) ? s.gems : [];
        gems.forEach((g, idx) => {
            gemsBySlot[slot].push(tag({
                ...g,
                _key: g._key || keyOf({ type: "Gem", subType: slot, name: g.nameSpec }, idx),
                name: g.nameSpec,
                rarity: g.Corrupted ? "UNIQUE" : "MAGIC",
                priceDivine: g.priceDivine ?? null
            }));
        });
    }

    // --- Equipment list (Weapons + Armour + Jewellery)
    const equipment = []
        .concat(weapons.mainHand ? [weapons.mainHand] : [])
        .concat(weapons.offHand ? [weapons.offHand] : [])
        .concat(armour.helmet ? [armour.helmet] : [])
        .concat(armour.bodyArmour ? [armour.bodyArmour] : [])
        .concat(armour.gloves ? [armour.gloves] : [])
        .concat(armour.boots ? [armour.boots] : [])
        .concat(jewellery.belt ? [jewellery.belt] : [])
        .concat(jewellery.amulet ? [jewellery.amulet] : [])
        .concat(jewellery.rings);

    // Tag every element with _key if missing
    const withKey = (arr) => arr.map(tag);

    return {
        classes,
        armour,
        weapons,
        jewellery,
        equipment: withKey(equipment),
        flasks: withKey(flasks),
        jewels: {
            base: withKey(jewels.base),
            abyss: withKey(jewels.abyss),
            timeless: withKey(jewels.timeless),
            cluster: {
                large: withKey(jewels.cluster.large),
                medium: withKey(jewels.cluster.medium),
                small: withKey(jewels.cluster.small)
            }
        },
        gemsBySlot
    };
}
