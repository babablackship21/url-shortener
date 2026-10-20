<script>
  import { onMount, onDestroy } from 'svelte';
  import {
    listUrls,
    deleteUrl,
    seedMockLinks,
    deleteMockLinks,
    buildShortUrl,
    MOCK_SHORT_CODES,
  } from '$lib/api.js';

  let urls = [];
  let loading = true;
  let seeding = false;
  let deletingMock = false;
  let searchQuery = '';
  let errorMessage = '';
  let feedbackMessage = '';
  let feedbackType = 'success'; // 'success' | 'error'
  let copiedKey = null;
  let feedbackTimeout = null;

  function showFeedback(msg, type = 'success', durationMs = 4000) {
    feedbackMessage = msg;
    feedbackType = type;
    if (feedbackTimeout) clearTimeout(feedbackTimeout);
    feedbackTimeout = setTimeout(() => {
      feedbackMessage = '';
    }, durationMs);
  }

  onDestroy(() => {
    if (feedbackTimeout) clearTimeout(feedbackTimeout);
  });

  async function loadData() {
    loading = true;
    errorMessage = '';
    try {
      urls = await listUrls();
    } catch (err) {
      errorMessage = err.message || 'Failed to fetch URLs from backend.';
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    loadData();
  });

  $: filteredUrls = urls.filter((item) => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase().trim();
    return (
      item.short_code.toLowerCase().includes(q) ||
      item.original_url.toLowerCase().includes(q)
    );
  });

  $: totalClicks = urls.reduce((acc, curr) => acc + (curr.clicks || 0), 0);

  $: topPerformer = urls.length > 0
    ? [...urls].sort((a, b) => (b.clicks || 0) - (a.clicks || 0))[0]
    : null;

  $: hasMockLinks = urls.some((item) => MOCK_SHORT_CODES.includes(item.short_code));

  async function handleSeedMockLinks() {
    seeding = true;
    try {
      const res = await seedMockLinks();
      const count = Array.isArray(res) ? res.length : 0;
      showFeedback(
        count > 0
          ? `Successfully seeded ${count} mock links (${MOCK_SHORT_CODES.join(', ')}).`
          : 'Mock links already exist in the database.',
        'success'
      );
      await loadData();
    } catch (err) {
      showFeedback(err.message || 'Failed to seed mock links.', 'error');
    } finally {
      seeding = false;
    }
  }

  async function handleDeleteMockLinks() {
    if (!confirm(`Are you sure you want to delete all seeded mock links (${MOCK_SHORT_CODES.join(', ')})?`)) return;

    deletingMock = true;
    try {
      await deleteMockLinks();
      showFeedback('All mock links have been deleted from the database.', 'success');
      await loadData();
    } catch (err) {
      showFeedback(err.message || 'Failed to delete mock links.', 'error');
    } finally {
      deletingMock = false;
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

  async function handleDelete(shortCode) {
    if (!confirm(`Are you sure you want to delete short URL "${shortCode}"?`)) return;

    try {
      await deleteUrl(shortCode);
      urls = urls.filter((item) => item.short_code !== shortCode);
      showFeedback(`Short link "${shortCode}" deleted.`, 'success');
    } catch (err) {
      alert(err.message || 'Failed to delete URL.');
    }
  }

  function formatDate(isoStr) {
    if (!isoStr) return '';
    try {
      const d = new Date(isoStr);
      return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
    } catch {
      return '';
    }
  }
</script>

<svelte:head>
  <title>Admin Dashboard — All Created URLs</title>
</svelte:head>

<div class="admin-container">
  <!-- Header Bar -->
  <div class="admin-header">
    <div>
      <div class="breadcrumb">
        <a href="/">Home</a>
        <span>/</span>
        <span class="active">Admin Dashboard</span>
      </div>
      <h1 class="page-title">All Created Short URLs</h1>
    </div>

    <!-- Header Actions including Seed and Delete Mock Links -->
    <div class="header-actions">
      <a href="/" class="btn-create">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        Create Link
      </a>

      <!-- Seed Mock Links Button -->
      <button
        type="button"
        class="btn-seed"
        on:click={handleSeedMockLinks}
        disabled={seeding}
        title="Seed database with mock links (POST /api/seed/)"
      >
        {#if seeding}
          <span class="spinner-small"></span>
          <span>Seeding...</span>
        {:else}
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"></path>
          </svg>
          <span>Seed Mock Links</span>
        {/if}
      </button>

      <!-- Delete Mock Links Button -->
      {#if hasMockLinks}
        <button
          type="button"
          class="btn-delete-mock"
          on:click={handleDeleteMockLinks}
          disabled={deletingMock}
          title="Delete all mock links from database (DELETE /api/seed/)"
        >
          {#if deletingMock}
            <span class="spinner-small danger"></span>
            <span>Deleting...</span>
          {:else}
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
            <span>Delete Mock Links</span>
          {/if}
        </button>
      {/if}

      <button type="button" class="btn-refresh" on:click={loadData} title="Refresh from backend">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="23 4 23 10 17 10"></polyline>
          <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
        </svg>
        <span>Refresh</span>
      </button>
    </div>
  </div>

  <!-- Feedback Banner (auto-dismissing) -->
  {#if feedbackMessage}
    <div class="feedback-banner" class:error={feedbackType === 'error'} class:success={feedbackType === 'success'}>
      <div class="feedback-text">
        <span>{feedbackType === 'success' ? '✓' : '⚠️'}</span>
        <span>{feedbackMessage}</span>
      </div>
      <button type="button" class="close-feedback" on:click={() => (feedbackMessage = '')}>✕</button>
    </div>
  {/if}

  <!-- KPI Overview Cards -->
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-top">
        <span class="kpi-label">Total Links</span>
        <div class="kpi-icon emerald">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
            <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
          </svg>
        </div>
      </div>
      <div class="kpi-value mono">{urls.length}</div>
      <p class="kpi-subtext">{urls.length === 0 ? 'Project just started' : 'Active records in database'}</p>
    </div>

    <div class="kpi-card">
      <div class="kpi-top">
        <span class="kpi-label">Total Clicks Recorded</span>
        <div class="kpi-icon amber">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
          </svg>
        </div>
      </div>
      <div class="kpi-value mono">{totalClicks}</div>
      <p class="kpi-subtext">Cumulative clicks / lookups</p>
    </div>

    <div class="kpi-card">
      <div class="kpi-top">
        <span class="kpi-label">Top Performer</span>
        <div class="kpi-icon purple">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
          </svg>
        </div>
      </div>
      <div class="kpi-value mono" class:dim={!topPerformer}>
        {topPerformer ? `${topPerformer.short_code} (${topPerformer.clicks})` : 'None yet'}
      </div>
      <p class="kpi-subtext truncate">{topPerformer ? topPerformer.original_url : 'No click activity yet'}</p>
    </div>
  </div>

  <!-- Table Card Wrapper -->
  <div class="table-card">
    {#if urls.length > 0}
      <div class="search-bar">
        <div class="search-input-wrap">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input
            type="text"
            bind:value={searchQuery}
            placeholder="Search by code or destination URL..."
          />
          {#if searchQuery}
            <button type="button" class="clear-search" on:click={() => (searchQuery = '')}>✕</button>
          {/if}
        </div>
        <div class="table-info">
          {#if hasMockLinks}
            <span class="mock-summary-pill mono">Mock links active</span>
          {/if}
          <span class="count-badge">Showing {filteredUrls.length} of {urls.length} URLs</span>
        </div>
      </div>
    {/if}

    {#if loading}
      <!-- Loading State -->
      <div class="state-container">
        <div class="spinner-large"></div>
        <p>Loading URLs from PostgreSQL...</p>
      </div>
    {:else if errorMessage}
      <!-- Error State -->
      <div class="state-container">
        <p class="error-msg">⚠️ {errorMessage}</p>
        <button type="button" class="btn-retry" on:click={loadData}>Retry Connection</button>
      </div>
    {:else if urls.length === 0}
      <!-- ============================================================== -->
      <!-- FEATURE 4: EMPTY STATE WHEN PROJECT JUST STARTED               -->
      <!-- ============================================================== -->
      <div class="empty-state">
        <div class="empty-illustration">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
            <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
          </svg>
        </div>
        <h3 class="empty-title">No shortened URLs yet</h3>
        <p class="empty-description">
          The project was just started and no URLs have been created in the database yet. You can create your first link, or use the <strong>Seed Mock Links</strong> API to populate sample data instantly.
        </p>
        <div class="empty-actions">
          <a href="/" class="btn-create large">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            Create Your First Link
          </a>

          <!-- Seed Mock Links CTA in Empty State -->
          <button
            type="button"
            class="btn-seed large"
            on:click={handleSeedMockLinks}
            disabled={seeding}
          >
            {#if seeding}
              <span class="spinner-small"></span>
              <span>Seeding Mock Links...</span>
            {:else}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"></path>
              </svg>
              <span>Seed Mock Links</span>
            {/if}
          </button>

          <button type="button" class="btn-refresh" on:click={loadData}>
            Check Again
          </button>
        </div>
      </div>
    {:else if filteredUrls.length === 0}
      <!-- No search matches -->
      <div class="state-container">
        <p>No links matching "{searchQuery}"</p>
        <button type="button" class="btn-retry" on:click={() => (searchQuery = '')}>Clear search</button>
      </div>
    {:else}
      <!-- Table View for Desktop -->
      <div class="table-responsive">
        <table class="url-table">
          <thead>
            <tr>
              <th>Short Code</th>
              <th>Original Destination URL</th>
              <th class="center">Clicks</th>
              <th>Created</th>
              <th class="right">Actions</th>
            </tr>
          </thead>
          <tbody>
            {#each filteredUrls as item (item.id || item.short_code)}
              <tr>
                <!-- Short code -->
                <td class="code-cell">
                  <div class="code-badge-group">
                    <span class="code-pill mono">{item.short_code}</span>
                    {#if MOCK_SHORT_CODES.includes(item.short_code)}
                      <span class="mock-tag mono" title="Created via Seed Mock Links API">mock</span>
                    {/if}
                  </div>
                  <div class="short-url-link mono">{buildShortUrl(item.short_code)}</div>
                </td>

                <!-- Original URL -->
                <td class="url-cell">
                  <a
                    href={item.original_url}
                    target="_blank"
                    rel="noreferrer"
                    class="dest-link mono"
                    title={item.original_url}
                  >
                    <span>{item.original_url}</span>
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                      <polyline points="15 3 21 3 21 9"></polyline>
                      <line x1="10" y1="14" x2="21" y2="3"></line>
                    </svg>
                  </a>
                </td>

                <!-- Clicks -->
                <td class="center clicks-cell">
                  <span class="click-counter mono">{item.clicks || 0}</span>
                </td>

                <!-- Created Date -->
                <td class="created-cell">
                  <span class="date-text mono">{formatDate(item.created_at) || '—'}</span>
                </td>

                <!-- Actions -->
                <td class="right action-cell">
                  <div class="action-buttons">
                  <button
                    type="button"
                    class="action-btn copy"
                    title="Copy full short link"
                    on:click={() => copyText(buildShortUrl(item.short_code), item.short_code)}
                  >
                    {copiedKey === item.short_code ? '✓' : 'Copy'}
                  </button>

                  <a
                    href={buildShortUrl(item.short_code)}
                    target="_blank"
                    rel="noreferrer"
                    class="action-btn visit"
                    title="Test redirect in new tab"
                  >
                    Test ↗
                  </a>

                  {#if item.can_delete === true}
                  <button
                    type="button"
                    class="action-btn delete"
                    title="Delete short link"
                    on:click={() => handleDelete(item.short_code)}
                  >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
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
</div>

<style>
  .admin-container {
    max-width: 1500px;
    margin: 0 auto;
    padding: 2.5rem 1.25rem 5rem;
    width: 100%;
  }

  .admin-header {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border-light);
  }

  @media (min-width: 640px) {
    .admin-header {
      flex-direction: row;
      align-items: flex-end;
      justify-content: space-between;
    }
  }

  .breadcrumb {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.775rem;
    font-weight: 600;
    color: var(--text-muted);
    margin-bottom: 0.35rem;
  }

  .breadcrumb a:hover {
    color: var(--emerald-700);
  }

  .breadcrumb .active {
    color: var(--emerald-800);
  }

  .page-title {
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--text-main);
  }

  .page-subtitle {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-top: 0.25rem;
  }

  .header-actions {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    align-items: center;
  }

  .btn-create {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.55rem 1rem;
    border-radius: 10px;
    background: var(--emerald-600);
    color: #fff;
    font-size: 0.825rem;
    font-weight: 700;
    box-shadow: 0 2px 6px rgba(27, 109, 81, 0.2);
    transition: all 0.15s ease;
  }

  .btn-create:hover {
    background: var(--emerald-700);
  }

  .btn-create.large {
    padding: 0.75rem 1.4rem;
    font-size: 0.9rem;
  }

  /* Seed Button */
  .btn-seed {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.55rem 0.95rem;
    border-radius: 10px;
    background: #eef2ff;
    border: 1px solid #c7d2fe;
    color: #4338ca;
    font-size: 0.825rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .btn-seed:hover:not(:disabled) {
    background: #e0e7ff;
    color: #3730a3;
    border-color: #a5b4fc;
  }

  .btn-seed.large {
    padding: 0.75rem 1.4rem;
    font-size: 0.9rem;
  }

  .btn-seed:disabled {
    opacity: 0.65;
    cursor: not-allowed;
  }

  /* Delete Mock Links Button */
  .btn-delete-mock {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.55rem 0.95rem;
    border-radius: 10px;
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #b91c1c;
    font-size: 0.825rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .btn-delete-mock:hover:not(:disabled) {
    background: #fee2e2;
    color: #991b1b;
    border-color: #fca5a5;
  }

  .btn-delete-mock:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .btn-refresh {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.55rem 0.85rem;
    border-radius: 10px;
    background: #ffffff;
    border: 1px solid var(--border-light);
    color: var(--text-muted);
    font-size: 0.825rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .btn-refresh:hover {
    background: #f4f6f4;
    color: var(--text-main);
  }

  /* Feedback banner */
  .feedback-banner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1rem;
    border-radius: 12px;
    margin-top: 1rem;
    font-size: 0.825rem;
    font-weight: 600;
    animation: fadeIn 0.2s ease;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(-4px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .feedback-banner.success {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    color: #065f46;
  }

  .feedback-banner.error {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #991b1b;
  }

  .feedback-text {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .close-feedback {
    background: none;
    border: none;
    font-size: 0.85rem;
    cursor: pointer;
    color: inherit;
    opacity: 0.7;
  }

  .close-feedback:hover {
    opacity: 1;
  }

  .spinner-small {
    width: 12px;
    height: 12px;
    border: 2px solid rgba(67, 56, 202, 0.25);
    border-top-color: #4338ca;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
  }

  .spinner-small.danger {
    border-color: rgba(185, 28, 28, 0.25);
    border-top-color: #b91c1c;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  /* KPI Grid */
  .kpi-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
    margin: 1.5rem 0;
  }

  @media (min-width: 640px) {
    .kpi-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }

  .kpi-card {
    background: #ffffff;
    border: 1px solid var(--border-light);
    border-radius: 16px;
    padding: 1.25rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
  }

  .kpi-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .kpi-label {
    font-size: 0.725rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-muted);
  }

  .kpi-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .kpi-icon.emerald { background: var(--emerald-50); color: var(--emerald-700); }
  .kpi-icon.amber { background: #fef3c7; color: #b45309; }
  .kpi-icon.purple { background: #f3e8ff; color: #7e22ce; }

  .kpi-value {
    font-size: 1.85rem;
    font-weight: 800;
    margin-top: 0.5rem;
    color: var(--text-main);
  }

  .kpi-value.dim {
    font-size: 1.1rem;
    font-weight: 600;
    color: #9ca3af;
  }

  .kpi-subtext {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 0.25rem;
  }

  /* Table Card */
  .table-card {
    background: #ffffff;
    border: 1px solid var(--border-light);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
  }

  .search-bar {
    padding: 1rem 1.25rem;
    border-bottom: 1px solid var(--border-light);
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    background: #fafbfa;
  }

  @media (min-width: 640px) {
    .search-bar {
      flex-direction: row;
      align-items: center;
      justify-content: space-between;
    }
  }

  .search-input-wrap {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: #ffffff;
    border: 1px solid #d8dfdb;
    border-radius: 10px;
    padding: 0.45rem 0.75rem;
    width: 100%;
    max-width: 360px;
  }

  .search-input-wrap input {
    border: none;
    outline: none;
    font-size: 0.825rem;
    width: 100%;
  }

  .clear-search {
    border: none;
    background: none;
    color: #9ca3af;
    cursor: pointer;
  }

  .table-info {
    display: flex;
    align-items: center;
    gap: 0.65rem;
  }

  .mock-summary-pill {
    font-size: 0.675rem;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 6px;
    background: #eef2ff;
    color: #4338ca;
    border: 1px solid #c7d2fe;
    text-transform: uppercase;
  }

  .count-badge {
    font-size: 0.75rem;
    color: var(--text-muted);
  }

  .table-responsive {
    overflow-x: auto;
  }

  .url-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.825rem;
    text-align: left;
  }

  .url-table th {
    padding: 0.85rem 1.25rem;
    background: #f7f9f7;
    color: var(--text-muted);
    font-size: 0.725rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 1px solid var(--border-light);
  }

  .url-table td {
    padding: 1rem 1.25rem;
    border-bottom: 1px solid #f0f3f0;
    vertical-align: middle;
  }

  .url-table tr:hover {
    background: #fafcfa;
  }

  .center { text-align: center; }
  .right { text-align: right; }

  .code-badge-group {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
  }

  .code-pill {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 6px;
    background: var(--emerald-50);
    border: 1px solid var(--emerald-100);
    color: var(--emerald-800);
    font-weight: 700;
    font-size: 0.8rem;
  }

  .mock-tag {
    font-size: 0.65rem;
    font-weight: 800;
    padding: 1px 5px;
    border-radius: 4px;
    background: #eef2ff;
    color: #4f46e5;
    border: 1px solid #c7d2fe;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }

  .short-url-link {
    font-size: 0.725rem;
    color: #8b9d92;
    margin-top: 3px;
  }

  .dest-link {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    color: var(--text-main);
    max-width: 420px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .dest-link:hover {
    color: var(--emerald-700);
    text-decoration: underline;
  }

  .click-counter {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 9999px;
    background: #f0f3f0;
    color: var(--text-main);
    font-size: 0.75rem;
    font-weight: 700;
  }

  .created-cell {
    white-space: nowrap;
  }

  .date-text {
    font-size: 0.75rem;
    color: var(--text-muted);
  }

  .action-cell {
    white-space: nowrap;
  }

  .action-buttons {
    display: inline-grid;
    grid-template-columns: 3.5rem 4rem 2.25rem;
    gap: 0.25rem;
    align-items: center;
  }

  .action-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.4rem 0.65rem;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    border: 1px solid var(--border-light);
    background: #ffffff;
    color: var(--text-muted);
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .action-btn:hover {
    color: var(--text-main);
    border-color: #cbd5e1;
  }

  .action-btn.copy:hover {
    color: var(--emerald-700);
    border-color: var(--emerald-100);
    background: var(--emerald-50);
  }

  .action-btn.delete:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .action-btn.delete:hover:not(:disabled) {
    color: #dc2626;
    border-color: #fecaca;
    background: #fef2f2;
  }

  /* States */
  .state-container {
    padding: 4rem 1.5rem;
    text-align: center;
    color: var(--text-muted);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
  }

  .spinner-large {
    width: 28px;
    height: 28px;
    border: 3px solid #e2e8f0;
    border-top-color: var(--emerald-600);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  .btn-retry {
    padding: 0.45rem 0.85rem;
    border-radius: 8px;
    background: #ffffff;
    border: 1px solid var(--border-light);
    font-size: 0.775rem;
    font-weight: 600;
    cursor: pointer;
  }

  /* Empty state */
  .empty-state {
    padding: 4.5rem 1.5rem;
    text-align: center;
    max-width: 520px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .empty-illustration {
    width: 68px;
    height: 68px;
    border-radius: 20px;
    background: var(--emerald-50);
    border: 1px solid var(--emerald-100);
    color: var(--emerald-700);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.25rem;
  }

  .empty-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--text-main);
  }

  .empty-description {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-top: 0.5rem;
    line-height: 1.5;
  }

  .empty-actions {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-top: 1.75rem;
    flex-wrap: wrap;
    justify-content: center;
  }
</style>
