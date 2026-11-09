export function getLinkStats(urls) {
  return urls.reduce((stats, link) => ({
    totalClicks: stats.totalClicks + (link.clicks || 0),
    topPerformer: !stats.topPerformer || (link.clicks || 0) > (stats.topPerformer.clicks || 0) ? link : stats.topPerformer
  }), { totalClicks: 0, topPerformer: null });
}
export function filterLinks(urls, query) {
  const q = query.trim().toLowerCase();
  return urls.filter(link => link.short_code.toLowerCase().includes(q) || link.original_url.toLowerCase().includes(q));
}
