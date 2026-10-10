import { useState } from 'react';

export type DevelopmentExtension = {
  decision: string; development_count: number; model_sha256: string;
  read_only: boolean; test_used: boolean; feature_space: string;
  pca: { explained_variance_ratio:number[]; components:number[][];method:string;usage:string };
  comparison: {
    method:string;linkage:string;metric:string;n_clusters:number;fit_space:string;
    frozen_counts:number[];hierarchical_counts:number[];contingency:number[][];
    ari:number;silhouette_kmeans:number;silhouette_hierarchical:number;interpretation:string;
  };
  points: { index:number;split:'train'|'validation';pc1:number;pc2:number;
    kmeans:number;hierarchical:number }[];
};
const LABELS=['Fresh','Milk','Grocery','Frozen','Detergents_Paper','Delicassen'];
const number=(v:number,n=3)=>new Intl.NumberFormat('vi-VN',{maximumFractionDigits:n}).format(v);
export function DevelopmentAnalytics({data}:{data:DevelopmentExtension}){
  const [color,setColor]=useState<'kmeans'|'hierarchical'>('kmeans');
  const [filter,setFilter]=useState<'all'|'train'|'validation'>('all');
  const points=data.points.filter(p=>filter==='all'||p.split===filter);
  const xall=data.points.map(p=>p.pc1), yall=data.points.map(p=>p.pc2);
  const minX=Math.min(...xall),maxX=Math.max(...xall),minY=Math.min(...yall),maxY=Math.max(...yall);
  const marginX=Math.max((maxX-minX)*.07,.05),marginY=Math.max((maxY-minY)*.07,.05);
  const mapX=(v:number)=>45+(v-(minX-marginX))/(maxX-minX+2*marginX)*620;
  const mapY=(v:number)=>360-(v-(minY-marginY))/(maxY-minY+2*marginY)*318;
  const label=color==='kmeans'?'K-Means D011':'Hierarchical Ward';
  const share=data.pca.explained_variance_ratio.map(x=>x*100);
  return <section className="content-card development-analytics" aria-label="PCA 2D và so sánh Hierarchical">
    <div className="section-heading">
      <h2>PCA 2D · So sánh K-Means và Hierarchical</h2>
      <p>352 khách development (264 train + 88 validation); không sử dụng final test hoặc huấn luyện lại D011.</p>
    </div>
    <div className="pca-toolbar">
      <div className="analysis-switch" role="group" aria-label="Phương pháp tô màu">
        <button type="button" aria-pressed={color==='kmeans'} className={color==='kmeans'?'toggle-selected':''}
          onClick={()=>setColor('kmeans')}>K-Means D011</button>
        <button type="button" aria-pressed={color==='hierarchical'} className={color==='hierarchical'?'toggle-selected':''}
          onClick={()=>setColor('hierarchical')}>Hierarchical Ward</button>
      </div>
      <div className="analysis-switch" role="group" aria-label="Lọc dữ liệu development">
        {([['all','Tất cả'],['train','Train'],['validation','Validation']] as const).map(([id,text])=>
          <button type="button" key={id} aria-pressed={filter===id}
            className={filter===id?'toggle-selected':''} onClick={()=>setFilter(id)}>{text}</button>)}
      </div>
    </div>
    <div className="pca-summary">
      <div><span>PC1</span><strong>{number(share[0],2)}%</strong><small>phương sai giải thích</small></div>
      <div><span>PC2</span><strong>{number(share[1],2)}%</strong><small>phương sai giải thích</small></div>
      <div><span>Tổng PC1 + PC2</span><strong>{number(share[0]+share[1],2)}%</strong><small>không phải độ chính xác</small></div>
      <div><span>Điểm đang hiển thị</span><strong data-testid="pca-visible-count">{points.length}</strong><small>trên 352 development</small></div>
    </div>
    <div className="pca-main">
      <div className="pca-plot">
        <svg viewBox="0 0 710 405" role="img"
          aria-label={'PCA 2D, '+points.length+' khách, màu theo '+label+', PC1 '+number(share[0],2)+' phần trăm PC2 '+number(share[1],2)+' phần trăm'}>
          <rect x="44" y="25" width="621" height="335" rx="8" fill="#fbfcfc" stroke="#d9e4e4"/>
          <line x1={mapX(0)} y1="25" x2={mapX(0)} y2="360" stroke="#9eaeb0" strokeDasharray="4 5"/>
          <line x1="44" y1={mapY(0)} x2="665" y2={mapY(0)} stroke="#9eaeb0" strokeDasharray="4 5"/>
          {points.map(p=><circle key={p.index} cx={mapX(p.pc1)} cy={mapY(p.pc2)} r="4"
            className={'pca-dot pca-group-'+p[color]} data-split={p.split}
            data-label={p[color]}>
            <title>{'Mẫu '+(p.index+1)+' · '+p.split+' · '+label+' cụm '+p[color]+' · PC1='+number(p.pc1)+' · PC2='+number(p.pc2)}</title>
          </circle>)}
          <text x="355" y="392" textAnchor="middle" fontSize="13" fill="#52666c">PC1 ({number(share[0],1)}%)</text>
          <text x="16" y="205" textAnchor="middle" fontSize="13" fill="#52666c" transform="rotate(-90 16 205)">PC2 ({number(share[1],1)}%)</text>
        </svg>
        <div className="pca-legend"><span><i className="legend-dot pca-group-0"/>Cụm 0</span>
          <span><i className="legend-dot pca-group-1"/>Cụm 1</span><small>Tô theo {label}</small></div>
      </div>
      <div className="pca-notes">
        <h3>Cách đọc biểu đồ</h3>
        <p>Mỗi chấm là một khách trong tập development. PCA chiếu sáu đặc trưng đã log1p + StandardScaler sang hai trục để xem xu hướng hình học.</p>
        <p>Hai trục chỉ giữ {number(share[0]+share[1],2)}% phương sai; các điểm gần nhau trên hình 2D không nhất thiết có khoảng cách gần tương ứng trong 6D.</p>
        <p className="muted small-note">K-Means D011 gán cụm bằng khoảng cách Euclidean 6D từ frozen centroid. Hierarchical Ward cũng được fit offline trên 6D; **không** phân cụm trên tọa độ PCA.</p>
      </div>
    </div>
    <div className="analysis-comparison">
      <div className="section-heading"><h3>So sánh trên cùng 352 khách, cùng không gian 6D</h3>
        <p>Ward là mô hình thăm dò; không thay K-Means D011 dùng trong API phân khúc.</p></div>
      <div className="table-scroll"><table className="data-table" aria-label="So sánh hai thuật toán">
        <thead><tr><th scope="col">Thuật toán</th><th scope="col">Số cụm</th>
          <th scope="col">Silhouette 6D</th><th scope="col">Số khách cụm 0</th><th scope="col">Số khách cụm 1</th></tr></thead>
        <tbody>
          <tr><th scope="row">Frozen K-Means D011</th><td>2</td><td>{number(data.comparison.silhouette_kmeans,4)}</td>
            <td>{data.comparison.frozen_counts[0]}</td><td>{data.comparison.frozen_counts[1]}</td></tr>
          <tr><th scope="row">Hierarchical Ward</th><td>2</td><td>{number(data.comparison.silhouette_hierarchical,4)}</td>
            <td>{data.comparison.hierarchical_counts[0]}</td><td>{data.comparison.hierarchical_counts[1]}</td></tr>
        </tbody>
      </table></div>
      <p><strong>Adjusted Rand Index (ARI): {number(data.comparison.ari,4)}</strong> — đánh giá mức giống nhau của hai phân hoạch, không bị ảnh hưởng bởi việc đổi tên cụm.</p>
      <div className="table-scroll"><table className="data-table" aria-label="Ma trận giao nhau giữa hai phân hoạch">
        <thead><tr><th scope="col">K-Means → Ward</th><th scope="col">Ward 0</th><th scope="col">Ward 1</th></tr></thead>
        <tbody>{data.comparison.contingency.map((row,i)=><tr key={i}>
          <th scope="row">K-Means {i}</th><td>{row[0]}</td><td>{row[1]}</td>
        </tr>)}</tbody>
      </table></div>
      <p className="muted small-note">Mã 0/1 của Ward không tương ứng trực tiếp với mã K-Means; phải đọc ARI và ma trận thay vì đối chiếu nhãn cùng số. Không kết luận thuật toán nào có hiệu quả kinh doanh tốt hơn từ silhouette.</p>
      <details className="pca-loadings"><summary>Chi tiết PCA: hệ số thành phần (loadings)</summary>
        <div className="table-scroll"><table className="data-table" aria-label="Hệ số PCA">
          <thead><tr><th scope="col">Biến</th><th scope="col">PC1</th><th scope="col">PC2</th></tr></thead>
          <tbody>{LABELS.map((f,i)=><tr key={f}><th scope="row">{f}</th>
            <td>{number(data.pca.components[0][i],4)}</td><td>{number(data.pca.components[1][i],4)}</td></tr>)}</tbody>
        </table></div>
        <p className="muted small-note">Hệ số ở không gian chuẩn hóa; dấu trục PCA có thể đảo mà không thay ý nghĩa hình chiếu.</p>
      </details>
    </div>
  </section>;
}
