<script>
import CopyButton from '$lib/components/CopyButton.svelte';
import Spinner from '$lib/components/Spinner.svelte';
import FeedbackBanner from '$lib/components/FeedbackBanner.svelte';
let loading = false;
let errorMessage = '';
import { createShortUrl } from '$lib/api/links.js';
import { normalizeUrl } from '$lib/utils/urls.js';
import { ChevronRight, Zap, Globe } from '@lucide/svelte';
let originalUrl = '';
let customCode = '';
let showCustomCode = false;
let createdResult = null;
  async function handleCreate() {
    errorMessage = '';
    createdResult = null;
    const targetUrl = normalizeUrl(originalUrl);
    if (!targetUrl) {
      errorMessage = 'Please enter a URL to shorten.';
      return;
    }
    loading = true;
    try {
      const data = await createShortUrl(targetUrl, showCustomCode ? customCode : null);
      createdResult = data;
      originalUrl = '';
      customCode = '';
    } catch (err) {
      errorMessage = err.message || 'Failed to create short URL.';
    } finally {
      loading = false;
    }
  }
</script>
<FeedbackBanner message={errorMessage} />
      <!-- TAB 1: CREATE -->
        <form on:submit|preventDefault={handleCreate} class="flex flex-col gap-5">
          <div>
            <label class="block text-[0.775rem] font-bold uppercase tracking-[0.06em] text-ink mb-[0.45rem]" for="long-url">Enter Destination Long URL</label>
            <div class="flex items-center relative border border-[#d8dfdb] rounded-xl bg-[#fdfdfc] transition-all duration-150 ease-[ease] focus-within:border-brand-600 focus-within:shadow-[0_0_0_3px_rgba(27,_109,_81,_0.12)] focus-within:bg-white">
              <span class="flex items-center pl-[0.9rem] text-[#94a39b]">
                <Globe size=18/>
              </span>
              <input class="flex-1 border-0 bg-transparent py-[0.85rem] px-[0.9rem] text-[0.925rem] text-ink outline-none min-w-0 placeholder:text-[#a3b0a8]"
                id="long-url"
                type="text"
                bind:value={originalUrl}
                placeholder="https://example.com/very/long/destination/url"
                required
              />
              {#if originalUrl}
                <button type="button" class="border-0 bg-[#e9eee9] text-[#556b5e] text-xs font-semibold py-[0.3rem] px-[0.6rem] mr-[0.6rem] rounded-md cursor-pointer" on:click={() => (originalUrl = '')}>Clear</button>
              {/if}
            </div>
            <p class="mt-[0.4rem] text-xs text-[#798b81]">Protocols like <code class="font-mono">https://</code> are auto-added if omitted.</p>
          </div>
          <!-- Custom Alias Toggle -->
          <div class="flex flex-col gap-[0.65rem]">
            <button
              type="button"
              class="inline-flex items-center gap-[0.35rem] text-[0.8rem] font-bold text-brand-700 bg-transparent border-0 cursor-pointer self-start"
              on:click={() => (showCustomCode = !showCustomCode)}
            >
              <span
                class="transition-transform duration-200 ease-[ease] {showCustomCode ? 'rotate-90' : 'rotate-0'}"
              >
                <ChevronRight size={14} />
              </span>
              {showCustomCode ? 'Hide custom alias' : 'Add custom alias / slug (optional)'}
            </button>
            {#if showCustomCode}
              <div class="bg-[#f8faf8] border border-line rounded-xl py-[0.85rem] px-4 flex flex-col gap-[0.35rem]">
                <label class="text-xs font-bold text-ink" for="custom-code">Custom Short Code</label>
                <div class="flex items-center border border-[#d8dfdb] rounded-lg bg-white overflow-hidden">
                  <span class="py-2 px-3 bg-[#eef2ee] text-[0.8rem] text-[#5d7065] border-r border-r-[#d8dfdb] font-mono">api/</span>
                  <input class="flex-1 border-0 py-2 px-3 text-sm outline-none"
                    id="custom-code"
                    type="text"
                    bind:value={customCode}
                    placeholder="my-cool-link"
                    minlength="4"
                    maxlength="16"
                  />
                </div>
                <p class="mt-[0.4rem] text-xs text-[#798b81]">4–16 alphanumeric characters, dashes, or underscores.</p>
              </div>
            {/if}
          </div>
          <button type="submit" class="flex items-center justify-center gap-2 py-[0.9rem] px-6 rounded-xl border-0 bg-brand-600 text-white text-[0.925rem] font-bold cursor-pointer shadow-[0_4px_12px_rgba(27,_109,_81,_0.2)] transition-all duration-150 ease-[ease] disabled:opacity-65 disabled:cursor-not-allowed hover:enabled:bg-brand-700 hover:enabled:-translate-y-px hover:enabled:shadow-[0_6px_16px_rgba(27,_109,_81,_0.25)]" disabled={loading}>
            {#if loading}
              <Spinner />
              Generating via Backend API...
            {:else}
              <Zap size={16} />
              Create Short URL
            {/if}
          </button>
        </form>
        <!-- CREATION RESULT CARD -->
        {#if createdResult}
          <div class="mt-6 rounded-card py-5 px-6 bg-brand-50 border border-brand-100">
            <div class="flex items-center justify-between pb-3 border-b border-b-[rgba(27,_109,_81,_0.12)] mb-[0.85rem]">
              <div class="flex items-center gap-[0.45rem] font-bold text-[0.85rem] text-brand-800">
                <span class="w-5 h-5 rounded-full bg-brand-600 text-white flex items-center justify-center text-xs font-black">✓</span>
                <span>Short Link Generated</span>
              </div>
              <span class="text-[0.7rem] py-0.5 px-1.5 rounded-md bg-white border border-brand-100 text-brand-700 font-mono">POST /api/url/</span>
            </div>
            <div>
              <span class="block text-xs font-bold text-muted mb-[0.35rem]">Your Shortened Link:</span>
              <div class="flex flex-col gap-2 min-[600px]:flex-row min-[600px]:items-center">
                <div class="flex-1 bg-white border border-brand-100 py-[0.65rem] px-[0.85rem] rounded-[10px] text-[0.85rem] text-brand-800 overflow-hidden text-ellipsis whitespace-nowrap select-all font-mono">{createdResult.short_url}</div>
                <div class="flex gap-[0.35rem]">
                  <CopyButton text={createdResult.short_url} />
                  <a
                    href={createdResult.short_url}
                    target="_blank"
                    rel="noreferrer"
                    class="inline-flex items-center justify-center py-[0.65rem] px-4 rounded-[10px] text-[0.8rem] font-bold border border-line cursor-pointer transition-all duration-150 ease-[ease] bg-white text-ink hover:bg-[#f3f5f3]"
                  >
                    Open ↗
                  </a>
                </div>
              </div>
              <div class="mt-3 pt-[0.65rem] border-t border-t-[rgba(27,_109,_81,_0.08)] flex items-center gap-[0.45rem] text-[0.775rem]">
                <span class="font-semibold text-muted">Destination:</span>
                <span class="text-ink overflow-hidden text-ellipsis whitespace-nowrap font-mono">{createdResult.original_url}</span>
              </div>
            </div>
          </div>
        {/if}
