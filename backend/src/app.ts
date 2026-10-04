import Fastify from 'fastify';

export function buildApp() {
  const app = Fastify({ logger: true });

  app.get('/api/health', async () => ({
    status: 'ok',
    service: 'wholesale-customer-segmentation-api',
    modelReady: false,
  }));

  app.get('/api/model-info', async (_request, reply) => {
    return reply.code(503).send({
      status: 'not_ready',
      message: 'Mô hình chưa được huấn luyện. Hoàn tất pipeline dữ liệu và thí nghiệm K-Means trước.',
    });
  });

  return app;
}
