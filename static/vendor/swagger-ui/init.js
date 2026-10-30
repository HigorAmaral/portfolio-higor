// Inicializa o Swagger UI servido localmente (sem CDN de terceiros, compatível com a CSP 'self').
window.addEventListener('load', function () {
  SwaggerUIBundle({
    url: '/api/docs/schema.json',
    dom_id: '#swagger-ui',
    deepLinking: true,
    presets: [SwaggerUIBundle.presets.apis],
    layout: 'BaseLayout',
    // Desabilita validação externa (evita requisições para validator.swagger.io)
    validatorUrl: null
  });
});
