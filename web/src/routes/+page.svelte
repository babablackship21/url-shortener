<script>
import { page } from '$app/stores';
import { Search, Plus } from '@lucide/svelte';
import CreateLinkForm from '$lib/components/links/CreateLinkForm.svelte';
import RetrieveLinkForm from '$lib/components/links/RetrieveLinkForm.svelte';
const queryCode = $page.url.searchParams.get('s') || $page.url.searchParams.get('code') || '';
let mode = queryCode ? 'retrieve' : 'create';
</script>
<svelte:head>
  <title>snip. — Shorten & Retrieve URLs</title>
</svelte:head>
<div class="max-w-[760px] my-0 mx-auto pt-12 px-5 pb-20 w-full">
  <!-- Hero Section -->
  <section class="text-center mb-9">
    <h1 class="text-[2.5rem] font-extrabold tracking-[-0.04em] leading-[1.15] text-ink">
      Shorten links, <span class="text-brand-600">expand reach.</span>
    </h1>
    <p class="mt-[0.65rem] text-[0.95rem] text-muted max-w-[520px] ml-auto mr-auto leading-[1.5]">
      Create clean short links, or look up and verify original destinations.
    </p>
  </section>
  <!-- Main Card -->
  <div class="bg-surface border border-line rounded-[20px] shadow-[0_10px_30px_rgba(0,_0,_0,_0.04),_0_1px_3px_rgba(0,_0,_0,_0.02)] overflow-hidden">
    <!-- Mode Switcher -->
    <div class="grid grid-cols-2 p-1.5 bg-[#f1f4f1] border-b border-b-line gap-1.5">
      <button
        type="button"
        class="flex items-center justify-center gap-[0.45rem] py-3 px-4 text-[0.85rem] font-bold border-0 rounded-xl cursor-pointer transition-all duration-150 ease-[ease] {(mode === 'create') ? ('text-brand-800 bg-white shadow-[0_2px_6px_rgba(0,_0,_0,_0.05)]') : ('text-muted bg-transparent hover:text-ink')}"
        on:click={() => { mode = 'create'; }}
      >
        <Plus size={16} />
        1. Create Short URL
      </button>
      <button
        type="button"
        class="flex items-center justify-center gap-[0.45rem] py-3 px-4 text-[0.85rem] font-bold border-0 rounded-xl cursor-pointer transition-all duration-150 ease-[ease] {(mode === 'retrieve') ? ('text-brand-800 bg-white shadow-[0_2px_6px_rgba(0,_0,_0,_0.05)]') : ('text-muted bg-transparent hover:text-ink')}"
        on:click={() => { mode = 'retrieve'; }}
      >
        <Search size={16} />
        2. Retrieve Original URL
      </button>
    </div>
    <div class="py-7 px-8">
      <div hidden={mode !== 'create'}><CreateLinkForm /></div>
      <div hidden={mode !== 'retrieve'}><RetrieveLinkForm initialCode={queryCode} /></div>
    </div>
  </div>
</div>
