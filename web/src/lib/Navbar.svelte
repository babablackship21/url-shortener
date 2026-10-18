<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { checkHealth } from '$lib/api.js';

  let backendHealthy = false;
  let checking = true;

  onMount(async () => {
    try {
      const res = await checkHealth();
      backendHealthy = res.database === 'connected';
    } catch {
      backendHealthy = false;
    } finally {
      checking = false;
    }
  });
</script>

<header class="navbar">
  <div class="nav-container">
    <!-- Brand -->
    <a href="/" class="brand">
      <div class="brand-icon">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
          <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
        </svg>
      </div>
      <div class="brand-title">
        <span>snip<span class="dot">.</span></span>
        <span class="badge">MVP</span>
      </div>
    </a>

    <!-- Nav Links & Status -->
    <div class="nav-right">
      <nav class="nav-links">
        <a href="/" class="nav-link" class:active={$page.url.pathname === '/'}>
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          Shorten & Retrieve
        </a>
        <a href="/admin" class="nav-link" class:active={$page.url.pathname.startsWith('/admin')}>
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="4" y1="6" x2="20" y2="6"></line>
            <line x1="4" y1="12" x2="20" y2="12"></line>
            <line x1="4" y1="18" x2="20" y2="18"></line>
          </svg>
          Admin
        </a>
      </nav>

      <!-- Backend status pill -->
      <div class="status-pill" title={backendHealthy ? "Connected to FastAPI Backend" : "Connecting to Backend /api"}>
        <span class="status-dot" class:healthy={backendHealthy} class:checking={checking}></span>
        <span class="status-text">{backendHealthy ? "API Ready" : (checking ? "Connecting..." : "API Standby")}</span>
      </div>
    </div>
  </div>
</header>

<style>
  .navbar {
    width: 100%;
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border-light);
    position: sticky;
    top: 0;
    z-index: 50;
  }

  .nav-container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 1.25rem;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    color: var(--text-main);
  }

  .brand-icon {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    background: var(--emerald-600);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 6px rgba(27, 109, 81, 0.25);
  }

  .brand-title {
    display: flex;
    align-items: baseline;
    gap: 0.4rem;
    font-weight: 800;
    font-size: 1.25rem;
    letter-spacing: -0.03em;
  }

  .dot {
    color: var(--amber-500);
  }

  .badge {
    font-size: 0.65rem;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 9999px;
    background: var(--emerald-50);
    color: var(--emerald-700);
    border: 1px solid var(--emerald-100);
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }

  .nav-right {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .nav-links {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    background: #f0f3f1;
    padding: 3px;
    border-radius: 10px;
    border: 1px solid var(--border-light);
  }

  .nav-link {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.45rem 0.85rem;
    font-size: 0.825rem;
    font-weight: 600;
    color: var(--text-muted);
    border-radius: 7px;
    transition: all 0.15s ease;
  }

  .nav-link:hover {
    color: var(--text-main);
  }

  .nav-link.active {
    background: #ffffff;
    color: var(--emerald-800);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  }

  .status-pill {
    display: none;
    align-items: center;
    gap: 0.35rem;
    padding: 0.3rem 0.6rem;
    border-radius: 9999px;
    background: #f4f6f4;
    border: 1px solid var(--border-light);
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--text-muted);
  }

  @media (min-width: 640px) {
    .status-pill {
      display: flex;
    }
  }

  .status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #f59e0b;
  }

  .status-dot.healthy {
    background: #10b981;
    box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
  }

  .status-dot.checking {
    background: #9ca3af;
  }
</style>

