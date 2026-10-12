// Meta Ad Library — extract advertisers, durations and the prices they charge.
//
// Paste into mcp__claude-in-chrome__javascript_tool on an Ad Library results
// page. Returns one summary object. Nothing here is specific to a product.
//
// Two things this exists to get right:
//   1. COUNT ADVERTISERS, NOT ADS. A single advertiser routinely runs ten ads
//      from one creative ("10 ads use this creative and text"), so an ad count
//      overstates competition roughly tenfold.
//   2. READ THE PRICES OUT OF THE AD COPY. What a competing dropshipper
//      charges is the real comparable — they carry our cost structure.
//
// Caveat the caller must apply: Meta's India filter leaks. `is_targeted_country`
// reasserts itself as false, so results include ads merely visible in India.
// Always eyeball `names` and drop national brands, marketplace affiliates
// (Meesho/Flipkart/Wishlink creators) and copy aimed at another country.
(() => {
  const t = document.body.innerText;

  const rows = t.split(/Library ID:\s*/).slice(1).map(chunk => {
    const body = (chunk.split(/See (?:ad|summary) details/)[1] || '');
    const prices = [...new Set(
      [...body.matchAll(/₹\s?([\d,]{3,6})|Rs\.?\s?([\d,]{3,6})/g)]
        .map(m => +(m[1] || m[2]).replace(/,/g, ''))
    )].filter(p => p >= 249 && p <= 9999);   // drop phone numbers and pincodes
    return {
      id:   (chunk.match(/^(\d+)/) || [])[1],
      date: (chunk.match(/Started running on ([0-9]{1,2} \w+ 20[0-9]{2})/) || [])[1],
      adv:  body.trim().split('\n')[0].trim(),
      reuse:(chunk.match(/(\d+) ads use this creative/) || [])[1],
      prices,
    };
  }).filter(r => r.id && r.adv);

  const advertisers = [...new Set(rows.map(r => r.adv))];
  const prices = rows.flatMap(r => r.prices).sort((a, b) => a - b);
  const dates  = rows.map(r => r.date).filter(Boolean)
                     .map(d => new Date(d)).sort((a, b) => a - b);
  const months = dates.length
    ? Math.round((Date.now() - dates[0]) / 2.63e9) : null;

  return {
    resultHeader : (t.match(/~?[\d,]+\s+results/) || [])[0],  // inflated; ignore
    ads          : rows.length,
    advertisers  : advertisers.length,                         // THIS is the number
    names        : advertisers.slice(0, 12),
    oldestAd     : dates[0] ? dates[0].toISOString().slice(0, 10) : null,
    longestRunMonths : months,
    priceLow     : prices[0] ?? null,
    priceMedian  : prices.length ? prices[Math.floor(prices.length / 2)] : null,
    priceHigh    : prices[prices.length - 1] ?? null,
    distinctPrices : [...new Set(prices)],
    adsWithPrice : rows.filter(r => r.prices.length)
                       .slice(0, 8)
                       .map(r => ({ id: r.id, adv: r.adv, date: r.date, prices: r.prices })),
  };
})();
