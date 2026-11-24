# Independent Citation Audit

**Verdict: WARN (`metadata_drift`) — not PASS**

- Date: 2026-11-18 (Asia/Shanghai); review completed 2026-11-17 UTC.
- Scope: all 41 bibliography entries and all 44 citation occurrences.
- Bibliography: `references.bib`.
- Context source: `writing/p12/paper-with-verified-references.md`.
- Result: **28 KEEP, 13 FIX, 0 REPLACE, 0 REMOVE**.
- Existence: 41/41 verified against arXiv, official proceedings/publisher records, Crossref, and/or OpenAlex.
- Context: all 44 occurrences support the cited topic; no citation needs replacement or removal.
- Duplicates: no duplicate DOI, arXiv identifier, normalized title, or preprint/published pair occurs within the 41-entry bibliography.
- Pass gate: fails because 13 entries have author, title, venue, year, or publication-version errors. This audit did not modify the bibliography or manuscript.

## Evidence Protocol

The four supplied probe files were used as evidence, not treated as verdicts. Exact-title matches, DOI/arXiv identifiers, author lists, dates, venues, and available abstracts were checked. Additional public checks used official CVF, AAAI, IJCAI, PMLR, NeurIPS, ICLR/DBLP, IEEE/Crossref, Elsevier, OpenAlex, arXiv, and DBLP records. A failed supplied probe was not interpreted as nonexistence when a canonical record was available.

Context lines below refer to `writing/p12/paper-with-verified-references.md`; `references.bib:L...` identifies the entry start. Each occurrence was assessed against the paper's actual abstract/contribution rather than title similarity alone. "All occurrences SUPPORTS" means the grouped citation supports the specific topic named by the manuscript, not that any cited work establishes this manuscript's new method or results.

## Required Fixes

### 1. `li2019deepgcn` — FIX (`references.bib:L37`)
- **Existence / context:** verified; line 17 occurrence SUPPORTS deep GCNs. [CVF](https://openaccess.thecvf.com/content_ICCV_2019/html/Li_DeepGCNs_Can_GCNs_Go_As_Deep_As_CNNs_ICCV_2019_paper.html); [DOI](https://doi.org/10.1109/ICCV.2019.00936).
- **Action:** correct `Muller, Matthias` to the published `Müller, Matthias` (BibTeX: `M{\"u}ller, Matthias`) and `Thabet, Ali` to `Thabet, Ali Kassem` (also indexed as Ali K. Thabet).

### 2. `zhu2023a2q` — FIX (`references.bib:L112`)
- **Existence / context:** verified; lines 19 and 87 SUPPORTS aggregation-aware mixed-precision/node-budget quantization. [ICLR/DBLP](https://dblp.org/rec/conf/iclr/ZhuLMH0LL023.html); [arXiv](https://arxiv.org/abs/2302.00193).
- **Action:** change `@article` / `journal={arXiv preprint}` to `@inproceedings` with `booktitle={International Conference on Learning Representations}`, `year={2023}`. The arXiv identifier may remain as a secondary identifier.

### 3. `hu2023fast` — FIX (`references.bib:L129`)
- **Existence / context:** verified; line 19 SUPPORTS quantized-ANN-to-SNN conversion. [DOI/OpenAlex](https://doi.org/10.1109/TPAMI.2023.3275769); [arXiv](https://arxiv.org/abs/2305.19868).
- **Action:** replace the arXiv-only venue with `journal={IEEE Transactions on Pattern Analysis and Machine Intelligence}`, `volume={45}`, `number={12}`, `pages={14546--14562}`, `year={2023}`, `doi={10.1109/TPAMI.2023.3275769}`.

### 4. `cherukuri2025lowrank` — FIX (`references.bib:L146`)
- **Existence / context:** verified; line 19 SUPPORTS low-rank neural-network compression. [DOI/OpenAlex](https://doi.org/10.1109/ICMLT65785.2025.11193154).
- **Action:** correct the venue from `International Conference on Machine Learning and Computing` to `International Conference on Machine Learning Technologies (ICMLT)`; add verified `pages={166--170}`. Do not confuse ICMLT with ICML.

### 5. `hao2023offset` — FIX (`references.bib:L165`)
- **Existence / context:** verified; line 21 SUPPORTS offset-spike calibration. [ICLR/DBLP](https://dblp.org/rec/conf/iclr/HaoDB0Y23.html); [arXiv](https://arxiv.org/abs/2302.10685).
- **Action:** change to `@inproceedings`, `booktitle={International Conference on Learning Representations}`, `year={2023}`; retain arXiv:2302.10685 only as a secondary identifier.

### 6. `lv2024group` — FIX (`references.bib:L174`)
- **Existence / context:** verified; line 21 SUPPORTS group-neuron conversion. [DOI/OpenAlex](https://doi.org/10.1109/ICASSP48485.2024.10448202).
- **Action:** change to `@inproceedings`, `booktitle={ICASSP 2024 - 2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)}`, `pages={6475--6479}`, `year={2024}`, `doi={10.1109/ICASSP48485.2024.10448202}`.

### 7. `bu2023optimal` — FIX (`references.bib:L183`)
- **Existence / context:** verified; line 21 SUPPORTS high-accuracy, low-latency conversion. [Published ICLR 2022 PDF](https://yuzhaofei.github.io/papers/22-ICLR-Optimal%20ANN-SNN%20Conversion%20for%20High-accuracy%20and%20Ultra-low-latency%20Spiking%20Neural%20Networks.pdf); [arXiv](https://arxiv.org/abs/2303.04347).
- **Action:** use the published version: `@inproceedings`, `booktitle={International Conference on Learning Representations}`, **`year={2022}`**. The 2023 arXiv posting is not the conference year.

### 8. `huang2025ecmt` — FIX (`references.bib:L213`)
- **Existence / context:** verified; line 21 SUPPORTS Transformer ANN-to-SNN conversion. [DOI/OpenAlex](https://doi.org/10.1145/3664647.3680620); [arXiv](https://arxiv.org/abs/2502.21193).
- **Action:** replace the 2025 arXiv-only record with the 2024 publication: `@inproceedings`, `booktitle={Proceedings of the 32nd ACM International Conference on Multimedia}`, `pages={10688--10697}`, `year={2024}`, `doi={10.1145/3664647.3680620}`.

### 9. `delay-dsgn` — FIX (`references.bib:L262`)
- **Existence / context:** verified; line 23 SUPPORTS delayed dynamic-graph evolution. [Official PMLR](https://proceedings.mlr.press/v267/wang25dm.html).
- **Action:** title ends in singular `Evolving Graph`, not `Evolving Graphs`; author is `Liang, Jianqing`, not `Jianqin`. Use the PMLR record: PMLR volume 267, pages 64880--64894, ICML 2025.

### 10. `sun2024spikegraphormer` — FIX (`references.bib:L293`)
- **Existence / context:** verified; line 23 SUPPORTS spiking graph attention. [Publisher](https://www.sciencedirect.com/science/article/pii/S0020025526007590); [DOI/OpenAlex](https://doi.org/10.1016/j.ins.2026.123828); [arXiv](https://arxiv.org/abs/2403.15480).
- **Action:** update to `journal={Information Sciences}`, `volume={755}`, `pages={123828}`, `year={2026}`, `doi={10.1016/j.ins.2026.123828}`; correct `O'Hared, Gregory` to the canonical `O'Hare, Gregory M. P.` The arXiv record retains the older spelling/year and should not override the publication.

### 11. `zhang2025sgnnbench` — FIX (`references.bib:L302`)
- **Existence / context:** verified; line 23 SUPPORTS large-scale SGNN evaluation. [Official NeurIPS 2026 listing](https://neurips.cc/virtual/2026/poster/139238); [arXiv](https://arxiv.org/abs/2509.21342); [author publication listing](https://chenliang.tech/publications).
- **Action:** replace the preprint with the accepted NeurIPS 2026 version, `SGNNBench: A Holistic Evaluation of Spiking Graph Neural Networks on Large-scale Graphs`. The accepted author list is Huizhe Zhang, Jintang Li, Yuchang Zhu, Huazhen Zhong, and Liang Chen: add `Zhong, Huazhen` and remove the preprint-only `Kuang, Li`. Do not merely change the year while retaining the v1 title/authors.

### 12. `nunes2022snnsurvey` — FIX (`references.bib:L349`)
- **Existence / context:** verified; line 21 SUPPORTS a broad SNN survey. [DOI](https://doi.org/10.1109/ACCESS.2022.3179968); [institutional metadata](https://sigarra.up.pt/ffup/en/pub_geral.pub_view?pi_pub_base_id=578876).
- **Action:** correct pages from `60764--60783` to **`60738--60764`**.

### 13. `dampfhoffer2023snnlearning` — FIX (`references.bib:L341`)
- **Existence / context:** verified; line 21 SUPPORTS conversion/direct-training distinctions. [IEEE](https://ieeexplore.ieee.org/document/10097504/); [DOI/OpenAlex](https://doi.org/10.1109/TNNLS.2023.3263008).
- **Action:** the DOI's online-first year 2023 is consistent, but the record is bibliographically incomplete. Add final publication metadata `volume={35}`, `number={9}`, `pages={11906--11921}`, `year={2024}` (or explicitly label an online-first 2023 citation without the 2024 volume fields). Do not combine year 2023 with the 2024 issue as though both were the same publication event.

## Verified Entries — All Occurrences SUPPORTS

The following 28 entries are KEEP. Their supplied title, author, year, venue/type, and identifiers are sufficiently accurate for the present citation; no action is required.

| Key | Bib | Context | Verification and context basis |
|---|---:|---:|---|
| `kipf2017gcn` | L1 | 17 | [arXiv:1609.02907](https://arxiv.org/abs/1609.02907): GCN graph convolution. |
| `hamilton2018graphsage` | L10 | 17 | [arXiv:1706.02216](https://arxiv.org/abs/1706.02216): neighborhood sampling/GraphSAGE; 2017 NeurIPS venue is correct. |
| `velickovic2018gat` | L19 | 17 | [arXiv:1710.10903](https://arxiv.org/abs/1710.10903): graph attention. |
| `xu2019gin` | L28 | 17 | [arXiv:1810.00826](https://arxiv.org/abs/1810.00826): expressive graph networks. |
| `abu2019mixhop` | L46 | 17 | [arXiv:1905.00067](https://arxiv.org/abs/1905.00067): higher-order neighborhood mixing. |
| `chen2020gcnii` | L55 | 17 | [arXiv:2007.02133](https://arxiv.org/abs/2007.02133): simple/deep GCNs. |
| `li2018deeper` | L64 | 17 | [AAAI DOI](https://doi.org/10.1609/aaai.v32i1.11604): GCN depth/over-smoothing analysis. |
| `wu2021gnnsurvey` | L74 | 17 | [DOI](https://doi.org/10.1109/TNNLS.2020.2978386): broad GNN survey. |
| `tailor2021degreequant` | L85 | 19 | [arXiv:2008.05000](https://arxiv.org/abs/2008.05000): GNN quantization-aware training. |
| `ding2021vqgnn` | L94 | 19 | [arXiv:2110.14363](https://arxiv.org/abs/2110.14363): vector-quantized GNN representations. |
| `wang2022qgtc` | L103 | 19 | [PPoPP](https://ppopp22.sigplan.org/details/PPoPP-2022-main-conference/10/QGTC-Accelerating-Quantized-Graph-Neural-Networks-via-GPU-Tensor-Core): quantized GNN execution on tensor cores. |
| `wan2023adaqp` | L121 | 19 | [Official MLSys abstract](https://proceedings.mlsys.org/paper_files/paper/2023/hash/420bcf98bb3615a21468f1efb426e96d-Abstract-mlsys2023.html): distributed message quantization. |
| `gholami2022quantization` | L138 | 19 | [DOI/OpenAlex](https://doi.org/10.1201/9781003162810-13): general quantization survey/chapter. |
| `one-spike` | L154 | 21, 21, 88 | [DOI](https://doi.org/10.1109/TETC.2024.3386893): single-spike phase/output coding; does not validate the manuscript's local adaptation. |
| `li2023seenn` | L192 | 21 | [Official NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2023/hash/c801e68207da477bbc44182b9fac1129-Abstract-Conference.html): temporal spiking early exit. |
| `you2024spikezip` | L199 | 21 | [Official PMLR](https://proceedings.mlr.press/v235/you24b.html): Transformer SNN conversion. |
| `zhao2025ttfs` | L206 | 21 | [Official PMLR](https://proceedings.mlr.press/v267/zhao25n.html): TTFS Transformer conversion. |
| `li2024erroraware` | L222 | 21 | [DOI](https://doi.org/10.1007/s11263-024-02046-2): post-training parameter calibration. |
| `spikinggcn` | L233 | 23 | [Official IJCAI](https://ijcai.org/proceedings/2022/338): spiking graph convolution. |
| `spikenet` | L242 | 23 | [Official AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/26034): dynamic graph representation via SNNs. |
| `dy-sign` | L251 | 23 | [Official AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/29587): dynamic spiking GNNs. |
| `signnn` | L269 | 23 | [Publisher](https://www.sciencedirect.com/science/article/pii/S0031320324007775): dynamic graph representation with SiGNN. |
| `msg` | L279 | 23 | [Official NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2024/hash/3ba7560b4c3e66d760fbdd472cf4a5a9-Abstract-Conference.html): Riemannian-manifold SGNN. |
| `negative-spike` | L286 | 23 | [Official IJCAI](https://ijcai.org/proceedings/2025/719): signed/negative-spike conversion. |
| `li2023graph1bit` | L311 | 23 | [Official ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/abb4847bbd60f38b1b7649d26c7a0067-Abstract-Conference.html): graph contrastive learning and 1-bit spikes. The entry is a valid 2023 arXiv citation, not a duplicate/version conflict. |
| `chaurasia2026sgspose` | L320 | 23 | [DOI](https://doi.org/10.1109/ACCESS.2026.3651795): spiking-graph geometric 6D pose application. |
| `asgcn` | L330 | 23 | [Official AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/32154): asynchronous event-based visual processing. |
| `wang2022taxonomicsnn` | L359 | 21 | [DOI/OpenAlex](https://doi.org/10.1007/s12293-022-00373-w): SNN taxonomy, training, and hardware survey. |

## Duplicate and Version Check

- Exact normalized DOI duplicates: **0**.
- Exact arXiv identifier duplicates: **0**.
- Exact normalized title duplicates: **0**.
- Same-work preprint/published duplicate pairs: **0**.
- Repeated key `one-spike` at manuscript lines 21 (twice) and 88 is intentional reuse, not a duplicate bibliography entry.
- Version corrections listed above concern inaccurate or outdated individual records; none requires deleting a second in-bib version.

## Limitations and Bottom Line

Some publisher landing pages in the supplied official-page probe returned empty metadata or bot checks. Those cases were resolved using the supplied Crossref/OpenAlex payloads plus independent official/DBLP searches; no entry is marked nonexistent merely because a landing-page scrape failed. The probe file also contains unrelated/legacy queries and a false arXiv result (`1904.01332`, an algebra paper) that does not correspond to any audited entry and was excluded.

**Bottom line:** all 41 cited works exist and every use is context-appropriate, with no duplicate versions in the bibliography. Nevertheless, the requested PASS condition is not met until the 13 FIX items are corrected and the corrected bibliography is rechecked.
