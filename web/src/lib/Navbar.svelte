<script>
  import { page } from '$app/stores';
  import { Link, Plus, Menu } from '@lucide/svelte';
  import BackendStatus from '$lib/components/BackendStatus.svelte';
</script>
<header class="w-full bg-[rgba(255,_255,_255,_0.85)] backdrop-blur-[12px] border-b border-b-line sticky top-0 z-[50]">
  <div class="max-w-[1100px] my-0 mx-auto py-0 px-5 h-16 flex items-center justify-between">
    <!-- Brand -->
    <a href="/" class="flex items-center gap-[0.65rem] text-ink">
      <div class="w-8.5 h-8.5 rounded-[10px] bg-brand-600 text-white flex items-center justify-center shadow-[0_2px_6px_rgba(27,_109,_81,_0.25)]">
        <Link size={18} />
      </div>
      <div class="flex items-baseline gap-[0.4rem] font-extrabold text-xl tracking-[-0.03em]">
        <span>snip<span class="text-amber-600">.</span></span>
        <span class="text-[0.65rem] font-bold py-0.5 px-1.5 rounded-full bg-brand-50 text-brand-700 border border-brand-100 tracking-[0.05em] uppercase">MVP</span>
      </div>
    </a>
    <!-- Nav Links & Status -->
    <div class="flex items-center gap-3">
      <nav class="flex items-center gap-[0.35rem] bg-[#f0f3f1] p-[3px] rounded-[10px] border border-line">
        <a href="/" class="flex items-center gap-[0.35rem] py-[0.45rem] px-[0.85rem] text-[0.825rem] font-semibold rounded-[7px] transition-all duration-150 ease-[ease] {($page.url.pathname === '/') ? ('text-brand-800 bg-white shadow-[0_1px_3px_rgba(0,_0,_0,_0.06)]') : ('text-muted hover:text-ink')}" >
          <Plus size={15} aria-hidden="true" />
          Shorten & Retrieve
        </a>
        <a href="/admin" class="flex items-center gap-[0.35rem] py-[0.45rem] px-[0.85rem] text-[0.825rem] font-semibold rounded-[7px] transition-all duration-150 ease-[ease] {($page.url.pathname.startsWith('/admin')) ? ('text-brand-800 bg-white shadow-[0_1px_3px_rgba(0,_0,_0,_0.06)]') : ('text-muted hover:text-ink')}" >
          <Menu size={15} aria-hidden="true" />
          Admin
        </a>
      </nav>
      <!-- Backend status pill -->
      <BackendStatus />
    </div>
  </div>
</header>
