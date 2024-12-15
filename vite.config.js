import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // 네트워크 접근 허용
    port: 5173  // 기본 포트
  },
  preview: {
    host: true, // 네트워크 접근 허용
    port: 4173  // 프로덕션 프리뷰 포트
  }
})
