import { useEffect, useState } from 'react';

type HealthResponse = {
  status: string;
  service: string;
  modelReady: boolean;
};

export default function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/api/health')
      .then(async (response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json() as Promise<HealthResponse>;
      })
      .then(setHealth)
      .catch((reason: unknown) => {
        setError(reason instanceof Error ? reason.message : 'Không kết nối được backend');
      });
  }, []);

  return (
    <main className="page">
      <section className="card">
        <p className="eyebrow">PROJECT 22 · GIAI ĐOẠN NỀN TẢNG</p>
        <h1>Phân khúc khách hàng bán sỉ theo cơ cấu chi tiêu</h1>
        <p>
          Skeleton React + TypeScript đã sẵn sàng. Giai đoạn hiện tại chỉ dựng kiến trúc và
          pipeline dữ liệu; K-Means chưa được huấn luyện.
        </p>
        <div className="status">
          <strong>Backend:</strong>{' '}
          {health ? `${health.status} · modelReady=${health.modelReady}` : error ? `Lỗi: ${error}` : 'Đang kiểm tra…'}
        </div>
      </section>
    </main>
  );
}
