<script>
import CopyButton from '$lib/components/CopyButton.svelte';
import Spinner from '$lib/components/Spinner.svelte';
import FeedbackBanner from '$lib/components/FeedbackBanner.svelte';
let loading = false;
let errorMessage = '';
import { onMount } from 'svelte';
import { getOriginalUrl } from '$lib/api/links.js';
import { extractSlug } from '$lib/utils/urls.js';
import { Search, ExternalLink } from '@lucide/svelte';
export let initialCode = '';
let retrieveInput = '';
let retrievedResult = null;
onMount(() => { if (initialCode) { retrieveInput = initialCode; handleRetrieve(); } });
  async function handleRetrieve() {
    errorMessage = '';
    retrievedResult = null;
    const code = extractSlug(retrieveInput);
    if (!code) {
      errorMessage = 'Please enter a valid short code or shortened URL.';
      return;
    }
    loading = true;
    try {
      const data = await getOriginalUrl(code);
      retrievedResult = data;
    } catch (err) {
      errorMessage = err.message || 'Could not find that shortened URL.';
    } finally {
      loading = false;
    }
  }
</script>
<FeedbackBanner message={errorMessage} />
      <!-- TAB 2: RETRIEVE -->
        <form on:submit|preventDefault={handleRetrieve} class="flex flex-col gap-5">
          <div>
            <label class="block text-[0.775rem] font-bold uppercase tracking-[0.06em] text-ink mb-[0.45rem]" for="retrieve-input">Enter Short Code or Shortened Link</label>
            <div class="flex items-center relative border border-[#d8dfdb] rounded-xl bg-[#fdfdfc] transition-all duration-150 ease-[ease] focus-within:border-brand-600 focus-within:shadow-[0_0_0_3px_rgba(27,_109,_81,_0.12)] focus-within:bg-white">
              <span class="flex items-center pl-[0.9rem] text-[#94a39b]">
                <Search size={18} />
              </span>
              <input class="flex-1 border-0 bg-transparent py-[0.85rem] px-[0.9rem] text-[0.925rem] text-ink outline-none min-w-0 placeholder:text-[#a3b0a8]"
                id="retrieve-input"
                type="text"
                bind:value={retrieveInput}
                placeholder="e.g. abc123 or http://localhost:8000/api/abc123"
                required
              />
              {#if retrieveInput}
                <button type="button" class="border-0 bg-[#e9eee9] text-[#556b5e] text-xs font-semibold py-[0.3rem] px-[0.6rem] mr-[0.6rem] rounded-md cursor-pointer" on:click={() => (retrieveInput = '')}>Clear</button>
              {/if}
            </div>
            <p class="mt-[0.4rem] text-xs text-[#798b81]">You can paste the entire short URL or just the code.</p>
          </div>
          <button type="submit" class="flex items-center justify-center gap-2 py-[0.9rem] px-6 rounded-xl border-0 bg-brand-600 text-white text-[0.925rem] font-bold cursor-pointer shadow-[0_4px_12px_rgba(27,_109,_81,_0.2)] transition-all duration-150 ease-[ease] disabled:opacity-65 disabled:cursor-not-allowed hover:enabled:bg-brand-700 hover:enabled:-translate-y-px hover:enabled:shadow-[0_6px_16px_rgba(27,_109,_81,_0.25)]" disabled={loading}>
            {#if loading}
              <Spinner />
              Looking up from Database...
            {:else}
              <ExternalLink size={16} aria-hidden="true" />
              Retrieve Original URL
            {/if}
          </button>
        </form>
        <!-- RETRIEVAL RESULT CARD -->
        {#if retrievedResult}
          <div class="mt-6 rounded-card py-5 px-6 bg-brand-50 border border-brand-100">
            <div class="flex items-center justify-between pb-3 border-b border-b-[rgba(27,_109,_81,_0.12)] mb-[0.85rem]">
              <div class="flex items-center gap-[0.45rem] font-bold text-[0.85rem] text-brand-800">
                <span class="w-5 h-5 rounded-full bg-brand-600 text-white flex items-center justify-center text-xs font-black">✓</span>
                <span>Original URL Retrieved</span>
              </div>
              <span class="text-[0.725rem] font-bold py-[3px] px-2 rounded-full bg-white border border-brand-100 text-brand-800 font-mono">Clicks: {retrievedResult.clicks}</span>
            </div>
            <div>
              <span class="block text-xs font-bold text-muted mb-[0.35rem]">Original Destination URL:</span>
              <div class="flex flex-col gap-2 min-[600px]:flex-row min-[600px]:items-center">
                <div class="flex-1 bg-white border border-brand-100 py-[0.65rem] px-[0.85rem] rounded-[10px] text-[0.85rem] text-brand-800 overflow-hidden text-ellipsis whitespace-normal select-all break-all font-mono">{retrievedResult.original_url}</div>
                <div class="flex gap-[0.35rem]">
                  <CopyButton text={retrievedResult.original_url} />
                  <a
                    href={retrievedResult.original_url}
                    target="_blank"
                    rel="noreferrer"
                    class="inline-flex items-center justify-center py-[0.65rem] px-4 rounded-[10px] text-[0.8rem] font-bold border border-line cursor-pointer transition-all duration-150 ease-[ease] bg-white text-ink hover:bg-[#f3f5f3]"
                  >
                    Visit Website ↗
                  </a>
                </div>
              </div>
              <div class="mt-3 pt-[0.65rem] border-t border-t-[rgba(27,_109,_81,_0.08)] flex items-center gap-[0.45rem] text-[0.775rem]">
                <span class="font-semibold text-muted">Short Code:</span>
                <span class="text-[0.7rem] py-0.5 px-1.5 rounded-md bg-white border border-brand-100 text-brand-700 font-mono">{retrievedResult.short_code}</span>
              </div>
            </div>
          </div>
        {/if}
