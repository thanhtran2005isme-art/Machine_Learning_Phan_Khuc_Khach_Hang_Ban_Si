import Fastify from 'fastify';
import { z } from 'zod';
import { loadModel, segment, modelInfo, dashboard, type LoadedModel } from '../model.mjs';
import { loadVerifiedDevelopmentExtension } from '../development-extension.mjs';

const spending = z.object({
  Fresh: z.number().finite().nonnegative(),
  Milk: z.number().finite().nonnegative(),
  Grocery: z.number().finite().nonnegative(),
  Frozen: z.number().finite().nonnegative(),
  Detergents_Paper: z.number().finite().nonnegative(),
  Delicassen: z.number().finite().nonnegative(),
}).strict();

export function buildApp(options: { modelPath?: string; profileDir?: string; extensionDir?: string } = {}) {
  const app = Fastify({ logger: false, bodyLimit: 16 * 1024 });
  let loaded: LoadedModel | null = null;
  try {
    loaded = loadModel(options);
  } catch {
    // Do not expose internal filesystem paths or model-loading diagnostics to HTTP clients.
    loaded = null;
  }
  app.get('/api/health', async () => ({
    status: 'ok', service: 'wholesale-customer-segmentation-api', modelReady: loaded !== null,
  }));
  app.get('/api/model-info', async (_request, reply) => {
    if (!loaded) return reply.code(503).send({ status: 'not_ready', message: 'Frozen model unavailable' });
    return modelInfo(loaded);
  });
  app.get('/api/dashboard', async (_request, reply) => {
    if (!loaded) return reply.code(503).send({ status: 'not_ready', message: 'Frozen model unavailable' });
    try { return dashboard(loaded, { profileDir: options.profileDir }); }
    catch { return reply.code(503).send({ status: 'not_ready', message: 'Dashboard evidence unavailable or failed integrity validation' }); }
  });
  app.get('/api/development-extension', async (_request, reply) => {
    if (!loaded) return reply.code(503).send({ status: 'not_ready', message: 'Frozen model unavailable' });
    try { return loadVerifiedDevelopmentExtension(loaded, { extensionDir: options.extensionDir }); }
    catch { return reply.code(503).send({ status: 'not_ready', message: 'Development extension evidence unavailable or invalid' }); }
  });
  app.post('/api/segment', async (request, reply) => {
    if (!loaded) return reply.code(503).send({ status: 'not_ready', message: 'Frozen model unavailable' });
    const checked = spending.safeParse(request.body);
    if (!checked.success) return reply.code(400).send({
      status: 'invalid_input', message: 'Cần đúng 6 giá trị chi tiêu không âm, hữu hạn (kiểu number)',
      errors: checked.error.issues.map(i => ({ path: i.path.join('.'), message: i.message })),
    });
    return { status: 'ok', ...segment(loaded, checked.data) };
  });
  return app;
}
