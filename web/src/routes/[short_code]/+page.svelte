<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { getOriginalUrl } from '$lib/api.js';

  let loading = true;
  let notFound = false;

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
    } catch {
      loading = false;
      notFound = true;
    }
  });
</script>

{#if loading}
  <div class="redirect-loading">
    <div class="spinner-container">
      <div class="spinner"></div>
      <svg class="link-icon" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
        <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
        <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
      </svg>
    </div>
    <h2>Redirecting to destination...</h2>
    <p>Please wait while we look up your shortened URL.</p>
  </div>
{:else if notFound}
  <main class="not-found-container">
    <div class="warning-icon">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
        <line x1="12" y1="9" x2="12" y2="13"></line>
        <line x1="12" y1="17" x2="12.01" y2="17"></line>
      </svg>
    </div>
    <h1>Short URL not found</h1>
    <p>The shortened URL does not exist or may have expired.</p>
    <div class="actions">
      <a href="/" class="btn-home">Create a New Link &rarr;</a>
      <a href="/admin" class="btn-admin">View All in Admin</a>
    </div>
  </main>
{/if}

<style>
  .redirect-loading {
    min-height: 60vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
  }

  .spinner-container {
    position: relative;
    width: 64px;
    height: 64px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .spinner {
    position: absolute;
    inset: 0;
    border: 4px solid var(--emerald-100);
    border-top-color: var(--emerald-600);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  .link-icon {
    color: var(--emerald-700);
    animation: pulse 1.5s infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.9); }
  }

  .redirect-loading h2 {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--text-main);
  }

  .redirect-loading p {
    font-size: 0.875rem;
    color: var(--text-muted);
    margin-top: 0.4rem;
  }

  .not-found-container {
    min-height: 60vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
  }

  .warning-icon {
    width: 64px;
    height: 64px;
    border-radius: 20px;
    background: #fef3c7;
    border: 1px solid #fde68a;
    color: #b45309;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.25rem;
  }

  .not-found-container h1 {
    font-size: 1.75rem;
    font-weight: 800;
    color: var(--text-main);
  }

  .not-found-container p {
    font-size: 0.925rem;
    color: var(--text-muted);
    margin-top: 0.5rem;
    max-width: 400px;
  }

  .actions {
    display: flex;
    gap: 0.75rem;
    margin-top: 1.75rem;
    flex-wrap: wrap;
    justify-content: center;
  }

  .btn-home {
    padding: 0.65rem 1.2rem;
    border-radius: 10px;
    background: var(--emerald-600);
    color: #fff;
    font-size: 0.825rem;
    font-weight: 700;
  }

  .btn-admin {
    padding: 0.65rem 1.2rem;
    border-radius: 10px;
    background: #ffffff;
    border: 1px solid var(--border-light);
    color: var(--text-muted);
    font-size: 0.825rem;
    font-weight: 600;
  }
</style>

