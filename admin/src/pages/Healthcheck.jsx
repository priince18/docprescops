import { useEffect } from 'react'

const Healthcheck = () => {
  useEffect(() => {
    const response = {
      status: 'ok',
      timestamp: new Date().toISOString(),
      uptime: performance.now() / 1000
    }
    document.write(JSON.stringify(response))
  }, [])

  return null
}

export default Healthcheck
