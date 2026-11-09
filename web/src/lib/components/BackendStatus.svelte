<script>
import { onMount } from 'svelte';
  import { checkHealth } from '$lib/api/health.js';
  let backendHealthy = false;
  let checking = true;
  onMount(async () => {
    try {
      const res = await checkHealth();
      backendHealthy = res.database === 'connected';
    } catch {
      backendHealthy = false;
    } finally {
      checking = false;
    }
  });
</script>
<div class="hidden items-center gap-[0.35rem] py-[0.3rem] px-[0.6rem] rounded-full bg-[#f4f6f4] border border-line text-[0.72rem] font-semibold text-muted sm:flex" title={backendHealthy ? "Connected to FastAPI Backend" : "Connecting to Backend /api"}>
        <span class="size-[7px] rounded-full {checking ? 'bg-[#9ca3af]' : backendHealthy ? 'bg-[#10b981] shadow-[0_0_0_2px_rgba(16,185,129,0.2)]' : 'bg-[#f59e0b]'}"></span>
        <span>{backendHealthy ? "API Ready" : (checking ? "Connecting..." : "API Standby")}</span>
      </div>
