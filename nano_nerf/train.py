from utils import compute_rays, compute_query_points, encoding_fun, get_batches, render_volume
def train_iter(height,
               width,
               focal_len,
               cam2world,
               near,
               far,
               samples,
               encoding_fun,
               model):
  ray_directions, ray_origins = compute_rays(height,
  width,
  focal_len,
  cam2world)
  query_points, depth_values = compute_query_points(
      ray_origins,
      ray_directions,
      near,
      far,
      samples)
  query_points = query_points.reshape((-1,3))
  encoded_points = encoding_fun(query_points)
  batches =  get_batches(encoded_points)
  predictions = []
  for batch in batches:
      predictions.append(model(batch))
  radiance_field = torch.cat(predictions,dim=0)
  shape = list(query_points.shape[:-1]) + [4]
  radiance_field = torch.reshape(radiance_field, shape)
  rgb_pred = render_volume(radiance_field, ray_origins, depth_values)

  return rgb_pred