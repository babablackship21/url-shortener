<script>
  import { Search, Link, Plus, Sun, ExternalLink, Trash2 } from '@lucide/svelte';
import CopyButton from '../CopyButton.svelte';
import Spinner from '../Spinner.svelte';
import { buildShortUrl } from '$lib/utils/urls.js';
import { formatDate } from '$lib/utils/dates.js';
import { filterLinks } from '$lib/utils/linkStats.js';
import { MOCK_SHORT_CODES } from '$lib/api/seed.js';
export let urls = [];
export let loading = false;
export let errorMessage = '';
export let seeding = false;
export let onseed;
export let onrefresh;
export let ondelete;
let searchQuery = '';
$: filteredUrls = filterLinks(urls, searchQuery);
$: hasMockLinks = urls.some(item => MOCK_SHORT_CODES.includes(item.short_code));
</script>
<div class="bg-white border border-line rounded-card overflow-hidden shadow-card">
    {#if urls.length > 0}
      <div class="py-4 px-5 border-b border-b-line flex flex-col gap-3 bg-[#fafbfa] sm:flex-row sm:items-center sm:justify-between">
        <div class="flex items-center gap-2 bg-white border border-[#d8dfdb] rounded-[10px] py-[0.45rem] px-3 w-full max-w-[360px]">
          <Search size={16} aria-hidden="true" />
          <input class="border-0 outline-none text-[0.825rem] w-full"
            type="text"
            bind:value={searchQuery}
            placeholder="Search by code or destination URL..."
          />
          {#if searchQuery}
            <button type="button" class="border-0 bg-transparent text-[#9ca3af] cursor-pointer" on:click={() => (searchQuery = '')}>✕</button>
          {/if}
        </div>
        <div class="flex items-center gap-[0.65rem]">
          {#if hasMockLinks}
            <span class="text-[0.675rem] font-bold py-0.5 px-[7px] rounded-md bg-[#eef2ff] text-[#4338ca] border border-[#c7d2fe] uppercase font-mono">Mock links active</span>
          {/if}
          <span class="text-xs text-muted">Showing {filteredUrls.length} of {urls.length} URLs</span>
        </div>
      </div>
    {/if}
    {#if loading}
      <!-- Loading State -->
      <div class="py-16 px-6 text-center text-muted flex flex-col items-center gap-3">
        <Spinner size={28} />
        <p>Loading URLs from PostgreSQL...</p>
      </div>
    {:else if errorMessage}
      <!-- Error State -->
      <div class="py-16 px-6 text-center text-muted flex flex-col items-center gap-3">
        <p>⚠️ {errorMessage}</p>
        <button type="button" class="py-[0.45rem] px-[0.85rem] rounded-lg bg-white border border-line text-[0.775rem] font-semibold cursor-pointer" on:click={onrefresh}>Retry Connection</button>
      </div>
    {:else if urls.length === 0}
      <!-- ============================================================== -->
      <!-- FEATURE 4: EMPTY STATE WHEN PROJECT JUST STARTED               -->
      <!-- ============================================================== -->
      <div class="py-18 px-6 text-center max-w-[520px] my-0 mx-auto flex flex-col items-center">
        <div class="w-17 h-17 rounded-[20px] bg-brand-50 border border-brand-100 text-brand-700 flex items-center justify-center mb-5">
          <Link size={40} strokeWidth={1.6} aria-hidden="true" />
        </div>
        <h3 class="text-xl font-extrabold text-ink">No shortened URLs yet</h3>
        <p class="text-[0.85rem] text-muted mt-2 leading-[1.5]">
          The project was just started and no URLs have been created in the database yet. You can create your first link, or use the <strong>Seed Mock Links</strong> API to populate sample data instantly.
        </p>
        <div class="flex items-center gap-3 mt-7 flex-wrap justify-center">
          <a href="/" class="inline-flex items-center gap-[0.4rem] py-3 px-[1.4rem] rounded-[10px] bg-brand-600 text-white text-[0.9rem] font-bold shadow-[0_2px_6px_rgba(27,_109,_81,_0.2)] transition-all duration-150 ease-[ease] hover:bg-brand-700">
            <Plus size={16} strokeWidth={2.5} aria-hidden="true" />
            Create Your First Link
          </a>
          <!-- Seed Mock Links CTA in Empty State -->
          <button
            type="button"
            class="inline-flex items-center gap-[0.4rem] py-3 px-[1.4rem] rounded-[10px] bg-[#eef2ff] border border-[#c7d2fe] text-[#4338ca] text-[0.9rem] font-bold cursor-pointer transition-all duration-150 ease-[ease] disabled:opacity-65 disabled:cursor-not-allowed hover:enabled:bg-[#e0e7ff] hover:enabled:text-[#3730a3] hover:enabled:border-[#a5b4fc]"
            on:click={onseed}
            disabled={seeding}
          >
            {#if seeding}
              <Spinner size={12} />
              <span>Seeding Mock Links...</span>
            {:else}
              <Sun size={16} aria-hidden="true" />
              <span>Seed Mock Links</span>
            {/if}
          </button>
          <button type="button" class="inline-flex items-center gap-[0.4rem] py-[0.55rem] px-[0.85rem] rounded-[10px] bg-white border border-line text-muted text-[0.825rem] font-semibold cursor-pointer transition-all duration-150 ease-[ease] hover:bg-[#f4f6f4] hover:text-ink" on:click={onrefresh}>
            Check Again
          </button>
        </div>
      </div>
    {:else if filteredUrls.length === 0}
      <!-- No search matches -->
      <div class="py-16 px-6 text-center text-muted flex flex-col items-center gap-3">
        <p>No links matching "{searchQuery}"</p>
        <button type="button" class="py-[0.45rem] px-[0.85rem] rounded-lg bg-white border border-line text-[0.775rem] font-semibold cursor-pointer" on:click={() => (searchQuery = '')}>Clear search</button>
      </div>
    {:else}
      <!-- Table View for Desktop -->
      <div class="overflow-x-auto">
        <table class="w-full border-collapse text-[0.825rem] text-left">
          <thead>
            <tr class="hover:bg-[#fafcfa]">
              <th class="py-[0.85rem] px-5 bg-[#f7f9f7] text-muted text-[0.725rem] font-bold uppercase tracking-[0.05em] border-b border-b-line">Short Code</th>
              <th class="py-[0.85rem] px-5 bg-[#f7f9f7] text-muted text-[0.725rem] font-bold uppercase tracking-[0.05em] border-b border-b-line">Original Destination URL</th>
              <th class="text-center py-[0.85rem] px-5 bg-[#f7f9f7] text-muted text-[0.725rem] font-bold uppercase tracking-[0.05em] border-b border-b-line">Clicks</th>
              <th class="py-[0.85rem] px-5 bg-[#f7f9f7] text-muted text-[0.725rem] font-bold uppercase tracking-[0.05em] border-b border-b-line">Created</th>
              <th class="text-right py-[0.85rem] px-5 bg-[#f7f9f7] text-muted text-[0.725rem] font-bold uppercase tracking-[0.05em] border-b border-b-line">Actions</th>
            </tr>
          </thead>
          <tbody>
            {#each filteredUrls as item (item.id || item.short_code)}
              <tr class="hover:bg-[#fafcfa]">
                <!-- Short code -->
                <td class="py-4 px-5 border-b border-b-[#f0f3f0] align-middle">
                  <div class="inline-flex items-center gap-[0.4rem]">
                    <span class="inline-block py-0.5 px-2 rounded-md bg-brand-50 border border-brand-100 text-brand-800 font-bold text-[0.8rem] font-mono">{item.short_code}</span>
                    {#if MOCK_SHORT_CODES.includes(item.short_code)}
                      <span class="text-[0.65rem] font-extrabold py-[1px] px-[5px] rounded bg-[#eef2ff] text-[#4f46e5] border border-[#c7d2fe] tracking-[0.04em] uppercase font-mono" title="Created via Seed Mock Links API">mock</span>
                    {/if}
                  </div>
                  <div class="text-[0.725rem] text-[#8b9d92] mt-[3px] font-mono">{buildShortUrl(item.short_code)}</div>
                </td>
                <!-- Original URL -->
                <td class="py-4 px-5 border-b border-b-[#f0f3f0] align-middle">
                  <a
                    href={item.original_url}
                    target="_blank"
                    rel="noreferrer"
                    class="inline-flex items-center gap-[0.35rem] text-ink max-w-[420px] overflow-hidden text-ellipsis whitespace-nowrap hover:text-brand-700 hover:underline font-mono"
                    title={item.original_url}
                  >
                    <span>{item.original_url}</span>
                    <ExternalLink size={13} aria-hidden="true" />
                  </a>
                </td>
                <!-- Clicks -->
                <td class="text-center py-4 px-5 border-b border-b-[#f0f3f0] align-middle">
                  <span class="inline-block py-[3px] px-2 rounded-full bg-[#f0f3f0] text-ink text-xs font-bold font-mono">{item.clicks || 0}</span>
                </td>
                <!-- Created Date -->
                <td class="whitespace-nowrap py-4 px-5 border-b border-b-[#f0f3f0] align-middle">
                  <span class="text-xs text-muted font-mono">{formatDate(item.created_at) || '—'}</span>
                </td>
                <!-- Actions -->
                <td class="text-right whitespace-nowrap py-4 px-5 border-b border-b-[#f0f3f0] align-middle">
                  <div class="inline-grid grid-cols-[3.5rem_4rem_2.25rem] gap-1 items-center">
                  <CopyButton text={buildShortUrl(item.short_code)} compact />
                  <a
                    href={buildShortUrl(item.short_code)}
                    target="_blank"
                    rel="noreferrer"
                    class="inline-flex items-center justify-center py-[0.4rem] px-[0.65rem] rounded-md text-xs font-bold border border-line bg-white text-muted cursor-pointer transition-all duration-150 ease-[ease] hover:text-ink hover:border-[#cbd5e1]"
                    title="Test redirect in new tab"
                  >
                    Test ↗
                  </a>
                  {#if item.can_delete === true}
                  <button
                    type="button"
                    class="inline-flex items-center justify-center py-[0.4rem] px-[0.65rem] rounded-md text-xs font-bold border border-line bg-white text-muted cursor-pointer transition-all duration-150 ease-[ease] hover:text-ink hover:border-[#cbd5e1] disabled:opacity-40 disabled:cursor-not-allowed hover:enabled:text-[#dc2626] hover:enabled:border-[#fecaca] hover:enabled:bg-[#fef2f2]"
                    title="Delete short link"
                    on:click={() => ondelete(item.short_code)}
                  >
                    <Trash2 size={14} aria-hidden="true" />
                  </button>
                  {/if}
                  </div>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}
  </div>
