<script>
  import { onDestroy } from 'svelte';
  let { text, compact = false } = $props();
  let copied = $state(false);
  let failed = $state(false);
  let timer;
  onDestroy(() => clearTimeout(timer));
  async function copy() {
    clearTimeout(timer);
    try {
      await navigator.clipboard.writeText(text);
      copied = true;
      failed = false;
    } catch {
      failed = true;
      copied = false;
    }
    timer = setTimeout(() => { copied = false; failed = false; }, 2000);
  }
</script>
<button class="inline-flex items-center justify-center font-bold cursor-pointer {(compact) ? ('py-[.4rem] px-[.65rem] rounded-md text-xs border border-line bg-surface text-muted hover:bg-brand-50 hover:text-brand-700 hover:border-brand-100') : ('py-[.65rem] px-4 rounded-[10px] text-[.8rem] border-0 bg-brand-600 text-white hover:bg-brand-700')}" type="button"  onclick={copy} title={failed ? 'Unable to copy. Please copy the link manually.' : 'Copy link'} aria-live="polite">
  {failed ? 'Failed' : copied ? (compact ? '\u2713' : '\u2713 Copied!') : 'Copy'}
</button>
