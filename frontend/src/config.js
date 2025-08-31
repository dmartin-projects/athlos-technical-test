const apiUrl = process.env.REACT_APP_DOCKER_ENV 
  ? 'http://localhost:8000'
  : 'https://0b6bc3f6-0480-40e8-8c57-3af2460a82da-dev.e1-eu-north-azure.choreoapis.dev/pruebatecnica-david/backend/v1.0';

export { apiUrl };