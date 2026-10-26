export type SpendingFeature = 'Fresh' | 'Milk' | 'Grocery' | 'Frozen' | 'Detergents_Paper' | 'Delicassen';
export type Spending = Record<SpendingFeature, number>;
export type Profile = {
  name: string;
  count: number;
  share: number;
  median_spending: Spending;
};
export type DecisionSupport = {
  status: 'descriptive' | 'review';
  priority: 'low' | 'medium' | 'high';
  reason_codes: string[];
  title: string;
  action: string;
  rationale: string;
};
export type LoadedModel = {
  model: Record<string, any>;
  evaluation: Record<string, any>;
  checksum: string;
  ranges: Record<string, { min: number; max: number }>;
};
export const FEATURES: readonly SpendingFeature[];
export function loadModel(options?: { modelPath?: string }): LoadedModel;
export function segment(loaded: LoadedModel, spending: Spending): {
  cluster_id: number;
  distance_to_centroid: number;
  distances_to_centroids: number[];
  distance_gap: number;
  relative_margin: number;
  distance_ratio_to_development_rms: number;
  out_of_train_range_features: SpendingFeature[];
  profile: Profile;
  alternative_profile: Profile;
  warnings: string[];
  decision_support: DecisionSupport;
  distance_space: string;
};
export type ModelInfo = {
  diagnostic_policy: {
    near_boundary_relative_margin: number;
    high_distance_ratio_to_development_rms: number;
    development_rms_distance: number;
    note: string;
  };
};
export function modelInfo(loaded: LoadedModel): ModelInfo & Record<string, unknown>;
export function dashboard(loaded: LoadedModel, options?: { profileDir?: string }): Record<string, unknown>;
