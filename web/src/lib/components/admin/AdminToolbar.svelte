<script>
  import { Plus, Sun, Trash2, RefreshCw } from '@lucide/svelte';
import Spinner from '../Spinner.svelte';
export let hasMockLinks = false;
export let seeding = false;
export let deletingMock = false;
export let onseed;
export let ondeletemock;
export let onrefresh;
</script>
<div class="flex gap-2 flex-wrap items-center">
      <a href="/" class="inline-flex items-center gap-[0.4rem] py-[0.55rem] px-4 rounded-[10px] bg-brand-600 text-white text-[0.825rem] font-bold shadow-[0_2px_6px_rgba(27,_109,_81,_0.2)] transition-all duration-150 ease-[ease] hover:bg-brand-700">
        <Plus size={15} strokeWidth={2.5} aria-hidden="true" />
        Create Link
      </a>
      <!-- Seed Mock Links Button -->
      <button
        type="button"
        class="inline-flex items-center gap-[0.4rem] py-[0.55rem] px-[0.95rem] rounded-[10px] bg-[#eef2ff] border border-[#c7d2fe] text-[#4338ca] text-[0.825rem] font-bold cursor-pointer transition-all duration-150 ease-[ease] disabled:opacity-65 disabled:cursor-not-allowed hover:enabled:bg-[#e0e7ff] hover:enabled:text-[#3730a3] hover:enabled:border-[#a5b4fc]"
        on:click={onseed}
        disabled={seeding}
        title="Seed database with mock links (POST /api/seed/)"
      >
        {#if seeding}
          <Spinner size={12} />
          <span>Seeding...</span>
        {:else}
          <Sun size={15} aria-hidden="true" />
          <span>Seed Mock Links</span>
        {/if}
      </button>
      <!-- Delete Mock Links Button -->
      {#if hasMockLinks}
        <button
          type="button"
          class="inline-flex items-center gap-[0.4rem] py-[0.55rem] px-[0.95rem] rounded-[10px] bg-[#fef2f2] border border-[#fecaca] text-[#b91c1c] text-[0.825rem] font-bold cursor-pointer transition-all duration-150 ease-[ease] disabled:opacity-60 disabled:cursor-not-allowed hover:enabled:bg-[#fee2e2] hover:enabled:text-[#991b1b] hover:enabled:border-[#fca5a5]"
          on:click={ondeletemock}
          disabled={deletingMock}
          title="Delete all mock links from database (DELETE /api/seed/)"
        >
          {#if deletingMock}
            <Spinner size={12} />
            <span>Deleting...</span>
          {:else}
            <Trash2 size={15} aria-hidden="true" />
            <span>Delete Mock Links</span>
          {/if}
        </button>
      {/if}
      <button type="button" class="inline-flex items-center gap-[0.4rem] py-[0.55rem] px-[0.85rem] rounded-[10px] bg-white border border-line text-muted text-[0.825rem] font-semibold cursor-pointer transition-all duration-150 ease-[ease] hover:bg-[#f4f6f4] hover:text-ink" on:click={onrefresh} title="Refresh from backend">
        <RefreshCw size={15} aria-hidden="true" />
        <span>Refresh</span>
      </button>
    </div>
