import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    port: 3000,
    watch: {
      // Docker Desktop bind mounts may not forward Windows file-change events.
      usePolling: process.env.VITE_USE_POLLING === 'true',
      interval: 300
    },
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  }
});

