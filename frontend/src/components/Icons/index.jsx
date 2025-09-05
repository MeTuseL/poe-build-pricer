// composant interne
function Svg({ d, size = 18, ...props }) {
    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden
            {...props}
        >
            <path d={d} />
        </svg>
    );
}

// --- COMPOSANTS EXPORTÉS UNIQUEMENT ---
export const HelmetIcon = (p) => <Svg {...p} d="M4 12v-2a8 8 0 0 1 16 0v2m-9 8v-6h6v6M3 12h18M6 16h2" />;
export const ChestIcon  = (p) => <Svg {...p} d="M7 3h10l2 4v10l-5 4H10L5 17V7l2-4Z" />;
export const GlovesIcon = (p) => <Svg {...p} d="M6 8l2-2 3 3-3 3-2-2Zm5-1l2-2 3 3-2 2-3-3Z" />;
export const BootsIcon  = (p) => <Svg {...p} d="M6 3v9l-2 3h12l2-2-4-2V3H6Z" />;
export const SwordIcon  = (p) => <Svg {...p} d="M14 3l7 7-4 4-7-7V3H7L3 7l4 4" />;
export const ShieldIcon = (p) => <Svg {...p} d="M12 3l7 3v6c0 5-3.5 7-7 9-3.5-2-7-4-7-9V6l7-3Z" />;
export const RingIcon   = (p) => <Svg {...p} d="M12 7l3-3m-3 3l-3-3M5 14a7 7 0 1 0 14 0 7 7 0 0 0-14 0Z" />;
export const AmuletIcon = (p) => <Svg {...p} d="M12 2v4m-6 2a6 6 0 0 0 12 0" />;
export const BeltIcon   = (p) => <Svg {...p} d="M3 10h18v4H3zM7 10v4M17 10v4" />;
export const FlaskIcon  = (p) => <Svg {...p} d="M9 2h6M10 4h4l1 4 3 6-4 6H10L6 14l3-6 1-4Z" />;
export const JewelIcon  = (p) => <Svg {...p} d="M12 2l6 6-6 14L6 8l6-6Z" />;
export const GemIcon    = (p) => <Svg {...p} d="M12 2l8 8-8 12L4 10l8-8Zm0 0l-8 8h16L12 2Z" />;

// mapping interne
const iconMap = {
    Helmet: HelmetIcon,
    "Body Armour": ChestIcon,
    Gloves: GlovesIcon,
    Boots: BootsIcon,
    Weapon: SwordIcon,
    Offhand: ShieldIcon,
    Shields: ShieldIcon,
    Rings: RingIcon,
    Amulets: AmuletIcon,
    Belts: BeltIcon,
    Flask: FlaskIcon,
    Jewel: JewelIcon,
    Gem: GemIcon
};

// Composant utilitaire
export function ItemIcon({ type, className, size = 18 }) {
    const Comp = iconMap[type] || JewelIcon;
    return (
        <span className={className}>
      <Comp size={size} />
    </span>
    );
}
