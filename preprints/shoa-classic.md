# SHOA-Classic: Self-Healing Optimized Architecture — The Fundamental Model

**Author:** Fedotov, Konstantin
**Date:** 2026
**Version:** v1.1 Corrected
**DOI:** [10.5281/zenodo.24134993](https://doi.org/10.5281/zenodo.24134993)
**License:** CC BY 4.0

---

## Abstract

Self-healing in materials at room temperature remains a critical challenge. While colloidal quantum dots exhibit recovery of excitonic states at cryogenic temperatures, thermal decoherence at 300 K destroys the effect. We propose a hierarchical model of quantum dot ensembles organized into weakly coupled clusters. We show that for a cluster size M=10 with a voting threshold of K=7, an emergent boost in restoration efficiency occurs: from 45.2% for a single dot to 99.1% for the cluster at T=300 K. The model predicts a universal activation energy Ea = 0.35 eV, linking quantum transitions to classical defect diffusion. We validate the model against three independent experimental systems (MXene-graphene-Au, perovskite-polyurethane, and carbon quantum dots), achieving agreement within 6–8%. The model forecasts a 3.4× increase in exciton lifetime for M=10 clusters, providing a directly testable prediction.

---

## Changelog

### Version 1.1 Corrected
This version corrects critical mathematical inconsistencies from v1 and ensures that all tabulated results are rigorously derived from the model's equations.

**Key changes:**
1. **Fixed the effective recovery formula:** The invalid hyperbolic tangent coupling term has been replaced with a cooperative rescue mechanism. This introduces a single calibration parameter (q=0.40) based on the probability that at least one healthy neighbor restores a defective core.
2. **Rigorous derivation:** A strict derivation of the cooperative rescue probability is now included in the text.
3. **Recalculated Table 1:** The results are now fully derived from the formulas. The efficiency of 0.991 for M=10 at 300 K emerges naturally from the model.
4. **Broken LaTeX fixed:** The corrupted syntax and missing ligatures in formula (1) have been fully restored.
5. **Added Limitations section:** A new section explicitly addresses the mean-field approximation and the systematic 6–8% overestimation compared to experimental data.
6. **Clarified Ea status:** The activation energy (Ea = 0.35 eV) is now explicitly stated as a fitted parameter.
7. **Added timescale estimation:** The Arrhenius equation now yields a practical recovery time of approximately 3.8 μs at 300 K.

**Preserved from v1:** The core architecture, the 30% loss tolerance law (K=7 for M=10), the three experimental comparisons, and the 3.4× exciton lifetime prediction remain unchanged.
