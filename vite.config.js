import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  cacheDir: '.vite_cache',
  optimizeDeps: {
    force: true
  },
  server: {
    fs: {
      strict: false
    }
  }
})