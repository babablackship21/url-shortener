<script>
  import { Link, TriangleAlert } from '@lucide/svelte';
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { getOriginalUrl } from '$lib/api/links.js';
  let loading = true;
  let notFound = false;
  let errorMessage = "";
  onMount(async () => {
    const code = $page.params.short_code;
    if (!code) {
      loading = false;
      notFound = true;
      return;
    }
    try {
      const data = await getOriginalUrl(code);
      if (data && data.original_url) {
        // Redirect to original destination
        window.location.replace(data.original_url);
      } else {
        loading = false;
        notFound = true;
      }
    } catch (error) {
      loading = false;
      notFound = error.status === 404;
      if (!notFound) errorMessage = "Unable to reach the destination lookup service. Please try again.";
    }
  });
</script>
{#if loading}
  <div class="min-h-[60vh] flex flex-col items-center justify-center text-center p-8">
    <div class="relative w-16 h-16 mb-6 flex items-center justify-center">
      <div class="absolute inset-0 border-4 border-brand-100 border-t-brand-600 rounded-full animate-resolver-spin"></div>
      <span class="text-brand-700 animate-link-pulse"><Link size={22} strokeWidth={2.2} aria-hidden="true" /></span>
    </div>
    <h2 class="text-2xl font-extrabold text-ink">Redirecting to destination...</h2>
    <p class="text-sm text-muted mt-[0.4rem]">Please wait while we look up your shortened URL.</p>
  </div>
{:else if errorMessage}
  <div class="min-h-[60vh] flex flex-col items-center justify-center text-center p-8" role="alert"><h1 class="text-[1.75rem] font-extrabold text-ink">Unable to look up link</h1><p class="text-[0.925rem] text-muted mt-2 max-w-[400px]">{errorMessage}</p><a href="/">Return home</a></div>
{:else if notFound}
  <main class="min-h-[60vh] flex flex-col items-center justify-center text-center p-8">
    <div class="w-16 h-16 rounded-[20px] bg-[#fef3c7] border border-[#fde68a] text-[#b45309] flex items-center justify-center mb-5">
      <TriangleAlert size={32} aria-hidden="true" />
    </div>
    <h1 class="text-[1.75rem] font-extrabold text-ink">Short URL not found</h1>
    <p class="text-[0.925rem] text-muted mt-2 max-w-[400px]">The shortened URL does not exist or may have expired.</p>
    <div class="flex gap-3 mt-7 flex-wrap justify-center">
      <a href="/" class="py-[0.65rem] px-[1.2rem] rounded-[10px] bg-brand-600 text-white text-[0.825rem] font-bold">Create a New Link &rarr;</a>
      <a href="/admin" class="py-[0.65rem] px-[1.2rem] rounded-[10px] bg-white border border-line text-muted text-[0.825rem] font-semibold">View All in Admin</a>
    </div>
  </main>
{/if}
