# S55 preregistration (written before any S55 numeric code exists)
All code new (s55_*.py), no import of s50–s54 modules. M2(ψ) = −log2(Σ_P ⟨P⟩⁴ / 2^N) over 4^N unsigned Pauli strings.

N1 (D6 radial coefficient). Random stabilizer states φ: |0..0⟩ then random Clifford circuit (≥ 20·N gates from {H,S,CNOT} on random qubits),
N = 2,3,4,5; 6 states per N; per state 8 random tangent directions w (complex Gaussian, projected ⊥ φ, normalized); geodesic χ(t) = cos t φ + sin t w.
Estimate a = lim M2(χ(t))/t² by symmetric second difference + Richardson (h = 2e-3, 1e-3).
PASS if max over all (state,direction) of |a − 4/ln2|/(4/ln2) < 1e-4. Also report it with h=1e-2 unextrapolated (expect O(h²) drift only).
N2 (D6 isotropy / full Hessian). N = 2,3 (2 states each): full real Hessian of f(v) = M2(normalize(φ + Σ v_k e_k)) over a real orthonormal basis
of the horizontal tangent space (dim 2(2^N−1)), central differences h=1e-3. PASS if all eigenvalues within 1e-3 relative of 8/ln2
(Hessian-matrix convention f ≈ ½vᵀHv; equivalently quadratic-form coefficient 4/ln2) and off-diagonal max < 1e-3·(8/ln2).
N3 (D7 global lower-bound shape, N=2 and N=3, all stabilizer states enumerated: expect 60 and 1080 rays).
Sample 20000 states: half Haar, half near random stabilizer rays at FS distance ~ U(0,0.5). d = FS distance to nearest stabilizer ray.
PASS if (a) ratio M2/((4/ln2) d²) → 1 as d→0 (bin d<0.02: mean within 2e-2 of 1), (b) min over all samples of M2/d² > 0 (report value: the global c),
(c) no sample has M2 < 1e-6 with d > 0.05.
N4 (D7 end-to-end, independent tiny instance). N=3, R,A,B single qubits, ψ0 = GHZ and ψ0 = |0⟩|Φ+⟩ (R=0, A,B=1,2), and N=4 R={0},A={1,2},B={3}
with ψ0 a random stabilizer state (2 instances). G = random Hermitian on (A-qubit, B-qubit). D² = min over local Hermitian h of
‖(1−Π0)(G+h)ψ0‖² computed by my own real least squares; coef = 4D²/ln2. LU-min via scipy L-BFGS over local unitaries exp(iΣ params·basis)
(10 restarts: 1 at identity, 9 random Haar starts). θ ∈ {0.08,0.04,0.02}. PASS if r = LUmin/(coef θ²) satisfies |r−1| ≤ 0.1 at θ=0.08
and |r−1| decreases monotonically with |r−1|(0.02) ≤ 0.5·|r−1|(0.08); and global ≥ identity-start − 1e-9·θ² … i.e. no restart beats D² coefficient
by more than O(θ³) (best/ident ≥ 1 − 5θ). Cases with D² < 1e-6 reported separately (then expect LU-min = O(θ³) or smaller).
Discrepancy in any PASS criterion → item verdict DISCREPANCY (or INCONCLUSIVE if numerically ill-conditioned, with stated reason).
2026-10-02T01:54:01Z
