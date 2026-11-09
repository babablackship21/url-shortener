<script>
  let { label, value, description, icon, muted = false, tone = 'emerald' } = $props();
  const tones = {
    emerald: 'bg-brand-50 text-brand-700',
    amber: 'bg-[#fef3c7] text-[#b45309]',
    purple: 'bg-[#f3e8ff] text-[#7e22ce]'
  };
</script>
<div class="rounded-card border border-line bg-surface p-5 shadow-card">
  <div class="flex items-center justify-between">
    <span class="text-[0.725rem] font-bold uppercase tracking-[0.06em] text-muted">{label}</span>
    {#if icon}
      <div class="flex size-8 items-center justify-center rounded-lg {tones[tone] || tones.emerald}">
        {@render icon()}
      </div>
    {/if}
  </div>
  <div class="mt-2 font-mono text-[1.85rem] font-extrabold {muted ? 'text-[#9ca3af]' : 'text-ink'}">{value}</div>
  <p class="mt-1 text-xs text-muted">{description}</p>
</div>
