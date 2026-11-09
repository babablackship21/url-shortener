<script>
import { onMount, onDestroy } from 'svelte';
  import { listUrls, deleteUrl } from '$lib/api/links.js';
  import { seedMockLinks, deleteMockLinks, MOCK_SHORT_CODES } from '$lib/api/seed.js';
  import AdminOverview from '$lib/components/admin/AdminOverview.svelte';
  import AdminToolbar from '$lib/components/admin/AdminToolbar.svelte';
  import LinksTable from '$lib/components/admin/LinksTable.svelte';
  import FeedbackBanner from '$lib/components/FeedbackBanner.svelte';
  let urls = [];
  let loading = true;
  let seeding = false;
  let deletingMock = false;
  let errorMessage = '';
  let feedbackMessage = '';
  let feedbackType = 'success'; // 'success' | 'error'
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
  async function handleDelete(shortCode) {
    if (!confirm(`Are you sure you want to delete short URL "${shortCode}"?`)) return;
    try {
      await deleteUrl(shortCode);
      urls = urls.filter((item) => item.short_code !== shortCode);
      showFeedback(`Short link "${shortCode}" deleted.`, 'success');
    } catch (err) {
      showFeedback(err.message || 'Failed to delete URL.', 'error');
    }
  }
</script>
<svelte:head>
  <title>Admin Dashboard — All Created URLs</title>
</svelte:head>
<div class="max-w-[1500px] my-0 mx-auto pt-10 px-5 pb-20 w-full">
  <!-- Header Bar -->
  <div class="flex flex-col gap-4 pb-6 border-b border-b-line sm:flex-row sm:items-end sm:justify-between">
    <div>
      <div class="flex items-center gap-[0.4rem] text-[0.775rem] font-semibold text-muted mb-[0.35rem]">
        <a class="hover:text-brand-700" href="/">Home</a>
        <span>/</span>
        <span class="text-brand-800">Admin Dashboard</span>
      </div>
      <h1 class="text-[1.85rem] font-extrabold tracking-[-0.03em] text-ink">All Created Short URLs</h1>
    </div>
    <!-- Header Actions including Seed and Delete Mock Links -->
    <AdminToolbar {hasMockLinks} {seeding} {deletingMock} onseed={handleSeedMockLinks} ondeletemock={handleDeleteMockLinks} onrefresh={loadData} />
  </div>
  <!-- Feedback Banner (auto-dismissing) -->
  <FeedbackBanner message={feedbackMessage} type={feedbackType} ondismiss={() => (feedbackMessage = "")} />
  <!-- KPI Overview Cards -->
<AdminOverview {urls} />
  <!-- Table Card Wrapper -->
  <LinksTable {urls} {loading} {errorMessage} {seeding} onseed={handleSeedMockLinks} onrefresh={loadData} ondelete={handleDelete} />
</div>
