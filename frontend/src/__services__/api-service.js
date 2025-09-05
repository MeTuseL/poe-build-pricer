/**
 * Fetch pricing data from Django API with a PoB link.
 * @param {string} pobLink - The Path of Building link provided by the user.
 * @returns {Promise<any>} The parsed JSON response.
 */

export async function pricePoB(pobString) {
    const res = await fetch(`http://127.0.0.1:8000/api/pob/price`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ pob_string: pobString }),
    });

    if (!res.ok) {
        throw new Error(`Erreur API ${res.status}`);
    }
    return res.json();
}
