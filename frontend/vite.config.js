import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',   // આ લાઈન તમારા ALB (લોડ બેલેન્સર) ના ટ્રાફિકને અંદર આવવા દેશે
    port: 5173,
    strictPort: true   // આનાથી પોર્ટ બદલાશે નહીં અને હંમેશા 5173 જ રહેશે
  }
})
