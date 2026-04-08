from __future__ import annotations

from dataclasses import asdict, dataclass
from math import exp, log10, sqrt
from typing import Optional
import argparse
import json

# Default fuel factors
FUEL_GB = {
    "LNG": 0.14,
    "LH2": 0.12,
    "Methanol": 0.05,
    "NH3": 0.035,
    "Diesel": 0.055,
}

# Table 2 curve-fit parameters for vertical receiving surface view factor Fv
# S/D : (y_inf, b, c)
FV_PARAMS = [
    (1.1, 0.4533, 10.6775, 0.9134),
    (1.2, 0.4149, 6.9809, 1.0322),
    (1.5, 0.3317, 2.9996, 1.0865),
    (2.0, 0.2482, 1.5043, 1.0931),
    (4.0, 0.1234, 0.4803, 1.0956),
    (10.0, 0.0484, 0.1377, 1.1721),
    (20.0, 0.0218, 0.0492, 1.3150),
]

@dataclass(frozen=True)
class PoolFireInputs:
    # Step 1
    D: float = 30.0
    U: float = 5.0
    Gb: float = 0.14
    rho: float = 1.205
    g: float = 9.81
    A: float = 55.0
    p: float = 0.6666667
    q: float = -0.21

    # Step 3
    r: float = 17.17
    beta: float = 0.06
    dHc: float = 50000.0
    Ca: float = 1.0
    Ta: float = 293.15

    # Step 5
    Emax: float = 325.0
    Dopt: float = 13.8
    k_m: float = 130.0
    Lb_factor: float = 0.6

    # Step 6
    S: float = 10.0
    H_override: Optional[float] = None

@dataclass(frozen=True)
class Step1Result:
    F: float
    U_star: float
    LF_over_D: float
    LF: float

@dataclass(frozen=True)
class Step2Result:
    log10D: float
    Y: float

@dataclass(frozen=True)
class Step3Result:
    denominator: float
    Cs: float


@dataclass(frozen=True)
class Step4Result:
    log10F: float
    psi: float
    Lc: float


@dataclass(frozen=True)
class Step5Result:
    Eb: float
    Lb: float
    BL: float
    w: float
    E_bar: float


@dataclass(frozen=True)
class InterpolatedFvParams:
    sd_used: float
    y_inf: float
    b: float
    c: float
    note: str


@dataclass(frozen=True)
class Step6Result:
    sd_ratio: float
    fv_params: InterpolatedFvParams
    H_used: float
    H_over_D: float
    Fv: float
    Pwsat: float
    tau_atm: float
    Qrad: float


@dataclass(frozen=True)
class PoolFireResult:
    inputs: PoolFireInputs
    step1: Step1Result
    step2: Step2Result
    step3: Step3Result
    step4: Step4Result
    step5: Step5Result
    step6: Step6Result

    def to_dict(self) -> dict:
        return asdict(self)


def inputs_for_fuel(fuel: str, **overrides) -> PoolFireInputs:
    if fuel not in FUEL_GB:
        raise ValueError(f"Unsupported fuel '{fuel}'. Choose from: {', '.join(FUEL_GB)}")
    return PoolFireInputs(Gb=FUEL_GB[fuel], **overrides)


def interpolate_fv_params(sd: float) -> InterpolatedFvParams:
    """Interpolate view-factor parameters by S/D ratio."""
    if sd <= 0:
        raise ValueError("S/D must be > 0.")

    if sd <= FV_PARAMS[0][0]:
        s0, y0, b0, c0 = FV_PARAMS[0]
        return InterpolatedFvParams(s0, y0, b0, c0, "S/D below range -> clamped to 1.1")

    if sd >= FV_PARAMS[-1][0]:
        s1, y1, b1, c1 = FV_PARAMS[-1]
        return InterpolatedFvParams(s1, y1, b1, c1, "S/D above range -> clamped to 20")

    for i in range(len(FV_PARAMS) - 1):
        s1, y1, b1, c1 = FV_PARAMS[i]
        s2, y2, b2, c2 = FV_PARAMS[i + 1]
        if s1 <= sd <= s2:
            if abs(sd - s1) < 1e-12:
                return InterpolatedFvParams(s1, y1, b1, c1, "Exact match")
            if abs(sd - s2) < 1e-12:
                return InterpolatedFvParams(s2, y2, b2, c2, "Exact match")

            t = (sd - s1) / (s2 - s1)
            y = y1 + t * (y2 - y1)
            b = b1 + t * (b2 - b1)
            c = c1 + t * (c2 - c1)
            return InterpolatedFvParams(
                sd,
                y,
                b,
                c,
                f"Interpolated between {s1} and {s2} (t={t:.3f})",
            )

    s0, y0, b0, c0 = FV_PARAMS[0]
    return InterpolatedFvParams(s0, y0, b0, c0, "Fallback clamp")

'''Calculation Steps
'''
def calculate_step1(
    *,
    D: float,
    U: float,
    Gb: float,
    rho: float,
    g: float,
    A: float,
    p: float,
    q: float,
) -> Step1Result:
    if D <= 0:
        raise ValueError("No D less than 0 senior")
    if Gb <= 0:
        raise ValueError("No Gb less than 0 sire")
    if rho <= 0:
        raise ValueError("No rho less than 0 mista")
    if g <= 0:
        raise ValueError("No g less than 0 senior pasta")
    if U < 0:
        raise ValueError("No U less than 0 sensei")

    F = Gb / (rho * sqrt(g * D))
    if F <= 0:
        raise ValueError("Computed F must be > 0.")

    U_star = U / (((Gb / rho) * g * D) ** (1.0 / 3.0))
    LF_over_D = A * (F**p) * (U_star**q)
    LF = LF_over_D * D
    return Step1Result(F=F, U_star=U_star, LF_over_D=LF_over_D, LF=LF)


def calculate_step2(*, D: float) -> Step2Result:
    if D <= 0:
        raise ValueError("D must be > 0. How u gon have a <=0 diameter bruh")

    log_d = log10(D)
    y = (9.412 + 2.758 * log_d) / 100.0
    return Step2Result(log10D=log_d, Y=y)


def calculate_step3(
    *,
    Y: float,
    rho: float,
    r: float,
    beta: float,
    dHc: float,
    Ca: float,
    Ta: float,
) -> Step3Result:
    if rho <= 0:
        raise ValueError("rho must be > 0.")
    if beta <= 0:
        raise ValueError("beta must be > 0.")
    if Ca <= 0:
        raise ValueError("Ca must be > 0.")
    if Ta <= 0:
        raise ValueError("Ta must be > 0.")

    denominator = 1.0 + (r / beta) + (dHc / (Ca * Ta))
    cs = rho * Y * (1.0 / denominator)
    return Step3Result(denominator=denominator, Cs=cs)


def calculate_step4(*, F: float, LF: float) -> Step4Result:
    if F <= 0:
        raise ValueError("F must be > 0.")
    if LF <= 0:
        raise ValueError("LF must be > 0.")

    log_f = log10(F)
    psi = 0.7 + 0.25 * log_f
    lc = psi * LF
    return Step4Result(log10F=log_f, psi=psi, Lc=lc)


def calculate_step5(
    *,
    D: float,
    Cs: float,
    psi: float,
    Emax: float,
    Dopt: float,
    k_m: float,
    Lb_factor: float,
) -> Step5Result:
    if D <= 0:
        raise ValueError("D must be > 0.")
    if Emax <= 0:
        raise ValueError("Emax must be > 0.")
    if Dopt <= 0:
        raise ValueError("Dopt must be > 0.")
    if k_m <= 0:
        raise ValueError("k_m must be > 0.")
    if Lb_factor <= 0:
        raise ValueError("Lb_factor must be > 0.")

    eb = Emax * (1.0 - exp(-D / Dopt))
    lb = Lb_factor * D
    bl = exp(-k_m * Cs * lb)
    w = (1.0 + 3.0 * bl) / 4.0
    e_bar = eb * (psi + w * (1.0 - psi))
    return Step5Result(Eb=eb, Lb=lb, BL=bl, w=w, E_bar=e_bar)


def calculate_step6(
    *,
    D: float,
    S: float,
    Ta: float,
    E_bar: float,
    LF: float,
    H_override: Optional[float] = None,
) -> Step6Result:
    if D <= 0:
        raise ValueError("D must be > 0.")
    if S <= 0:
        raise ValueError("S must be > 0.")
    if Ta <= 0:
        raise ValueError("Ta must be > 0.")
    if E_bar <= 0:
        raise ValueError("E_bar must be > 0.")
    if LF <= 0:
        raise ValueError("LF must be > 0.")

    d_radius = D / 2.0
    if d_radius <= 0:
        raise ValueError("Derived radius must be > 0.")

    sd_ratio = S / d_radius
    fv_params = interpolate_fv_params(sd_ratio)

    h_used = LF if H_override is None else H_override
    if h_used <= 0:
        raise ValueError("H must be > 0.")

    h_over_d = h_used / d_radius
    fv = fv_params.y_inf * (1.0 - exp(-fv_params.b * (h_over_d**fv_params.c)))
    pwsat = exp(25.897 - 5319.4 / Ta)
    tau_atm = 2.02 * ((pwsat * S) ** (-0.09))
    qrad = E_bar * fv * tau_atm

    return Step6Result(
        sd_ratio=sd_ratio,
        fv_params=fv_params,
        H_used=h_used,
        H_over_D=h_over_d,
        Fv=fv,
        Pwsat=pwsat,
        tau_atm=tau_atm,
        Qrad=qrad,
    )


def calculate_pool_fire(inputs: PoolFireInputs) -> PoolFireResult:
    step1 = calculate_step1(
        D=inputs.D,
        U=inputs.U,
        Gb=inputs.Gb,
        rho=inputs.rho,
        g=inputs.g,
        A=inputs.A,
        p=inputs.p,
        q=inputs.q,
    )
    step2 = calculate_step2(D=inputs.D)
    step3 = calculate_step3(
        Y=step2.Y,
        rho=inputs.rho,
        r=inputs.r,
        beta=inputs.beta,
        dHc=inputs.dHc,
        Ca=inputs.Ca,
        Ta=inputs.Ta,
    )
    step4 = calculate_step4(F=step1.F, LF=step1.LF)
    step5 = calculate_step5(
        D=inputs.D,
        Cs=step3.Cs,
        psi=step4.psi,
        Emax=inputs.Emax,
        Dopt=inputs.Dopt,
        k_m=inputs.k_m,
        Lb_factor=inputs.Lb_factor,
    )
    step6 = calculate_step6(
        D=inputs.D,
        S=inputs.S,
        Ta=inputs.Ta,
        E_bar=step5.E_bar,
        LF=step1.LF,
        H_override=inputs.H_override,
    )
    return PoolFireResult(
        inputs=inputs,
        step1=step1,
        step2=step2,
        step3=step3,
        step4=step4,
        step5=step5,
        step6=step6,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the modular pool fire model.")
    parser.add_argument("--fuel", choices=sorted(FUEL_GB), default="LNG")
    parser.add_argument("--diameter", type=float, default=30.0)
    parser.add_argument("--wind-speed", type=float, default=5.0)
    parser.add_argument("--separation", type=float, default=10.0)
    parser.add_argument("--height-override", type=float, default=None)
    return parser


def main() -> None:
    args = _build_parser().parse_args()
    inputs = inputs_for_fuel(
        args.fuel,
        D=args.diameter,
        U=args.wind_speed,
        S=args.separation,
        H_override=args.height_override,
    )
    result = calculate_pool_fire(inputs)
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()