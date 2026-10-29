export type CustomerFeature = 'Fresh' | 'Milk' | 'Grocery' | 'Frozen' | 'Detergents_Paper' | 'Delicassen';

export const CUSTOMER_HISTORY_KEY = 'project22.customer-history.v1';

export type StoredCustomer<Result> = {
  id: string;
  name: string;
  note: string;
  values: Record<CustomerFeature, string>;
  result: Result;
  createdAt: string;
};

export function readCustomerHistory<Result>(): StoredCustomer<Result>[] {
  try {
    const raw = window.localStorage.getItem(CUSTOMER_HISTORY_KEY);
    if (!raw) return [];
    const parsed: unknown = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed as StoredCustomer<Result>[] : [];
  } catch {
    return [];
  }
}

export function writeCustomerHistory<Result>(entries: StoredCustomer<Result>[]): void {
  try {
    window.localStorage.setItem(CUSTOMER_HISTORY_KEY, JSON.stringify(entries.slice(0, 100)));
  } catch {
    // Private browsing or a full storage quota must not block segmentation.
  }
}

export function csvCell(value: string | number): string {
  if (typeof value === 'number') return Number.isFinite(value) ? String(value) : '';
  const safe = /^[=+\-@\t\r]/.test(value) ? "'" + value : value;
  return '"' + safe.replace(/"/g, '""') + '"';
}

export function csvText(rows: (string | number)[][]): string {
  return '\ufeff' + rows.map(row => row.map(csvCell).join(',')).join('\r\n') + '\r\n';
}

export function downloadCsv(name: string, rows: (string | number)[][]): void {
  const url = URL.createObjectURL(new Blob([csvText(rows)], { type: 'text/csv;charset=utf-8' }));
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = name;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export function parseCsvRows(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = '';
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    const next = text[i + 1];
    if (char === '"' && quoted && next === '"') {
      cell += '"';
      i += 1;
    } else if (char === '"') {
      quoted = !quoted;
    } else if (char === ',' && !quoted) {
      row.push(cell);
      cell = '';
    } else if ((char === '\n' || char === '\r') && !quoted) {
      if (char === '\r' && next === '\n') i += 1;
      row.push(cell);
      if (row.some(value => value.trim() !== '')) rows.push(row);
      row = [];
      cell = '';
    } else {
      cell += char;
    }
  }
  if (cell !== '' || row.length > 0) {
    row.push(cell);
    if (row.some(value => value.trim() !== '')) rows.push(row);
  }
  return rows;
}
