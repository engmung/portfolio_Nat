module.exports = {
  apps: [
    {
      name: 'fort-net-frontend',
      script: 'npm',
      args: 'run preview',
      cwd: './',
      env: {
        NODE_ENV: 'production',
        VITE_API_URL: 'http://localhost:8000'
      }
    },
    {
      name: 'fort-net-backend',
      cwd: './backend',
      script: 'uvicorn',
      args: 'main:app --host 0.0.0.0 --port 8000',
      interpreter: './venv/bin/python3',
      env: {
        PYTHONPATH: '.'
      }
    }
  ]
}
