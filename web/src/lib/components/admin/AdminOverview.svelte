<script>
import KpiCard from '../KpiCard.svelte';
import { Activity, Link, Star } from '@lucide/svelte';
import { getLinkStats } from '$lib/utils/linkStats.js';
export let urls = [];
$: ({ totalClicks, topPerformer } = getLinkStats(urls));
</script>
<section>
  <h2 class="text-2xl font-bold">Dashboard Overview</h2>
  <div class="grid grid-cols-1 gap-4 my-6 mx-0 sm:grid-cols-3">
    <!-- Total Links -->
    <KpiCard
      label="Total Links"
      value={urls.length}
      description={urls.length === 0
        ? 'Project just started'
        : 'Active records in database'}
    >
      {#snippet icon()}
      <Link size={16} />
      {/snippet}
    </KpiCard>
    <!-- Total Clicks -->
    <KpiCard
      tone="amber" label="Total Clicks Recorded"
      value={totalClicks}
      description="Cumulative clicks / lookups"
    >
      {#snippet icon()}
        <Activity size={16} strokeWidth={2} />
      {/snippet}
    </KpiCard>
    <!-- Top Performer -->
    <KpiCard
      tone="purple" label="Top Performer"
      value={topPerformer
        ? `${topPerformer.short_code} (${topPerformer.clicks})`
        : 'None yet'}
      description={topPerformer
        ? topPerformer.original_url
        : 'No click activity yet'}
      muted={!topPerformer}
    >
      {#snippet icon()}
        <Star size={16} strokeWidth={2} />
      {/snippet}
    </KpiCard>
  </div>
</section>
