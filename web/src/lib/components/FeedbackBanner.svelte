<script>
  import { CircleAlert, Check } from '@lucide/svelte';
  let { message, type = 'error', ondismiss } = $props();
</script>
{#if message}
  <div class="flex items-center gap-[.65rem] py-[.85rem] px-4 rounded-xl border text-[.825rem] my-4 mx-0 {(type === 'error') ? ('bg-[#fef2f2] text-[#991b1b] border-[#fecaca]') : ('bg-brand-50 text-brand-800 border-brand-100')}"  role={type === 'error' ? 'alert' : 'status'}>
    {#if type === 'error'}<CircleAlert size={18} />{:else}<Check size={18} />{/if}
    <span class="flex-1">{message}</span>
    {#if ondismiss}<button class="bg-transparent border-0 text-inherit cursor-pointer text-base" type="button" onclick={ondismiss} aria-label="Dismiss message">&times;</button>{/if}
  </div>
{/if}
