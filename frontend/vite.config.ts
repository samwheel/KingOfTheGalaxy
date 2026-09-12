import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/starmap': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/tech_tree': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/empires': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/turn': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/ships': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/shipyard': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
    },
  },
})
