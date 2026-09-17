"""
Cura.Earth What-If Ecology Simulator.

The simulator creates comparative, directional ecological projections
from predefined benchmark scenarios and intervention coefficients.

These outputs are modelled scenarios, not guaranteed real-world
predictions.
"""

from typing import Dict, Any, List, Optional

from .scenarios import BENCHMARK_SCENARIOS
from .intervention_mapper import (
    get_intervention_effects,
    get_intervention_name,
)


class EcologySimulator:

    def __init__(self):
        self.scenarios = BENCHMARK_SCENARIOS

    def _clamp(
        self,
        value: float,
        minimum: float,
        maximum: float
    ) -> float:

        return max(minimum, min(maximum, value))

    def _derive_water_availability(
        self,
        state: Dict[str, float]
    ) -> float:

        retention = state.get(
            "water_retention_capacity",
            0.0
        )

        base = state.get(
            "water_availability",
            0.0
        )

        # Retention is converted into a normalized contribution.
        retention_signal = self._clamp(
            retention / 150.0,
            0.0,
            1.0
        )

        value = (
            0.55 * base +
            0.45 * retention_signal
        )

        return self._clamp(value, 0.0, 1.0)

    def _derive_biodiversity(
        self,
        state: Dict[str, float]
    ) -> float:

        microbial = self._clamp(
            state.get(
                "microbial_diversity_index",
                0.0
            ) / 4.0,
            0.0,
            1.0
        )

        pollinators = self._clamp(
            state.get(
                "pollinator_richness",
                0.0
            ) / 20.0,
            0.0,
            1.0
        )

        fragmentation = self._clamp(
            state.get(
                "habitat_fragmentation_index",
                1.0
            ),
            0.0,
            1.0
        )

        crop_diversity = self._clamp(
            state.get(
                "crop_diversity",
                0.0
            ),
            0.0,
            1.0
        )

        biodiversity = (
            0.30 * microbial +
            0.30 * pollinators +
            0.20 * (1.0 - fragmentation) +
            0.20 * crop_diversity
        )

        return self._clamp(
            biodiversity,
            0.0,
            1.0
        )

    def _apply_cascade(
        self,
        state: Dict[str, float],
        intervention_effects: Dict[str, float]
    ) -> Dict[str, float]:

        # ---------------------------------------------------------
        # 1. Direct intervention effects
        # ---------------------------------------------------------

        for metric, effect in intervention_effects.items():

            if metric not in state:
                state[metric] = 0.0

            state[metric] += effect

        # ---------------------------------------------------------
        # 2. Soil → Water cascade
        # ---------------------------------------------------------

        soc = state.get(
            "soil_organic_carbon",
            0.0
        )

        retention = state.get(
            "water_retention_capacity",
            0.0
        )

        # Higher SOC improves the modelled water-retention pathway.
        soc_water_effect = max(
            0.0,
            soc - 0.35
        ) * 8.0

        state["water_retention_capacity"] += (
            soc_water_effect
        )

        # ---------------------------------------------------------
        # 3. Water retention → Water availability
        # ---------------------------------------------------------

        state["water_availability"] = (
            self._derive_water_availability(state)
        )

        # ---------------------------------------------------------
        # 4. Soil → Microbial cascade
        # ---------------------------------------------------------

        state["microbial_diversity_index"] += (
            max(0.0, soc - 0.35) * 0.10
        )

        # ---------------------------------------------------------
        # 5. Habitat → Pollinator cascade
        # ---------------------------------------------------------

        fragmentation = state.get(
            "habitat_fragmentation_index",
            1.0
        )

        habitat_recovery = max(
            0.0,
            0.85 - fragmentation
        )

        state["pollinator_richness"] += (
            habitat_recovery * 1.5
        )

        # ---------------------------------------------------------
        # 6. Crop diversity → Biodiversity
        # ---------------------------------------------------------

        state["crop_diversity"] = self._clamp(
            state.get(
                "crop_diversity",
                0.0
            ),
            0.0,
            1.0
        )

        state["biodiversity"] = (
            self._derive_biodiversity(state)
        )

        # ---------------------------------------------------------
        # 7. Keep physical bounds sensible
        # ---------------------------------------------------------

        state["soil_organic_carbon"] = max(
            0.0,
            state["soil_organic_carbon"]
        )

        state["water_retention_capacity"] = max(
            0.0,
            state["water_retention_capacity"]
        )

        state["microbial_diversity_index"] = max(
            0.0,
            state["microbial_diversity_index"]
        )

        state["pollinator_richness"] = max(
            0.0,
            state["pollinator_richness"]
        )

        state["habitat_fragmentation_index"] = (
            self._clamp(
                state["habitat_fragmentation_index"],
                0.0,
                1.0
            )
        )

        return state

    def simulate(
        self,
        scenario_key: str,
        timeframe_years: int = 5,
        custom_baseline: Optional[
            Dict[str, float]
        ] = None,
        perturbations: Optional[
            List[Dict[str, Any]]
        ] = None,
        intervention: Optional[str] = None,
    ) -> Dict[str, Any]:

        if scenario_key not in self.scenarios:

            scenario_key = (
                "semi_arid_monoculture_agroforestry"
            )

        scenario = self.scenarios[scenario_key]

        baseline = dict(
            scenario["baseline"]
        )

        if custom_baseline:
            baseline.update(
                custom_baseline
            )

        timeframe_years = max(
            1,
            min(timeframe_years, 30)
        )

        perturbations = perturbations or []

        intervention_effects = (
            get_intervention_effects(
                intervention
            )
        )

        intervention_name = (
            get_intervention_name(
                intervention
            )
        )

        rates = dict(
            scenario[
                "annual_rate_multipliers"
            ]
        )

        # ---------------------------------------------------------
        # Projection
        # ---------------------------------------------------------

        trajectory = []

        state = dict(baseline)

        for year in range(
            0,
            timeframe_years + 1
        ):

            # Save current ecological state.
            trajectory.append(
                {
                    "year": year,
                    "metrics": {
                        key: round(
                            value,
                            4
                        )
                        for key, value in state.items()
                    },
                }
            )

            if year == timeframe_years:
                break

            next_state = dict(state)

            # -----------------------------------------------------
            # Baseline ecological progression
            # -----------------------------------------------------

            for metric, rate in rates.items():

                if metric not in next_state:
                    continue

                # Derived metrics are handled by the cascade,
                # rather than by independent compounding.
                if metric in {
                    "water_availability",
                    "biodiversity",
                    "crop_diversity",
                }:
                    continue

                next_state[metric] *= (
                    1.0 + rate
                )

            # -----------------------------------------------------
            # Intervention-specific direct effects
            # -----------------------------------------------------

            next_state = self._apply_cascade(
                next_state,
                intervention_effects
            )

            # -----------------------------------------------------
            # External perturbations
            # -----------------------------------------------------

            for perturbation in perturbations:

                p_year = perturbation.get(
                    "year"
                )

                if p_year != year + 1:
                    continue

                metric = perturbation.get(
                    "metric"
                )

                delta = perturbation.get(
                    "delta",
                    0.0
                )

                if metric in next_state:
                    next_state[metric] += delta

            state = next_state

        initial = trajectory[0]["metrics"]
        final = trajectory[-1]["metrics"]

        # ---------------------------------------------------------
        # Change summary
        # ---------------------------------------------------------

        change_summary = {}

        for metric in final:

            start_value = initial.get(
                metric,
                0.0
            )

            final_value = final[metric]

            absolute_change = (
                final_value - start_value
            )

            if abs(start_value) > 1e-9:

                percent_change = (
                    absolute_change /
                    abs(start_value)
                ) * 100.0

            else:
                percent_change = 0.0

            change_summary[metric] = {
                "initial": round(
                    start_value,
                    4
                ),
                "final": round(
                    final_value,
                    4
                ),
                "absolute_change": round(
                    absolute_change,
                    4
                ),
                "percent_change": round(
                    percent_change,
                    2
                ),
            }

        # ---------------------------------------------------------
        # Cascade explanation
        # ---------------------------------------------------------

        cascade_summary = []

        if intervention:

            cascade_summary.append(
                f"{intervention_name} applies "
                "intervention-specific effects."
            )

        cascade_summary.extend(
            [
                "Soil organic carbon influences "
                "water-retention dynamics.",

                "Water retention contributes to "
                "modelled water availability.",

                "Soil conditions influence "
                "microbial diversity.",

                "Habitat fragmentation influences "
                "pollinator recovery.",

                "Microbial diversity, pollinators, "
                "habitat connectivity and crop diversity "
                "contribute to the biodiversity index.",
            ]
        )

        return {
            "scenario_key": scenario_key,

            "scenario_name": (
                scenario["title"]
                + (
                    f" + {intervention_name}"
                    if intervention
                    else ""
                )
            ),

            "description": scenario[
                "description"
            ],

            "intervention": intervention,

            "intervention_name": (
                intervention_name
                if intervention
                else None
            ),

            "timeframe_years": timeframe_years,

            "baseline": {
                key: round(
                    value,
                    4
                )
                for key, value in baseline.items()
            },

            "trajectory": trajectory,

            "final_state": final,

            "change_summary": change_summary,

            "cascade_summary": cascade_summary,

            "confidence_level": (
                "Modelled scenario projection. "
                "Directional effects are intended for "
                "comparative What-If analysis and require "
                "site-specific validation before real-world use."
            ),
        }


ecology_simulator = EcologySimulator()