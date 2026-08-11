# CVPR 2027 Problem Statement Ideas — 4D Surface Reconstruction

> **Generated from analysis of 16 papers in the 4D surface / dynamic scene reconstruction literature.**
> Each idea targets a genuine gap identified across the surveyed works.

---

## Table of Contents

| # | Problem Statement (Short Title) | Core Gap | Compute Required | Doability in 3 months | Likelihood of Acceptance in CVPR27 | Paradigm |
|:--|:--|:--|:--|:--|:--|:--|
| 1 | [Topology-Changing 4D Surface Reconstruction](#ps-1-topology-changing-4d-surface-reconstruction) | Every method assumes fixed canonical topology | 4× A100 (~2k-3k hrs) | Medium-High | High (75–85%) | Per-Scene |
| 2 | [Physics-Informed 4D Gaussian Surface Dynamics](#ps-2-physics-informed-4d-gaussian-surface-dynamics) | No physics priors in current 4D methods | 4× A100 (~2.5k-4k hrs) | Medium | High (70–80%) | Per-Scene |
| 3 | [Foundation-Model-Driven 4D Surface Prior](#ps-3-foundation-model-driven-4d-surface-prior) | All methods are per-scene optimized from scratch | 8-16× A100/H100 (~8k-15k hrs) | Low-Medium | Very High (80–90%) | Generalisable |
| 4 | [Monocular 4D Surface Reconstruction without Templates](#ps-4-monocular-4d-surface-reconstruction-without-templates) | Sparse-view surface methods need multi-view | 2-4× A100 (~1k-2k hrs) | High | High (75–85%) | Per-Scene |
| 5 | [4D Surface Reconstruction from Event Cameras](#ps-5-4d-surface-reconstruction-from-event-cameras) | Entire field assumes conventional frame-based cameras | 2-4× A100 (~1.5k-2.5k hrs) | Medium | Medium-High (65–75%) | Per-Scene |
| 6 | [Unified Static-Dynamic 4D Surface SLAM](#ps-6-unified-static-dynamic-4d-surface-slam) | SLAM methods discard dynamics or don't extract surfaces | 2-4× RTX4090/A100 (~1.5k-2k hrs) | Medium-High | High (75–85%) | Per-Scene |
| 7 | [4D Surface Completion via Diffusion from Partial Observations](#ps-7-4d-surface-completion-via-diffusion-from-partial-observations) | No generative completion for dynamic surfaces | 4-8× A100 (~3k-5k hrs) | Medium | High (70–80%) | Generalisable |
| 8 | [Text/Language-Guided 4D Surface Editing](#ps-8-textlanguage-guided-4d-surface-editing) | 4D editing is limited to NeRF/GS appearance, not surfaces | 4-8× A100 (~2k-4k hrs) | Medium | Medium-High (65–75%) | Both |
| 9 | [Category-Agnostic Articulated 4D Surface Reconstruction](#ps-9-category-agnostic-articulated-4d-surface-reconstruction) | Methods are either category-specific or fully general | 2-4× A100 (~1.5k-2.5k hrs) | High | High (70–80%) | Per-Scene |
| 10 | [Temporal Super-Resolution for 4D Surfaces](#ps-10-temporal-super-resolution-for-4d-surfaces) | No method synthesizes in-between surface frames | 2-4× A100 (~1k-2k hrs) | High | Medium-High (65–75%) | Per-Scene |
| 11 | [4D Surface Reconstruction of Transparent / Refractive Objects](#ps-11-4d-surface-reconstruction-of-transparent--refractive-objects) | All methods assume opaque Lambertian surfaces | 2-4× A100 (~1.5k-2.5k hrs) | Medium | Medium (55–70%) | Per-Scene |
| 12 | [Self-Supervised 4D Surface from Unlabeled Web Videos](#ps-12-self-supervised-4d-surface-from-unlabeled-web-videos) | All methods require calibrated multi-view setups | 16-32× A100/H100 (~10k-20k hrs) | Low | Very High (80–90%) | Generalisable |
| 13 | [Multi-Entity Compositional 4D Surface Reconstruction](#ps-13-multi-entity-compositional-4d-surface-reconstruction) | Methods model scenes monolithically | 4× A100 (~2k-3k hrs) | High | High (70–80%) | Per-Scene |
| 14 | [Neural Jacobian Fields for Simulation-Ready 4D Meshes](#ps-14-neural-jacobian-fields-for-simulation-ready-4d-meshes) | Extracted meshes can't be used in physics simulators | 2-4× A100 (~1.5k-2.5k hrs) | Medium-High | High (70–80%) | Per-Scene |
| 15 | [4D Surface Gaussian Splatting with Adaptive Topology Remeshing](#ps-15-4d-surface-gaussian-splatting-with-adaptive-topology-remeshing) | No online mesh adaptation during 4DGS optimization | 2-4× A100 (~1k-2k hrs) | High | Medium-High (65–75%) | Per-Scene |

---

## PS 1: Topology-Changing 4D Surface Reconstruction

### Problem Statement

**Every existing 4D surface reconstruction method (DySurface, 4DSurf, DynaSurfGS, TextMesh4D, Motion2VecSets, Unbiased4D) fundamentally assumes that the scene maintains a fixed canonical topology throughout the entire temporal sequence.** This means they universally fail on scenes involving fracturing, tearing, merging, splashing, growth, or dissolution — deformations that break the homeomorphism between the canonical and deformed space. This is not a minor limitation: it excludes entire categories of real-world phenomena (cooking, surgery, manufacturing, natural disasters, biological growth) from reconstruction.

The core challenge is that SDFs and canonical-space formulations inherently enforce watertight, fixed-genus surfaces. Once a single canonical mesh is extracted (via Marching Cubes), no existing deformation field can split it into two disjoint pieces or merge two pieces into one.

### Ideas

1. **Level-Set Evolution + Gaussian Dynamics:** Replace the static canonical SDF with a time-evolving level-set field that can naturally undergo topological changes (splitting/merging) via the Hamilton-Jacobi equation. Couple this with explicit Gaussians that track the evolving zero-level set, so the Gaussians can be split or merged when the level-set topology changes. The key insight: level-set methods from computational physics natively handle topology changes — they've just never been married to Gaussian Splatting.

2. **Multi-Canonical-Space Handoff:** Instead of one canonical space for the entire sequence, maintain a *graph of canonical spaces* connected by transition operators. When the system detects a topology change (e.g., via a learned topology-change classifier operating on the SDF gradient field), it spawns a new canonical space from the current state and begins optimizing separately. Adjacent canonical spaces share an overlapping transition region for smooth interpolation.

3. **Implicit Surface Unions via Constructive Solid Geometry (CSG):** Represent the dynamic scene as a CSG tree of simple implicit primitives. Topology changes correspond to CSG operations (union → merge, difference → tear). Learn the CSG tree structure and primitive deformations jointly. This provides interpretable topology changes with explicit operation semantics.

### Datasets

- **D-FAUST** (CVPR 2017) — human bodies, though topology-preserving; useful for baseline comparison.
- **DeformingThings4D** (NeurIPS 2021) — animated mesh sequences; can be augmented with synthetic fracture/merge events.
- **Custom Synthetic Dataset (Blender/Houdini):** Generate physics-simulated sequences of tearing cloth, shattering glass, splashing fluids, growing plants using Houdini's FLIP/Vellum solvers. Export ground-truth meshes with known topology changes.
- **ScanNet++** or equivalent RGB-D captures of real topology-changing events (pouring liquids, tearing paper).

### Compute Required

- **GPUs:** 4× NVIDIA A100 (80GB)
- **Estimated GPU Hours:** ~2,000–3,000 hours total (synthetic data generation + level-set training + baseline comparisons)

### Doability in 3 Months

**Medium-High.** The level-set evolution formulation is well-understood in computational physics (Osher & Fedkiw). The main risk is making the level-set ↔ Gaussian coupling differentiable and stable. Synthetic data generation via Houdini is straightforward. The multi-canonical handoff idea is simpler to implement but less elegant theoretically.

### Likelihood of Acceptance at CVPR 2027

**High (75–85%).** Topology change is the single most cited limitation across all surveyed papers (DySurface, TextMesh4D, 4DSurf, Motion2VecSets, Unbiased4D all explicitly list it). A principled solution would be highly impactful. Risk: the problem is genuinely hard, so the method must show clear improvements on non-trivial topology-changing sequences, not just toy examples.

---

## PS 2: Physics-Informed 4D Gaussian Surface Dynamics

### Problem Statement

**Current 4D surface reconstruction methods learn motion purely from photometric supervision, without any understanding of the physical laws governing the dynamics.** Deformation fields (MLP-based or velocity-based) are unconstrained black boxes that can produce physically implausible motions: surfaces can self-intersect, violate conservation of momentum, stretch beyond material limits, or pass through each other. This limits downstream applications in simulation, robotics, and digital twins where physical realism is essential.

DySurface demonstrated a cloth-collision experiment but treated physics as a post-hoc application rather than an inductive bias. No existing method embeds physical constraints (elasticity, gravity, collision) *into* the reconstruction optimization itself.

### Ideas

1. **Differentiable Physics Loss for 4DGS:** Add physics-based regularization losses during 4DGS optimization: (a) a Neo-Hookean elastic energy loss penalizing non-physical strain in the Gaussian velocity field (from 4DSurf), (b) a collision detection loss using signed distance queries between Gaussian clusters, (c) a gravitational consistency loss ensuring free-falling objects follow parabolic trajectories. These losses act as soft priors, not hard constraints, allowing the photometric loss to still dominate.

2. **Material-Conditioned Deformation Networks:** Extend the deformation MLP to accept a per-Gaussian material embedding (e.g., rigid, elastic, fluid). The material embedding modulates the deformation field's capacity: rigid materials get near-SE(3) constraints, elastic materials get strain-limited deformations, fluid materials get divergence-free velocity fields. Learn material labels from visual appearance or assign them via a material segmentation network.

3. **Neural Physics Residual:** Train a standard 4DGS first (Stage 1). Then train a physics simulator (e.g., a GNN-based particle simulator like GNS) to predict the next-frame Gaussian positions from current positions + velocities. The residual between the physics prediction and the photometric-optimized positions reveals where physics is violated. Use this residual to fine-tune the deformation field (Stage 2) toward physical plausibility.

### Datasets

- **D-NeRF** (synthetic, simple motions) — baseline comparison.
- **Hi4D** (CVPR 2023) — interacting humans with contacts/collisions.
- **InterCap** (GCPR 2022) — human-object interaction with ground-truth contact.
- **Custom Synthetic Physics Scenes:** Blender/Houdini with known material parameters, forces, and ground-truth physics trajectories.
- **CMU Panoptic** — multi-person interactions.

### Compute Required

- **GPUs:** 4× NVIDIA A100 (80GB)
- **Estimated GPU Hours:** ~2,500–4,000 hours (physics simulation is cheap; the differentiable physics integration into GS training is the expensive part)

### Doability in 3 Months

**Medium.** The differentiable physics loss approach (Idea 1) is quite feasible — it's adding regularization terms, not building a full simulator. The material-conditioned network (Idea 2) requires careful architecture design. The neural physics residual (Idea 3) is the most ambitious and might need more time. Recommend starting with Idea 1.

### Likelihood of Acceptance at CVPR 2027

**High (70–80%).** Physics-informed learning is a hot topic across ML, and applying it to 4D surfaces is timely. The narrative of "reconstruction for simulation" is compelling for robotics/embodied AI audiences. Risk: showing that physics priors actually improve reconstruction quality (not just physical plausibility) requires careful experimental design.

---

## PS 3: Foundation-Model-Driven 4D Surface Prior

### Problem Statement

**All current 4D surface reconstruction methods optimize each scene from scratch, requiring minutes to hours per scene and producing no transferable knowledge.** While ReconDrive demonstrated feed-forward 4D Gaussian prediction for driving scenes using a frozen VGGT backbone, it (a) only handles rigid/linear vehicle motion, (b) produces Gaussians without surface constraints, and (c) is limited to the autonomous driving domain. There is no general-purpose 4D surface foundation model that can reconstruct dynamic surfaces in a single forward pass across diverse scene types.

### Ideas

1. **4D Surface Transformer:** Build a transformer-based architecture that takes multi-view video frames as input and directly predicts per-frame surface representations (e.g., deformation latent sets à la Motion2VecSets, or 2DGS parameters with surface normals). Pre-train on a massive synthetic 4D dataset (Objaverse-4D + DeformingThings4D + synthetic humans). Fine-tune with LoRA on specific domains. Key architectural innovations: (a) Cross-view spatial attention for multi-view fusion, (b) Temporal attention across frames for motion modeling, (c) Surface-aware prediction heads that output SDF values or 2DGS disk parameters rather than vanilla 3DGS.

2. **4D Surface Diffusion Prior with Score Distillation:** Train a 4D surface diffusion model on paired (point cloud sequence → mesh sequence) data. At test time, use Score Distillation Sampling (SDS) to distill this learned prior into a per-scene 4DGS optimization. This combines the generalizability of the diffusion prior with the per-scene fidelity of optimization. Crucially, the diffusion prior operates on *surface* representations (SDF latents or mesh Jacobians from TextMesh4D), not images.

3. **Video Foundation Model → 4D Surface Lifting:** Leverage a large pre-trained video generation model (e.g., a Sora-class model) as a 4D prior. Given sparse input views, use the video model to hallucinate dense novel spatio-temporal views. Then run a fast per-scene 4D surface optimization (e.g., 4DSurf) on the hallucinated + real views jointly. The video model provides the multi-view/temporal prior that sparse inputs lack.

### Datasets

- **Objaverse** (CVPR 2023) + animated extensions — millions of 3D objects, subset with animations.
- **DeformingThings4D** (NeurIPS 2021) — 1,972 animation sequences.
- **D-FAUST** — dynamic human meshes.
- **RenderMe-360** — multi-view human performance capture.
- **Hi4D**, **CMU Panoptic** — multi-view real-world dynamics.
- Pre-training on large-scale synthetic rendering is essential.

### Compute Required

- **GPUs:** 8–16× NVIDIA A100/H100 (80GB)
- **Estimated GPU Hours:** ~8,000–15,000 hours (dominated by pre-training the foundation model on large-scale synthetic data; fine-tuning and inference are cheap)

### Doability in 3 Months

**Low-Medium.** Pre-training a foundation model is compute-intensive and requires significant data engineering. The most feasible variant is Idea 2 (diffusion prior + SDS), which can be trained on existing datasets in ~3,000 GPU hours. Idea 3 (video model lifting) is feasible if using an existing pre-trained video model (no training needed for the video model itself). Idea 1 requires the most infrastructure.

### Likelihood of Acceptance at CVPR 2027

**Very High (80–90%) if executed well.** Foundation models for 3D/4D are the hottest topic in the field. A generalizable 4D surface model that works across domains would be a landmark contribution. Even a well-executed version of Idea 2 or 3 would be highly competitive. Risk: the bar for "foundation model" papers is very high — it must convincingly generalize, not just overfit to the training distribution.

---

## PS 4: Monocular 4D Surface Reconstruction without Templates

### Problem Statement

**Reconstructing temporally consistent, watertight dynamic surfaces from a single monocular RGB video — without any template, category prior, or depth sensor — remains unsolved.** Unbiased4D (CVPR 2023) addressed monocular 4D reconstruction but (a) used implicit NeRF-based rendering (slow), (b) required an optional skeleton proxy for large motions, and (c) produced SDFs without explicit mesh tracking. Meanwhile, newer 4DGS methods (4DSurf, DySurface) achieve excellent surface quality but require multi-view input. Bridging these — bringing 4DGS-quality surfaces to monocular input — is a critical open problem for in-the-wild applications (smartphone videos, legacy footage, surveillance).

### Ideas

1. **Monocular Depth + Flow → Pseudo-Multi-View 4D Surface Optimization:** Given a monocular video, use foundation models to extract (a) per-frame monocular depth (Depth Anything V2), (b) dense optical flow (RAFT/UniMatch), (c) camera poses (DROID-SLAM or PoseDiffusion). Treat these as pseudo-multi-view supervision: depth provides scale-ambiguous geometry, flow provides temporal correspondence, and the camera trajectory provides virtual baselines. Run a 4DGS surface optimization (building on 4DSurf's SDF flow regularization) with these pseudo-labels. Key innovation: a **scale-consistent depth alignment module** that resolves the per-frame scale ambiguity of monocular depth estimators using the optical flow as a temporal consistency anchor.

2. **Monocular 4D Surface via Test-Time Diffusion Adaptation:** Train a 4D surface diffusion model (Motion2VecSets-style) on synthetic data. At test time, given a monocular video, use the frozen diffusion model's denoising score as a regularizer during per-frame SDF optimization. The diffusion prior handles ambiguous/occluded regions by generating plausible surface completions, while the photometric loss from the video anchors visible regions.

3. **Canonical 2DGS + Monocular Geometric Cues:** Optimize a set of canonical 2D Gaussian Surfel disks that are deformed per-frame. Supervise with: (a) RGB photometric loss, (b) rendered normal vs. monocular normal estimation (Metric3D/Marigold), (c) rendered depth vs. monocular depth, (d) rendered optical flow (from 3D Gaussian displacement, as in 4DGS-SLAM) vs. estimated optical flow. The 2DGS representation naturally provides surface normals and tight geometric coupling.

### Datasets

- **iPhone dataset** (Nerfies/HyperNeRF) — monocular casual captures.
- **DAVIS** (video object segmentation) — high-quality monocular videos with masks.
- **Sintel** — synthetic with GT depth, flow, and camera.
- **iPhone-4D** (from Sparse4DGS) — monocular dynamic scenes.
- **RealCactus / Humanoid** (from Unbiased4D) — monocular with GT meshes.
- **TAP-Vid** — videos with dense point tracks for evaluation.

### Compute Required

- **GPUs:** 2–4× NVIDIA A100 (80GB)
- **Estimated GPU Hours:** ~1,000–2,000 hours (per-scene optimization is efficient; the main cost is ablation studies across many scenes)

### Doability in 3 Months

**High.** Idea 1 and 3 are very feasible — they combine existing off-the-shelf models with a well-defined 4DGS optimization pipeline. The main engineering challenge is the scale-consistent depth alignment, which is a known problem with existing solutions (e.g., from Consistent Depth of Moving Objects). Idea 2 requires pre-training a diffusion model, which adds complexity.

### Likelihood of Acceptance at CVPR 2027

**High (75–85%).** Monocular 4D is a highly practical and impactful problem. The combination of modern foundation model outputs (depth, flow, normals) as pseudo-labels for 4D surface optimization is timely and well-motivated. Risk: the results may be noisy compared to multi-view methods, requiring careful presentation of when/where the method works best.

---

## PS 5: 4D Surface Reconstruction from Event Cameras

### Problem Statement

**The entire 4D surface reconstruction field assumes conventional frame-based RGB cameras, which suffer from motion blur, limited dynamic range, and fixed temporal resolution.** Event cameras (neuromorphic sensors) offer microsecond-level temporal resolution, high dynamic range, and no motion blur — precisely the properties needed for capturing fast dynamic surfaces (sports, industrial machinery, biological processes). Yet no existing work has explored 4D surface reconstruction from event streams.

### Ideas

1. **Event-Driven 4D Gaussian Splatting:** Design a continuous-time 4DGS framework where Gaussian deformations are parameterized as continuous splines (rather than discrete per-frame offsets). Events trigger local updates to the spline control points of nearby Gaussians. Supervision comes from: (a) the event generation model (brightness change ↔ event), (b) optional sparse intensity frames from a DAVIS-style hybrid sensor. Surface extraction via 2DGS surfel fitting with SDF regularization.

2. **Event Flow → 4D Surface Flow:** Events naturally encode brightness changes that correspond to surface motion. Compute dense event-based optical flow (via contrast maximization or learned methods). Use this as direct supervision for the Gaussian velocity field (analogous to how 4DSurf uses RGB-derived SDF flow). The key advantage: event-based flow is defined at arbitrary temporal resolution, enabling continuous-time surface tracking.

3. **Hybrid Event-Frame 4D Surface:** Use sparse keyframes (from the DAVIS sensor's APS) for coarse 4D surface initialization, then refine the inter-keyframe motion at microsecond resolution using the event stream. This avoids the chicken-and-egg problem of pure event-based reconstruction.

### Datasets

- **EDS (Event-aided Direct Sparse Odometry)** dataset — stereo events + frames.
- **DSEC** (autonomous driving event dataset) — stereo events with LiDAR GT.
- **HQF** (High Quality Frames) dataset — events + sharp frames.
- **Custom Synthetic Events:** Render synthetic dynamic scenes (from D-NeRF or DeformingThings4D) through an event camera simulator (ESIM, v2e) to generate paired GT meshes + event streams.

### Compute Required

- **GPUs:** 2–4× NVIDIA A100 (80GB)
- **Estimated GPU Hours:** ~1,500–2,500 hours (event processing is lightweight; the main cost is the 4DGS optimization and event simulation)

### Doability in 3 Months

**Medium.** The main challenge is the lack of established datasets with event streams + ground-truth dynamic surfaces. Synthetic event simulation (ESIM) is well-established and feasible. The continuous-time spline formulation for Gaussians is novel but builds on existing work (CubicSplat, EventNeRF). Hybrid event-frame (Idea 3) is the most feasible starting point.

### Likelihood of Acceptance at CVPR 2027

**Medium-High (65–75%).** Event cameras are a growing area at CVPR, and "event camera + Gaussian Splatting" is a relatively unexplored intersection. The novelty of applying events to *dynamic surface* reconstruction (not just novel view synthesis) adds differentiation. Risk: the CVPR community may perceive event cameras as niche; strong qualitative results on fast-motion scenes are essential to demonstrate the advantage over frame-based methods.

---

## PS 6: Unified Static-Dynamic 4D Surface SLAM

### Problem Statement

**4D Gaussian Splatting SLAM (ICCV 2025) demonstrated dynamic scene modeling within SLAM but (a) does not extract explicit surfaces, (b) relies on RGB-D input (depth sensor), (c) depends on pre-trained YOLO and RAFT models for dynamic segmentation, and (d) uses a simple MLP deformation that cannot scale to complex multi-object motions.** Meanwhile, 4D surface methods (DySurface, 4DSurf) achieve excellent surface quality but assume known camera poses and offline processing. Unifying SLAM (online, unknown poses) with 4D surface reconstruction (high-quality meshes of both static and dynamic elements) in a single framework is an open challenge critical for robotics, AR/VR, and autonomous navigation.

### Ideas

1. **4D Surface SLAM with SDF Flow Tracking:** Build on MonoGS-style Gaussian SLAM, but replace vanilla 3DGS with 2DGS surfels + SDF regularization (from 4DSurf). For dynamics: instead of relying on external YOLO segmentation, use the residual between the predicted static depth and the observed depth as a self-supervised dynamic mask (inspired by DeSiRe-GS's "failure-as-signal" insight). Model dynamic Gaussians with a lightweight velocity field (from 4DSurf) and use rendered optical flow (from 4DGS-SLAM) for kinematic supervision. Extract watertight meshes of both static background and dynamic objects in real-time.

2. **Panoptic 4D Surface SLAM:** Extend the dynamic SLAM to panoptic understanding: simultaneously estimate (a) camera pose, (b) static background surface, (c) per-object dynamic surfaces with instance IDs, (d) per-object SE(3) rigid motions + non-rigid residual deformations. Use SAM2 for initial instance segmentation, then track instances via Gaussian association across frames. Each instance maintains its own canonical 2DGS surface representation.

### Datasets

- **TUM RGB-D** — indoor dynamic scenes with ground-truth poses.
- **BONN** — dynamic RGB-D dataset.
- **ScanNet / ScanNet++** — indoor scenes (static, but useful for surface evaluation).
- **Replica** — synthetic indoor with perfect GT.
- **KITTI** — outdoor driving with ground-truth poses and LiDAR.
- **Custom: Simulated dynamic indoor scenes** in Habitat/iGibson.

### Compute Required

- **GPUs:** 2–4× NVIDIA RTX 4090 or A100
- **Estimated GPU Hours:** ~1,500–2,000 hours (SLAM is inherently online/sequential, making parallelization less effective; but individual scenes are fast)

### Doability in 3 Months

**Medium-High.** Building on existing MonoGS/SplaTAM codebases and adding 2DGS surface constraints + velocity fields is architecturally straightforward. The self-supervised dynamic mask (from DeSiRe-GS insight) eliminates the YOLO dependency. The main engineering challenge is making the system run in real-time (or near-real-time) while maintaining surface quality.

### Likelihood of Acceptance at CVPR 2027

**High (75–85%).** SLAM + Gaussian Splatting is one of the hottest sub-areas. Adding surface extraction and removing the dependency on external foundation models (YOLO, RAFT) for self-supervised decomposition would be a strong contribution. Risk: SLAM papers require extensive quantitative evaluation on standard benchmarks with many baselines; this is engineering-intensive.

---

## PS 7: 4D Surface Completion via Diffusion from Partial Observations

### Problem Statement

**All current 4D surface reconstruction methods produce surfaces only where there is sufficient multi-view photometric evidence. Occluded, unseen, or partially observed regions are left as holes, artifacts, or blurred approximations.** Motion2VecSets (CVPR 2024) showed that diffusion models can complete *static* shapes from partial point clouds, but no method extends this to *temporally consistent* 4D surface completion — hallucinating plausible complete surface sequences from partial observations.

This is critical for practical applications: a person captured from the front should have a plausible backside at every timestep; an object emerging from behind another should be complete before it's fully visible.

### Ideas

1. **4D Surface Completion Diffusion Transformer (4D-SCDiT):** Extend Motion2VecSets' latent vector set diffusion to a full 4D completion framework. Architecture: (a) Encode observed partial surfaces at each timestep into shape latent sets, (b) Encode deformation fields into motion latent sets, (c) Run a joint diffusion process with Interleaved Spatio-Temporal Attention (ISTA from Motion2VecSets) conditioned on the partial observations. Key novelty: the denoising process generates *both* the completed shape and the motion simultaneously, ensuring the completed regions are temporally coherent.

2. **Surface Inpainting with 4DGS:** For regions where Gaussians have low confidence (few training views, low opacity, high variance), use a learned surface inpainting network. This network takes the confident Gaussians' positions + normals as boundary conditions and predicts plausible surface patches to fill the gaps. Train on synthetic data where GT full surfaces are available and artificial occlusions are simulated.

3. **Symmetry-Aware 4D Surface Completion:** Exploit the observation that many real-world objects (humans, animals, vehicles) have approximate bilateral symmetry. Given the visible half of a dynamic object, reflect the reconstructed Gaussians through the learned symmetry plane to initialize the occluded half, then refine with temporal consistency losses.

### Datasets

- **D-FAUST** — ground-truth complete human meshes; simulate occlusion by masking views.
- **DeformingThings4D** — complete animated meshes; simulate partial observations.
- **BEHAVE** — human-object interaction with heavy mutual occlusion.
- **Hi4D** — two interacting humans with inter-person occlusion.
- Self-occluded monocular sequences from Nerfies/HyperNeRF.

### Compute Required

- **GPUs:** 4–8× NVIDIA A100 (80GB)
- **Estimated GPU Hours:** ~3,000–5,000 hours (diffusion model training on 4D data is the main cost)

### Doability in 3 Months

**Medium.** Idea 1 is the most ambitious (requires training a 4D diffusion model from scratch). Idea 2 (surface inpainting) is more tractable as a localized network. Idea 3 (symmetry) is the simplest and could serve as a strong baseline. A pragmatic approach: implement Idea 3 as a baseline, then show Idea 2 as the main contribution.

### Likelihood of Acceptance at CVPR 2027

**High (70–80%).** Completion/inpainting for 3D is well-established, but extending it to *4D surfaces with temporal consistency* is novel. The practical value (complete reconstructions from incomplete observations) is immediately compelling. Risk: generative completion can produce hallucinated geometry that doesn't match reality; careful evaluation protocols (measuring plausibility vs. accuracy) are needed.

---

## PS 8: Text/Language-Guided 4D Surface Editing

### Problem Statement

**TextMesh4D (ICML 2026) demonstrated text-to-4D mesh generation from scratch, but there is no method for *editing* an existing reconstructed 4D surface using text instructions.** Imagine reconstructing a dynamic scene and then saying "make the person's shirt turn into armor" or "add a cape that flows in the wind" or "make the walking motion faster and bouncier." Current 4D editing methods (if they exist) operate on NeRF/GS appearance only, not on the explicit surface geometry.

### Ideas

1. **Text-Guided 4D Surface Deformation via Jacobian SDS:** Given a reconstructed 4DGS surface (from DySurface or 4DSurf), use TextMesh4D's Jacobian Deformation Field to apply text-guided edits. Freeze the appearance and optimize only the per-face Jacobians using Video Score Distillation (VSD) from a video diffusion model, conditioned on the editing text prompt. The Poisson solver ensures the edited surface remains watertight and smooth. Key novelty over TextMesh4D: operating on a *reconstructed* scene (not from scratch) and preserving the original identity/appearance while modifying geometry and motion.

2. **Instruction-Following 4D Surface Editor:** Train an instruction-following model (fine-tuned LLM or VLM) that takes as input: (a) a text instruction, (b) rendered video of the current 4D surface, and outputs: (c) per-frame Gaussian attribute modifications (position offsets, scale changes, opacity masks for additions/deletions). Train on synthetic paired data (original 4D scene + edited 4D scene + text description of edit).

3. **Part-Aware 4D Surface Editing:** Use SAM/DINO to segment the reconstructed 4D surface into semantic parts (head, arms, torso, legs). Allow text-guided editing that is grounded to specific parts: "elongate the arms" → apply stretch deformation only to arm-labeled Gaussians. Part segmentation enables fine-grained, semantically meaningful edits.

### Datasets

- **Existing 4D reconstructions** from D-NeRF, Hi4D, CMU Panoptic.
- **Synthetic Edit Pairs:** Use Blender to create (original animation, edited animation, text description) triplets for training.
- **InstructPix2Pix-style paired data** extended to 4D.

### Compute Required

- **GPUs:** 4–8× NVIDIA A100 (80GB)
- **Estimated GPU Hours:** ~2,000–4,000 hours (VSD optimization is expensive per-scene; training the instruction model requires more compute)

### Doability in 3 Months

**Medium.** Idea 1 (Jacobian SDS on existing surfaces) is the most feasible — it directly combines TextMesh4D's machinery with existing 4D reconstruction outputs. Idea 2 requires paired training data, which is harder to obtain. Idea 3 (part-aware) can be built on top of Idea 1.

### Likelihood of Acceptance at CVPR 2027

**Medium-High (65–75%).** 4D editing is a natural next step after 4D generation, and CVPR has been receptive to editing papers. The narrative of "reconstruct → edit → simulate" is compelling. Risk: text-guided 3D/4D editing results are often noisy or inconsistent; the paper needs convincing qualitative results and a strong user study.

---

## PS 9: Category-Agnostic Articulated 4D Surface Reconstruction

### Problem Statement

**Current methods are either fully category-specific (using SMPL for humans, SMAL for animals) or fully category-agnostic but struggle with articulated motions.** Category-specific methods (e.g., using SMPL) produce excellent results for their target category but fail on novel object types. Category-agnostic methods (4DSurf, DySurface) model deformation as a generic continuous field but have no notion of articulated structure — they treat a walking robot the same as flowing water. This leads to unnecessary capacity waste and physically implausible inter-part motions for articulated objects.

### Ideas

1. **Automatic Skeleton Discovery + Skinning for 4DGS:** During the 4DGS optimization, simultaneously discover a skeleton (graph of joints) and skinning weights. Method: (a) Group Gaussians with correlated motion (like SpeeDe3DGS's GroupFlow), (b) Fit an articulated skeleton to these groups via spectral clustering on the motion correlation matrix, (c) Replace the MLP deformation with Linear Blend Skinning (LBS) driven by per-joint rotation parameters. The discovered skeleton provides interpretable, editable articulation. Key insight: SpeeDe3DGS's GroupFlow already clusters Gaussians by motion — extending this to discover hierarchical articulation (not just flat groups) is a natural next step.

2. **Neural Part-Based Canonical Spaces:** Instead of one canonical space for the whole scene, maintain per-part canonical spaces connected by articulation joints. Each part has its own 2DGS surfel set and SDF. Parts are discovered automatically from motion analysis. This is a structured version of MAPo's temporal partitioning, but in the spatial (part) domain rather than the temporal domain.

3. **Category-Agnostic 4D Surface via Structure-from-Motion-Field:** Estimate a dense 3D motion field from multi-view video. Decompose this field into a locally-rigid articulated component (discovered joints + skinning) and a non-rigid residual. Reconstruct the surface using 2DGS with the articulated prior providing strong geometric regularization.

### Datasets

- **DeformingThings4D** — diverse animated objects (animals, humanoids, robots) with GT meshes and articulations.
- **D-FAUST** — humans (for comparison with SMPL-based methods).
- **AMA (Articulated Mesh Animation)** — diverse articulated objects.
- **ARCTIC** (CVPR 2023) — hands interacting with articulated objects.
- **HOI4D** — human-object interaction with diverse articulated objects.
- **Custom: Articulated Robot Captures** using multi-view setup.

### Compute Required

- **GPUs:** 2–4× NVIDIA A100 (80GB)
- **Estimated GPU Hours:** ~1,500–2,500 hours

### Doability in 3 Months

**High.** The core idea (GroupFlow clustering → skeleton fitting → LBS deformation) is algorithmically well-understood. Spectral clustering on motion correlations is straightforward. The main challenge is making the skeleton discovery differentiable and end-to-end trainable with the 4DGS optimization. A two-stage approach (optimize 4DGS, then fit skeleton) is very feasible.

### Likelihood of Acceptance at CVPR 2027

**High (70–80%).** Bridging the gap between category-specific and category-agnostic methods is a well-motivated problem. Automatic skeleton discovery from 4DGS is novel and immediately useful for downstream applications (animation retargeting, editing). Risk: the discovered skeletons must be meaningful and robust across diverse object categories; a failure on simple cases would undermine the contribution.

---

## PS 10: Temporal Super-Resolution for 4D Surfaces

### Problem Statement

**Current 4D surface methods reconstruct surfaces only at the input video's frame rate. No method addresses temporal super-resolution: synthesizing physically plausible in-between surface frames at arbitrarily high temporal resolution.** This is crucial for slow-motion rendering, physics simulation (which requires sub-millisecond timesteps), and temporal upsampling of low-FPS captures. Sparse4DGS (AAAI 2026) handles sparse spatial frames but does not address temporal interpolation of surfaces.

### Ideas

1. **Neural Surface ODE for Continuous-Time 4D Surfaces:** Model the temporal evolution of the 4D Gaussian surface as a Neural ODE: dG/dt = f_θ(G, t), where G is the full Gaussian state and f_θ is a learned velocity field (extending 4DSurf's Gaussian Velocity Field). Train on observed frames; at inference, integrate the ODE to any desired timestep using adaptive Runge-Kutta solvers. The Neural ODE naturally provides continuous-time interpolation and can be queried at arbitrary temporal resolution.

2. **4D Surface Frame Interpolation Network:** Train a network that takes two temporally adjacent reconstructed surface frames (as Gaussian parameter sets or mesh vertex positions) and predicts an intermediate surface frame. Use a learned interpolation in the *surface* space, not the image space. Architecturally, this could be an attention-based network operating on Gaussian attributes, inspired by the Interleaved Spatio-Temporal Attention from Motion2VecSets.

3. **Velocity-Field Extrapolation + Physics Correction:** Use the trained Gaussian velocity field from 4DSurf to extrapolate Gaussian positions to intermediate timesteps (simple Euler integration). Then apply physics-based corrections: (a) collision resolution (surfaces shouldn't self-intersect), (b) ARAP energy minimization (from DynaSurfGS) to maintain local rigidity, (c) Laplacian smoothing to prevent surface noise amplification during extrapolation.

### Datasets

- **D-NeRF** (synthetic, known GT at arbitrary timesteps by re-rendering).
- **Neural 3D Video** (Neu3DV) — high-FPS multi-view captures (can downsample and use original as GT).
- **Hi4D** — 30 FPS captures (downsample to 10 FPS input, evaluate interpolation to 30 FPS GT).
- **Technicolor** — multi-view high-speed captures.
- **Custom High-Speed Captures** using synchronized high-speed cameras.

### Compute Required

- **GPUs:** 2–4× NVIDIA A100 (80GB)
- **Estimated GPU Hours:** ~1,000–2,000 hours

### Doability in 3 Months

**High.** The Neural ODE formulation (Idea 1) is well-supported by existing libraries (torchdiffeq). 4DSurf's Gaussian Velocity Field already provides the continuous-time derivative — the main contribution is formalizing it as an ODE, training it for interpolation accuracy, and demonstrating high-quality temporal super-resolution. Idea 3 (velocity extrapolation + physics) is even simpler.

### Likelihood of Acceptance at CVPR 2027

**Medium-High (65–75%).** Temporal super-resolution is an important and under-explored problem in 4D surfaces. The Neural ODE angle provides strong theoretical grounding. Risk: if the interpolated surfaces are only marginally better than naive linear interpolation of vertex positions, the contribution feels weak. Need to show results on fast/complex motions where linear interpolation clearly fails.

---

## PS 11: 4D Surface Reconstruction of Transparent / Refractive Objects

### Problem Statement

**All 4D surface reconstruction methods assume opaque, approximately Lambertian surfaces.** Transparent and refractive objects (glasses, bottles, lenses, bubbles, water surfaces) violate the fundamental photometric assumptions: they have view-dependent appearance that varies dramatically with viewing angle, refraction causes geometric distortion of the background, and standard depth estimation fails. Yet transparent dynamic surfaces are ubiquitous in real-world scenes (pouring water, rotating glass objects, inflating bubbles).

### Ideas

1. **Refraction-Aware 4D Gaussian Splatting:** Extend the 4DGS rendering to model refraction. Each Gaussian is augmented with a refractive index parameter. During rasterization, rays that hit transparent Gaussians are refracted (bent) using Snell's law before continuing to render the background. The deformation field models both the surface motion and the time-varying refraction effects. Surface extraction via the SDF is guided by the refracted ray consistency.

2. **Environment Matting + 4D Surface:** Use environment matting techniques to capture the transparent object's light transport function. Given multi-view captures with a known background pattern (checkerboard or coded patterns), solve for the transparent object's surface normals and depth via refraction inversion. Then track the surface over time using 4DGS with the recovered normals as supervision.

3. **Neural Transient 4D Surface:** Use a combination of polarimetric cues (which encode surface normals even for transparent objects) and multi-view stereo to reconstruct transparent dynamic surfaces. Polarization cameras naturally decompose the reflected and transmitted light components, providing surface orientation information that is independent of the object's transparency.

### Datasets

- **TransCG** (ICRA 2022) — transparent object grasping dataset (static, but useful for validation).
- **ClearGrasp** — transparent objects with depth GT.
- **Custom Synthetic Transparent Dynamics:** Render glass/fluid animations in Blender Cycles (which supports physically based refraction) with multi-view cameras.
- **KeyPose** — transparent object pose estimation dataset.

### Compute Required

- **GPUs:** 2–4× NVIDIA A100 (80GB)
- **Estimated GPU Hours:** ~1,500–2,500 hours

### Doability in 3 Months

**Medium.** The refraction-aware rendering (Idea 1) requires careful implementation of differentiable Snell's law within the GS rasterizer. The polarimetric approach (Idea 3) requires specialized hardware. Idea 2 (environment matting) is the most feasible but requires controlled capture setups. Synthetic data (Blender) is the most realistic path for ground-truth evaluation.

### Likelihood of Acceptance at CVPR 2027

**Medium (55–70%).** Transparent object reconstruction is a recognized challenge, and combining it with 4D dynamics is novel. However, the scope is somewhat niche. Risk: results on transparent objects are inherently harder to evaluate quantitatively (depth GT for transparent objects is scarce). Strong qualitative results and a well-designed synthetic benchmark are essential.

---

## PS 12: Self-Supervised 4D Surface from Unlabeled Web Videos

### Problem Statement

**All current 4D surface reconstruction methods require carefully calibrated multi-view camera setups or, at minimum, accurate camera intrinsics/extrinsics from SfM.** This restricts 4D surface reconstruction to controlled lab environments. Meanwhile, billions of single-view videos on the internet show dynamic scenes with rich surface information. Can we extract 4D surface priors from these unlabeled, uncalibrated, single-view web videos?

### Ideas

1. **Self-Supervised 4D Surface Pre-Training on Web Videos:** Train a foundation model that, given a single video frame, predicts (a) a canonical 3D surface (as an SDF or 2DGS), (b) per-frame deformation parameters, (c) camera parameters. Training signal: reconstruction loss on the same video (render the predicted 4D surface from the predicted cameras and compare to the input frames). Cycle consistency: deforming frame i's surface to frame j's time should match frame j's predicted surface. This is purely self-supervised — no GT depth, flow, or camera poses.

2. **Large-Scale 4D Surface Dataset via Automatic Annotation:** Use existing foundation models (Depth Anything V2, SAM2, RAFT, DINOv2) to automatically annotate a large corpus of web videos with pseudo-labels (depth maps, segmentation masks, optical flow, features). Train a 4D surface prediction model on this automatically annotated dataset. This is not fully self-supervised but eliminates manual annotation.

3. **Contrastive 4D Surface Learning:** Learn a 4D surface representation by contrasting: (a) different timesteps of the same object should have the same canonical surface but different deformations, (b) different objects should have different canonical surfaces. Train on web videos where object tracking (via SAM2) provides the correspondence. The learned representation can then be fine-tuned for specific 4D surface reconstruction tasks.

### Datasets

- **WebVid-10M** — large-scale web video dataset (for pre-training).
- **Ego4D** — egocentric video dataset.
- **Something-Something V2** — human-object interaction videos.
- **Kinetics-700** — human action videos.
- **Fine-tune/evaluate on:** D-FAUST, Hi4D, CMU Panoptic, iPhone datasets.

### Compute Required

- **GPUs:** 16–32× NVIDIA A100/H100 (80GB)
- **Estimated GPU Hours:** ~10,000–20,000 hours (dominated by large-scale pre-training on web videos)

### Doability in 3 Months

**Low.** Large-scale self-supervised pre-training on web videos requires massive compute and data infrastructure. Even with a smaller subset (e.g., 100K videos), the pipeline is complex. Idea 2 (pseudo-label annotation) is more feasible as it leverages existing models, but still requires significant engineering.

### Likelihood of Acceptance at CVPR 2027

**Very High (80–90%) if executed well.** Self-supervised learning from web data for 3D/4D is one of the most exciting frontiers. If the model shows strong zero-shot generalization to standard benchmarks, this would be a landmark paper. Risk: extremely compute-intensive and may require a large research team.

---

## PS 13: Multi-Entity Compositional 4D Surface Reconstruction

### Problem Statement

**Current 4D surface methods model the entire scene as a single, monolithic deformation field. They cannot separately identify, reconstruct, and track individual objects or entities within a dynamic scene.** DeSiRe-GS (CVPR 2025) separates static backgrounds from dynamic objects but treats all dynamic objects as one category and doesn't extract per-object surfaces. MAPo partitions by motion magnitude but not by object identity. For real-world applications (robotics manipulation, AR scene understanding, autonomous driving), per-object 4D surface reconstruction with instance-level tracking is essential.

### Ideas

1. **Instance-Aware 4DGS with Per-Object Canonical Spaces:** Extend DeSiRe-GS's decomposition to instance-level granularity. Use SAM2 or DINOv2 features to associate Gaussians with object instances. Each instance maintains its own canonical 2DGS representation and deformation field. Interactions between instances (contacts, collisions) are modeled via inter-object constraints. Surface extraction is per-instance, enabling independent manipulation.

2. **Object-Centric 4D Surface Slots:** Inspired by slot attention (Locatello et al.), learn a fixed number of "4D surface slots" that compete to explain the observed dynamics. Each slot owns a subset of Gaussians and a dedicated deformation field. Slots are trained to reconstruct the multi-view video, with a diversity loss ensuring different slots capture different objects. This is fully unsupervised (no SAM or YOLO needed).

3. **Scene Graph 4D Surface:** Represent the dynamic scene as a scene graph where nodes are object 4D surfaces and edges are spatial/temporal relationships (contact, occlusion, proximity). Jointly optimize the per-node surfaces and the edge relationships. The graph structure provides compositional generalization: new objects can be added or removed without re-optimizing the entire scene.

### Datasets

- **KITTI / Waymo** — driving scenes with instance-level annotations.
- **CMU Panoptic** — multi-person indoor scenes.
- **Hi4D** — two-person interaction with GT meshes.
- **BEHAVE** — human-object interaction.
- **HOI4D** — human-object interaction in diverse scenes.
- **ScanNet++** (rendered as video) — indoor scenes with instance segmentation.

### Compute Required

- **GPUs:** 4× NVIDIA A100 (80GB)
- **Estimated GPU Hours:** ~2,000–3,000 hours

### Doability in 3 Months

**High.** Idea 1 (instance-aware 4DGS) is the most straightforward — it builds directly on DeSiRe-GS + 4DSurf. SAM2 provides reliable instance masks. The per-object canonical space and deformation field are architecturally simple. Idea 2 (slot attention) is more novel but requires more research. Idea 3 (scene graph) is the most complex.

### Likelihood of Acceptance at CVPR 2027

**High (70–80%).** Compositional/object-centric 4D reconstruction is directly relevant to robotics and embodied AI — two of CVPR's fastest-growing areas. The paper would bridge the 4D reconstruction and object-centric learning communities. Risk: if each object's surface quality degrades compared to monolithic reconstruction, the contribution is weakened.

---

## PS 14: Neural Jacobian Fields for Simulation-Ready 4D Meshes

### Problem Statement

**Current 4D surface methods extract meshes as a byproduct of visualization (Marching Cubes on SDF, or TSDF fusion). These meshes are not "simulation-ready": they have inconsistent vertex counts across frames, no correspondences, poor triangle quality, and unknown material properties.** DySurface showed a cloth simulation experiment, but the mesh was manually post-processed. For the "digital twin" vision to work, reconstructed 4D meshes must be directly usable in physics engines (FEM, cloth simulation, robotics planning).

### Ideas

1. **Jacobian-Aligned 4D Surface Extraction:** Extend TextMesh4D's Jacobian Deformation Field to *reconstruction* (not generation). Given a 4DGS reconstruction, extract a canonical mesh and learn per-face Jacobians that deform the mesh to match each frame. Key insight: because the Poisson solver preserves vertex connectivity, the output mesh has **frame-consistent topology and vertex correspondence** by construction — exactly what simulators need. Add mesh quality losses: aspect ratio regularization, minimum angle constraints, and area preservation to ensure good triangle quality.

2. **Material Parameter Estimation from 4D Surfaces:** Given a reconstructed 4D surface sequence (with known deformations), solve an *inverse problem* to estimate the object's material parameters (Young's modulus, Poisson's ratio, density). Method: run a differentiable physics simulator (e.g., DiffTaichi, Warp) with guessed material parameters, simulate the deformation, and compare the simulated surface trajectory with the reconstructed one. Gradient descent on material parameters until the simulation matches the reconstruction. The resulting mesh + material parameters form a complete simulation-ready digital twin.

3. **Tetrahedral 4D Reconstruction:** Instead of surface-only reconstruction, jointly reconstruct the interior volumetric tetrahedral mesh (using differentiable tetrahedralization like TetGen + differentiable FEM). This provides a volumetric representation directly compatible with physics simulators. Optimize the tet-mesh deformation to match the observed 4DGS rendering.

### Datasets

- **D-NeRF** (synthetic, with known mesh GT).
- **DG-Mesh** dataset — mesh-level GT for dynamic scenes.
- **Hi4D** — human dynamics with GT meshes.
- **DeformingThings4D** — GT mesh sequences with known material categories.
- **Custom Synthetic FEM Sequences:** Simulate deformations with known materials in Blender/Houdini, capture multi-view renders, reconstruct and recover material parameters.

### Compute Required

- **GPUs:** 2–4× NVIDIA A100 (80GB)
- **Estimated GPU Hours:** ~1,500–2,500 hours (differentiable simulation adds cost per iteration)

### Doability in 3 Months

**Medium-High.** Idea 1 (Jacobian-aligned extraction) is very feasible — it's essentially applying TextMesh4D's Jacobian framework to reconstructed scenes rather than generated ones. Idea 2 (material estimation) requires integrating a differentiable simulator, which adds complexity but is well-supported by existing libraries (DiffTaichi, Warp). Idea 3 (tetrahedral) is the most ambitious.

### Likelihood of Acceptance at CVPR 2027

**High (70–80%).** "Simulation-ready" and "digital twin" are major narrative themes aligned with the robotics and embodied AI push at CVPR. Showing that reconstructed meshes can be directly used in physics simulations (and that material parameters can be recovered) would be a compelling demonstration of downstream utility. Risk: the paper must show tangible downstream benefits, not just "our meshes are simulator-compatible."

---

## PS 15: 4D Surface Gaussian Splatting with Adaptive Topology Remeshing

### Problem Statement

**Current 4D surface extraction methods use a two-stage approach: (1) optimize 4DGS, then (2) extract a mesh via Marching Cubes on an SDF or by fitting surfels. This decoupling means the mesh is never directly optimized, leading to suboptimal surface quality.** Furthermore, the mesh resolution is uniform (determined by the Marching Cubes grid resolution), wasting triangles in flat regions and under-sampling curved regions.

### Ideas

1. **Differentiable Mesh-Gaussian Co-Optimization:** Maintain *both* a Gaussian representation and an explicit mesh simultaneously during training. At each iteration: (a) render the scene using Gaussians for photometric loss, (b) render the mesh for geometric losses (silhouette, depth), (c) enforce consistency between the Gaussian positions and mesh vertices via a mutual snapping loss. Periodically remesh the explicit mesh using isotropic remeshing (long edges → split, short edges → collapse, non-Delaunay edges → flip) to maintain adaptive triangle quality.

2. **Gaussian-to-Mesh Distillation with Progressive Refinement:** After optimizing 4DGS, extract an initial coarse mesh. Then iteratively: (a) identify regions where the mesh poorly approximates the Gaussians (high chamfer distance), (b) locally subdivide the mesh in those regions, (c) optimize vertex positions using differentiable rendering with the original training views. Repeat until convergence. This produces an adaptively refined mesh concentrated in high-detail regions.

3. **Dynamic Gaussian Surfels with Mesh Connectivity:** Directly optimize 2DGS surfel disks with explicit mesh connectivity (Delaunay triangulation of surfel centers). The connectivity is updated dynamically during training: (a) when a surfel splits (densification), update the triangulation, (b) when surfels merge (pruning), collapse the edge. The deformation field operates on the mesh vertices (surfel centers) with ARAP regularization on the mesh edges, naturally preserving surface quality during dynamics.

### Datasets

- **D-NeRF**, **DG-Mesh** — synthetic with GT meshes for quantitative evaluation.
- **Hi4D**, **CMU Panoptic** — real-world multi-view.
- **Ub4D datasets** — monocular with GT mesh.

### Compute Required

- **GPUs:** 2–4× NVIDIA A100 (80GB)
- **Estimated GPU Hours:** ~1,000–2,000 hours

### Doability in 3 Months

**High.** Idea 2 (distillation with progressive refinement) is the simplest — it's a post-processing pipeline on existing 4DGS reconstructions. Idea 3 (surfels with connectivity) is the most elegant but requires modifying the core 3DGS training loop. Idea 1 (co-optimization) is feasible if using differentiable rendering libraries (Nvdiffrast, PyTorch3D).

### Likelihood of Acceptance at CVPR 2027

**Medium-High (65–75%).** Mesh quality is a recurring concern in the 4DGS literature, and an adaptive remeshing solution addresses a real need. However, if the improvement over simple Marching Cubes is only incremental, the paper may not feel impactful enough. Strong improvements in mesh quality metrics (e.g., Hausdorff distance, normal consistency) on challenging scenes with fine details are needed.

---

## Cross-Cutting Analysis: Prioritized Recommendations

Based on novelty, feasibility, and estimated acceptance likelihood, here are the top-5 ranked ideas:

| Rank | PS # | Title | Feasibility | Impact | Acceptance Likelihood |
|:--|:--|:--|:--|:--|:--|
| 🥇 1 | **PS 3** | Foundation-Model-Driven 4D Surface Prior | Low-Medium | Very High | 80–90% |
| 🥈 2 | **PS 1** | Topology-Changing 4D Surface Reconstruction | Medium-High | Very High | 75–85% |
| 🥉 3 | **PS 4** | Monocular 4D Surface without Templates | High | High | 75–85% |
| 4 | **PS 6** | Unified Static-Dynamic 4D Surface SLAM | Medium-High | High | 75–85% |
| 5 | **PS 13** | Multi-Entity Compositional 4D Surface | High | High | 70–80% |

### Sweet-Spot Recommendations (High Feasibility + High Impact):

- **PS 4 (Monocular 4D Surface)** and **PS 9 (Articulated 4D Surface)** are the most feasible within 3 months while maintaining high acceptance likelihood.
- **PS 1 (Topology-Changing)** is the highest-impact gap across the entire literature — solving it, even partially, would be a major contribution.
- **PS 14 (Simulation-Ready Meshes)** has a strong narrative for the growing robotics/embodied AI community at CVPR.

### High-Risk / High-Reward:

- **PS 3 (Foundation Model)** and **PS 12 (Web Videos)** are potentially transformative but require significant compute and team resources.

---

*Generated from analysis of: DySurface (arXiv 2026), 4C4D (CVPR 2026), 4DSurf (CVPR 2026), ReconDrive (arXiv 2026), FRoG (TVCG 2026), Sparse4DGS (AAAI 2026), TextMesh4D (ICML 2026), MAPo (CVPR 2026), SpeeDe3DGS (CVPR 2026), 4DGS-SLAM (ICCV 2025), DeSiRe-GS (CVPR 2025), DynaSurfGS (arXiv 2024), H3D-DGS (NeurIPS 2025), Motion2VecSets (CVPR 2024), 4D-GS (CVPR 2024), Unbiased4D (CVPR 2023).*
