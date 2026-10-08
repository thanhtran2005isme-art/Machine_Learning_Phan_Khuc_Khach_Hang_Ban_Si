export type SpendingFeature = 'Fresh' | 'Milk' | 'Grocery' | 'Frozen' | 'Detergents_Paper' | 'Delicassen';
export type Spending = Record<SpendingFeature, number>;
export type LoadedModel = { model: Record<string, any>; evaluation: Record<string, any>; checksum: string; ranges: Record<string, { min: number; max: number }> };
export const FEATURES: readonly SpendingFeature[];
export function loadModel(options?: { modelPath?: string }): LoadedModel;
export function segment(loaded: LoadedModel, spending: Spending): {
  cluster_id: number; distance_to_centroid: number; distances_to_centroids: number[];
  profile: { name: string; count: number; share: number; median_spending: Spending };
  warnings: string[]; distance_space: string;
};
export function modelInfo(loaded: LoadedModel): Record<string, unknown>;
export function dashboard(loaded: LoadedModel, options?: { profileDir?: string }): Record<string, unknown>;
