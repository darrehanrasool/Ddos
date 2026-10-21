# Deep Learning Models Directory

In the multi-dataset defense architecture, specialized deep learning models (DeepResidualMLP PyTorch state dicts)
are organized per network domain in:
  `models/dataset_specialized/<dataset_id>/deep_model.pt`

Active Domain Models:
- `models/dataset_specialized/cic_ids2017/deep_model.pt` (Enterprise Cloud)
- `models/dataset_specialized/sdn_ddos/deep_model.pt` (SDN OpenFlow)
- `models/dataset_specialized/nsl_kdd/deep_model.pt` (Protocol Infrastructure)
- `models/dataset_specialized/bot_iot/deep_model.pt` (Smart Home IoT)
- `models/dataset_specialized/ton_iot/deep_model.pt` (Industrial Telemetry)
- `models/dataset_specialized/cic_ddos2019/deep_model.pt` (Volumetric Reflection)
