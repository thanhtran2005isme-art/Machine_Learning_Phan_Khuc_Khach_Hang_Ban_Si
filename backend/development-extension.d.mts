import type { LoadedModel } from './model.mjs';
export type DevelopmentExtensionPoint = {
  index: number; split: 'train' | 'validation'; pc1: number; pc2: number;
  kmeans: 0 | 1; hierarchical: 0 | 1;
};
export function loadVerifiedDevelopmentExtension(
  loaded: LoadedModel,
  options?: { extensionDir?: string }
): {
  schema_version: number; decision: string; source_scope: string;
  points: DevelopmentExtensionPoint[];
  pca: { explained_variance_ratio: number[]; components: number[][]; method: string; usage: string };
  comparison: {
    frozen_counts: number[]; hierarchical_counts: number[]; contingency: number[][];
    ari: number; silhouette_kmeans: number; silhouette_hierarchical: number;
  };
  read_only: true; test_used: false; development_count: 352;
};
