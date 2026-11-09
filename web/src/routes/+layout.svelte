<script>
  import '../app.css';
  import Navbar from '$lib/Navbar.svelte';
</script>
<div class="min-h-screen flex flex-col">
  <Navbar />
  <main class="flex-1 flex flex-col">
    <slot />
  </main>
  <footer class="py-6 px-4 text-center text-xs text-muted border-t border-t-line bg-white">
    <p>Minimal & Lightweight URL Shortener</p>
  </footer>
</div>
