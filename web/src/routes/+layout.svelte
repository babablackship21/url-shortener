<script>
  import '../app.css';
  import Navbar from '$lib/Navbar.svelte';
</script>

<div class="app-shell">
  <Navbar />
  <main class="page-content">
    <slot />
  </main>
  <footer class="footer">
    <p>Minimal & Lightweight URL Shortener</p>
  </footer>
</div>

<style>
  .app-shell {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .page-content {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .footer {
    padding: 1.5rem 1rem;
    text-align: center;
    font-size: 0.75rem;
    color: var(--text-muted);
    border-top: 1px solid var(--border-light);
    background: #ffffff;
  }
</style>

