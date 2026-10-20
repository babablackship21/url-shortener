<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { createShortUrl, getOriginalUrl, extractSlug } from '$lib/api.js';

  let mode = 'create'; // 'create' | 'retrieve'

  // Create Mode state
  let originalUrl = '';
  let customCode = '';
  let showCustomCode = false;
  let createdResult = null;

  // Retrieve Mode state
  let retrieveInput = '';
  let retrievedResult = null;

  // UI state
  let loading = false;
  let errorMessage = '';
  let copiedKey = null;

  onMount(() => {
    // Check if query param ?s=code or ?code=code was passed
    const queryCode = $page.url.searchParams.get('s') || $page.url.searchParams.get('code');
    if (queryCode) {
      mode = 'retrieve';
      retrieveInput = queryCode;
      handleRetrieve();
    }
  });

  async function handleCreate() {
    errorMessage = '';
    createdResult = null;

    let targetUrl = originalUrl.trim();
    if (!targetUrl) {
      errorMessage = 'Please enter a URL to shorten.';
      return;
    }

    // Auto prepend https:// if missing
    if (!/^[a-zA-Z][a-zA-Z0-9+.-]*:\/\//.test(targetUrl)) {
      targetUrl = `https://${targetUrl}`;
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

  async function copyText(text, key) {
    try {
      await navigator.clipboard.writeText(text);
      copiedKey = key;
      setTimeout(() => (copiedKey = null), 2000);
    } catch {
      alert('Unable to copy to clipboard.');
    }
  }
</script>

<svelte:head>
  <title>snip. — Shorten & Retrieve URLs</title>
</svelte:head>

<div class="page-container">
  <!-- Hero Section -->
  <section class="hero">
    <!-- <div class="eyebrow">
      <span class="pulse-dot"></span>
      FASTAPI + SVELTEKIT MVP
    </div> -->
    <h1 class="hero-title">
      Shorten links, <span class="highlight">expand reach.</span>
    </h1>
    <p class="hero-subtitle">
      Create clean short links, or look up and verify original destinations.
    </p>
  </section>

  <!-- Main Card -->
  <div class="card">
    <!-- Mode Switcher -->
    <div class="mode-tabs">
      <button
        type="button"
        class="tab-btn"
        class:active={mode === 'create'}
        on:click={() => { mode = 'create'; errorMessage = ''; }}
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        1. Create Short URL
      </button>

      <button
        type="button"
        class="tab-btn"
        class:active={mode === 'retrieve'}
        on:click={() => { mode = 'retrieve'; errorMessage = ''; }}
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        2. Retrieve Original URL
      </button>
    </div>

    <div class="card-body">
      <!-- Error Banner -->
      {#if errorMessage}
        <div class="error-banner">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <div class="error-content">
            <strong>Error</strong>
            <span>{errorMessage}</span>
          </div>
        </div>
      {/if}

      <!-- TAB 1: CREATE -->
      {#if mode === 'create'}
        <form on:submit|preventDefault={handleCreate} class="form-stack">
          <div class="form-group">
            <label for="long-url">Enter Destination Long URL</label>
            <div class="input-wrap">
              <span class="input-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="2" y1="12" x2="22" y2="12"></line>
                  <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                </svg>
              </span>
              <input
                id="long-url"
                type="text"
                bind:value={originalUrl}
                placeholder="https://example.com/very/long/destination/url"
                required
              />
              {#if originalUrl}
                <button type="button" class="clear-btn" on:click={() => (originalUrl = '')}>Clear</button>
              {/if}
            </div>
            <p class="field-hint">Protocols like <code class="mono">https://</code> are auto-added if omitted.</p>
          </div>

          <!-- Custom Alias Toggle -->
          <div class="alias-toggle-section">
            <button
              type="button"
              class="toggle-link"
              on:click={() => (showCustomCode = !showCustomCode)}
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class:rotated={showCustomCode}>
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
              {showCustomCode ? 'Hide custom alias' : 'Add custom alias / slug (optional)'}
            </button>

            {#if showCustomCode}
              <div class="custom-alias-box">
                <label for="custom-code">Custom Short Code</label>
                <div class="alias-input-wrap">
                  <span class="alias-prefix mono">api/</span>
                  <input
                    id="custom-code"
                    type="text"
                    bind:value={customCode}
                    placeholder="my-cool-link"
                    maxlength="16"
                  />
                </div>
                <p class="field-hint">Up to 16 alphanumeric characters, dashes, or underscores.</p>
              </div>
            {/if}
          </div>

          <button type="submit" class="submit-btn" disabled={loading}>
            {#if loading}
              <span class="spinner"></span>
              Generating via Backend API...
            {:else}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
              </svg>
              Create Short URL
            {/if}
          </button>
        </form>

        <!-- CREATION RESULT CARD -->
        {#if createdResult}
          <div class="result-card success">
            <div class="result-header">
              <div class="result-title">
                <span class="check-icon">✓</span>
                <span>Short Link Generated</span>
              </div>
              <span class="tag mono">POST /api/url/</span>
            </div>

            <div class="result-body">
              <span class="result-label">Your Shortened Link:</span>
              <div class="short-link-row">
                <div class="short-link-display mono">{createdResult.short_url}</div>
                <div class="btn-group">
                  <button
                    type="button"
                    class="btn-action copy"
                    on:click={() => copyText(createdResult.short_url, 'created')}
                  >
                    {copiedKey === 'created' ? '✓ Copied!' : 'Copy'}
                  </button>
                  <a
                    href={createdResult.short_url}
                    target="_blank"
                    rel="noreferrer"
                    class="btn-action visit"
                  >
                    Open ↗
                  </a>
                </div>
              </div>

              <div class="result-footer">
                <span class="dest-label">Destination:</span>
                <span class="dest-url mono">{createdResult.original_url}</span>
              </div>
            </div>
          </div>
        {/if}
      {/if}

      <!-- TAB 2: RETRIEVE -->
      {#if mode === 'retrieve'}
        <form on:submit|preventDefault={handleRetrieve} class="form-stack">
          <div class="form-group">
            <label for="retrieve-input">Enter Short Code or Shortened Link</label>
            <div class="input-wrap">
              <span class="input-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </span>
              <input
                id="retrieve-input"
                type="text"
                bind:value={retrieveInput}
                placeholder="e.g. abc123 or http://localhost:8000/api/abc123"
                required
              />
              {#if retrieveInput}
                <button type="button" class="clear-btn" on:click={() => (retrieveInput = '')}>Clear</button>
              {/if}
            </div>
            <p class="field-hint">You can paste the entire short URL or just the code.</p>

            <!-- Quick test with mock links -->
            <!-- <div class="mock-chips-row">
              <span class="chips-label">Quick test mock links:</span>
              <div class="chips-list">
                {#each ['google', 'github', 'youtube', 'openai'] as mockCode}
                  <button
                    type="button"
                    class="chip-btn mono"
                    on:click={() => {
                      retrieveInput = mockCode;
                      handleRetrieve();
                    }}
                  >
                    {mockCode}
                  </button>
                {/each}
              </div>
            </div> -->
          </div>

          <button type="submit" class="submit-btn" disabled={loading}>
            {#if loading}
              <span class="spinner"></span>
              Looking up from Database...
            {:else}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                <polyline points="15 3 21 3 21 9"></polyline>
                <line x1="10" y1="14" x2="21" y2="3"></line>
              </svg>
              Retrieve Original URL
            {/if}
          </button>
        </form>

        <!-- RETRIEVAL RESULT CARD -->
        {#if retrievedResult}
          <div class="result-card success">
            <div class="result-header">
              <div class="result-title">
                <span class="check-icon">✓</span>
                <span>Original URL Retrieved</span>
              </div>
              <span class="clicks-badge mono">Clicks: {retrievedResult.clicks}</span>
            </div>

            <div class="result-body">
              <span class="result-label">Original Destination URL:</span>
              <div class="short-link-row">
                <div class="short-link-display mono break">{retrievedResult.original_url}</div>
                <div class="btn-group">
                  <button
                    type="button"
                    class="btn-action copy"
                    on:click={() => copyText(retrievedResult.original_url, 'retrieved')}
                  >
                    {copiedKey === 'retrieved' ? '✓ Copied!' : 'Copy'}
                  </button>
                  <a
                    href={retrievedResult.original_url}
                    target="_blank"
                    rel="noreferrer"
                    class="btn-action visit"
                  >
                    Visit Website ↗
                  </a>
                </div>
              </div>

              <div class="result-footer">
                <span class="dest-label">Short Code:</span>
                <span class="mono tag">{retrievedResult.short_code}</span>
              </div>
            </div>
          </div>
        {/if}
      {/if}
    </div>

    <!-- Card Bottom Feature Footnote -->
    <!-- <div class="card-footer">
      <div class="footer-note">
        <span>✓ Connected to FastAPI backend</span>
        <span>•</span>
        <span>PostgreSQL storage</span>
      </div>
      <a href="/admin" class="admin-link">View all in Admin &rarr;</a>
    </div> -->
  </div>
</div>

<style>
  .page-container {
    max-width: 760px;
    margin: 0 auto;
    padding: 3rem 1.25rem 5rem;
    width: 100%;
  }

  .hero {
    text-align: center;
    margin-bottom: 2.25rem;
  }

  .eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: var(--emerald-50);
    border: 1px solid var(--emerald-100);
    color: var(--emerald-700);
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.725rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    margin-bottom: 0.85rem;
  }

  .pulse-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--emerald-600);
    animation: pulse 1.5s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.85); }
  }

  .hero-title {
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1.15;
    color: var(--text-main);
  }

  .highlight {
    color: var(--emerald-600);
  }

  .hero-subtitle {
    margin-top: 0.65rem;
    font-size: 0.95rem;
    color: var(--text-muted);
    max-width: 520px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.5;
  }

  .card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04), 0 1px 3px rgba(0, 0, 0, 0.02);
    overflow: hidden;
  }

  .mode-tabs {
    display: grid;
    grid-template-columns: 1fr 1fr;
    padding: 6px;
    background: #f1f4f1;
    border-bottom: 1px solid var(--border-light);
    gap: 6px;
  }

  .tab-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.45rem;
    padding: 0.75rem 1rem;
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--text-muted);
    border: none;
    border-radius: 12px;
    background: transparent;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .tab-btn:hover {
    color: var(--text-main);
  }

  .tab-btn.active {
    background: #ffffff;
    color: var(--emerald-800);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  }

  .card-body {
    padding: 1.75rem 2rem;
  }

  .form-stack {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }

  .form-group label {
    display: block;
    font-size: 0.775rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-main);
    margin-bottom: 0.45rem;
  }

  .input-wrap {
    display: flex;
    align-items: center;
    position: relative;
    border: 1px solid #d8dfdb;
    border-radius: 12px;
    background: #fdfdfc;
    transition: all 0.15s ease;
  }

  .input-wrap:focus-within {
    border-color: var(--border-focus);
    box-shadow: 0 0 0 3px rgba(27, 109, 81, 0.12);
    background: #ffffff;
  }

  .input-icon {
    display: flex;
    align-items: center;
    padding-left: 0.9rem;
    color: #94a39b;
  }

  .input-wrap input {
    flex: 1;
    border: none;
    background: transparent;
    padding: 0.85rem 0.9rem;
    font-size: 0.925rem;
    color: var(--text-main);
    outline: none;
    min-width: 0;
  }

  .input-wrap input::placeholder {
    color: #a3b0a8;
  }

  .clear-btn {
    border: none;
    background: #e9eee9;
    color: #556b5e;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.3rem 0.6rem;
    margin-right: 0.6rem;
    border-radius: 6px;
    cursor: pointer;
  }

  .field-hint {
    margin-top: 0.4rem;
    font-size: 0.75rem;
    color: #798b81;
  }

  .alias-toggle-section {
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
  }

  .toggle-link {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--emerald-700);
    background: none;
    border: none;
    cursor: pointer;
    align-self: flex-start;
  }

  .toggle-link svg {
    transition: transform 0.2s ease;
  }

  .toggle-link svg.rotated {
    transform: rotate(90deg);
  }

  .custom-alias-box {
    background: #f8faf8;
    border: 1px solid var(--border-light);
    border-radius: 12px;
    padding: 0.85rem 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }

  .custom-alias-box label {
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--text-main);
  }

  .alias-input-wrap {
    display: flex;
    align-items: center;
    border: 1px solid #d8dfdb;
    border-radius: 8px;
    background: #ffffff;
    overflow: hidden;
  }

  .alias-prefix {
    padding: 0.5rem 0.75rem;
    background: #eef2ee;
    font-size: 0.8rem;
    color: #5d7065;
    border-right: 1px solid #d8dfdb;
  }

  .alias-input-wrap input {
    flex: 1;
    border: none;
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
    outline: none;
  }

  .submit-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.9rem 1.5rem;
    border-radius: 12px;
    border: none;
    background: var(--emerald-600);
    color: #ffffff;
    font-size: 0.925rem;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(27, 109, 81, 0.2);
    transition: all 0.15s ease;
  }

  .submit-btn:hover:not(:disabled) {
    background: var(--emerald-700);
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(27, 109, 81, 0.25);
  }

  .submit-btn:disabled {
    opacity: 0.65;
    cursor: not-allowed;
  }

  .spinner {
    width: 14px;
    height: 14px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: #ffffff;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .error-banner {
    display: flex;
    align-items: flex-start;
    gap: 0.65rem;
    padding: 0.85rem 1rem;
    border-radius: 12px;
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #991b1b;
    font-size: 0.825rem;
    margin-bottom: 1.25rem;
  }

  .error-content {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
  }

  /* Result Card */
  .result-card {
    margin-top: 1.5rem;
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    background: var(--emerald-50);
    border: 1px solid var(--emerald-100);
  }

  .result-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid rgba(27, 109, 81, 0.12);
    margin-bottom: 0.85rem;
  }

  .result-title {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    font-weight: 700;
    font-size: 0.85rem;
    color: var(--emerald-800);
  }

  .check-icon {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: var(--emerald-600);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 900;
  }

  .tag {
    font-size: 0.7rem;
    padding: 2px 6px;
    border-radius: 6px;
    background: #ffffff;
    border: 1px solid var(--emerald-100);
    color: var(--emerald-700);
  }

  .clicks-badge {
    font-size: 0.725rem;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 9999px;
    background: #ffffff;
    border: 1px solid var(--emerald-100);
    color: var(--emerald-800);
  }

  .result-body .result-label {
    display: block;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--text-muted);
    margin-bottom: 0.35rem;
  }

  .short-link-row {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  @media (min-width: 600px) {
    .short-link-row {
      flex-direction: row;
      align-items: center;
    }
  }

  .short-link-display {
    flex: 1;
    background: #ffffff;
    border: 1px solid var(--emerald-100);
    padding: 0.65rem 0.85rem;
    border-radius: 10px;
    font-size: 0.85rem;
    color: var(--emerald-800);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    user-select: all;
  }

  .short-link-display.break {
    white-space: normal;
    word-break: break-all;
  }

  .btn-group {
    display: flex;
    gap: 0.35rem;
  }

  .btn-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.65rem 1rem;
    border-radius: 10px;
    font-size: 0.8rem;
    font-weight: 700;
    border: none;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .btn-action.copy {
    background: var(--emerald-600);
    color: #fff;
  }

  .btn-action.copy:hover {
    background: var(--emerald-700);
  }

  .btn-action.visit {
    background: #ffffff;
    border: 1px solid var(--border-light);
    color: var(--text-main);
  }

  .btn-action.visit:hover {
    background: #f3f5f3;
  }

  .result-footer {
    margin-top: 0.75rem;
    padding-top: 0.65rem;
    border-top: 1px solid rgba(27, 109, 81, 0.08);
    display: flex;
    align-items: center;
    gap: 0.45rem;
    font-size: 0.775rem;
  }

  .mock-chips-row {
    margin-top: 0.65rem;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.4rem;
  }

  .chips-label {
    font-size: 0.725rem;
    font-weight: 600;
    color: var(--text-muted);
  }

  .chips-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
  }

  .chip-btn {
    border: 1px solid #c7d2fe;
    background: #eef2ff;
    color: #4338ca;
    padding: 2px 7px;
    border-radius: 6px;
    font-size: 0.725rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .chip-btn:hover {
    background: #e0e7ff;
    color: #3730a3;
    border-color: #a5b4fc;
    transform: translateY(-1px);
  }

  .dest-label {
    font-weight: 600;
    color: var(--text-muted);
  }

  .dest-url {
    color: var(--text-main);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .card-footer {
    padding: 0.85rem 2rem;
    background: #fbfcfb;
    border-top: 1px solid var(--border-light);
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.775rem;
    color: var(--text-muted);
  }

  .footer-note {
    display: flex;
    align-items: center;
    gap: 0.45rem;
  }

  .admin-link {
    font-weight: 700;
    color: var(--emerald-700);
  }

  .admin-link:hover {
    text-decoration: underline;
  }
</style>
