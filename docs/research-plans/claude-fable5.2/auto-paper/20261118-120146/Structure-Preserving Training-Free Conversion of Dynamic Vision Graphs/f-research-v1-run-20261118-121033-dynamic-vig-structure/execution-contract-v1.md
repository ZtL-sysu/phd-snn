# Execution contract v1 — f-research-v1

## Goal and scope

- Produce a top-conference-level manuscript from the accepted guidance file, with no tier downgrade after a failed idea.
- Selected method family: training-free ANN-to-SNN conversion for dynamic vision graphs with structure-aware calibration.
- Authorized correction: if the binding strong-result lock fails, open the correction loop, preserve evidence, and activate a versioned replacement from the documented material set; never lower an already failed target merely to pass.
- Local execution only; no remote compute, credentials, commits, pushes, or submission are authorized.
- All process and delivery artifacts remain under the run root.

## Inputs

- Guidance: `..\guidance.md`.
- CCFA packet: `..\ccfa-startup-packet\`.
- Builder state: `..\pipeline-state.json`.
- Local dataset/teacher inventory: `..\local-dataset-availability.md`.

## Writing and edit scope

- edit_scope: full manuscript under this run root.
- protected_sections: none supplied by the user.
- protected_artifacts: frozen experiment JSON/CSV/log artifacts after P5 acceptance.
- declaration_mode: author-managed; no author identity, funding, or conflict declarations are invented.
- allow_new_experiments: yes, within the recorded method family and correction policy.
- Editing-round budget: three; stop after two rounds without fewer concrete defects.

## Author preferences and restrictions

- Formal top-conference English manuscript; Chinese progress communication.
- Preserve negative results and failed attempts.
- Do not copy unlicensed upstream code.
- Do not use historically exposed local official tests as unseen final evidence.
- Do not place workflow logs or submission-process narration in the manuscript.
- Do not add appendices or research content after the six-section conclusion body.

## Resources

- Python: `C:/Users/xhf/miniconda3/envs/dyg-cold/python.exe`.
- PyTorch: 2.11.0+cu128; CUDA available; NVIDIA GeForce RTX 3060 12 GB.
- 12 logical CPUs; about 481 GiB free disk at builder probe.
- Runtime envelope: 24 hours, 8 GB GPU memory, 3 seeds, 12 search trials for the first contract.

## Version

Contract version `v1` is immutable. Any material scope, data, target, or compute change creates `v2` and reopens the affected canonical stages.
