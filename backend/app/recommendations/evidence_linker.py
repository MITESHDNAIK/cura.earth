"""Small curated evidence catalogue used by the deterministic recommendation layer.

The recommendation engine never invents quantitative site-specific outcomes. Evidence
summaries are intentionally directional unless a source provides a transferable estimate.
"""
from typing import Dict, List
from app.core.schema import ScientificEvidence

EVIDENCE_CATALOG: Dict[str, List[ScientificEvidence]] = {
    "agroforestry": [
        ScientificEvidence(title="Climate Change and Land", source_organization="IPCC", year=2019, url_or_doi="https://www.ipcc.ch/srccl/", finding_summary="The IPCC discusses agroforestry and diversified land management as options that can support soil carbon, reduce degradation and provide biodiversity and ecosystem-service benefits; outcomes vary by system and climate."),
        ScientificEvidence(title="Recarbonizing Global Soils", source_organization="FAO", year=2022, url_or_doi="https://www.fao.org/3/cb6386en/cb6386en.pdf", finding_summary="FAO describes agroforestry, cover, residue and diversified management practices as pathways for rebuilding soil organic matter and improving soil functions."),
    ],
    "legume_intercropping": [
        ScientificEvidence(title="Climate Change and Land", source_organization="IPCC", year=2019, url_or_doi="https://www.ipcc.ch/srccl/", finding_summary="The IPCC describes diversification and agroecological practices as options that can improve resilience and provide multiple ecosystem services; effects depend on local management and climate."),
        ScientificEvidence(title="Recarbonizing Global Soils", source_organization="FAO", year=2022, url_or_doi="https://www.fao.org/3/cb6386en/cb6386en.pdf", finding_summary="FAO identifies legume integration, cover crops and diversified rotations among practices that can contribute organic inputs and improve soil management."),
    ],
    "cover_cropping": [
        ScientificEvidence(title="Recarbonizing Global Soils", source_organization="FAO", year=2022, url_or_doi="https://www.fao.org/3/cb6386en/cb6386en.pdf", finding_summary="FAO describes cover crops, residue retention and reduced disturbance as practices that protect soil, add organic inputs and support soil-water functions."),
        ScientificEvidence(title="Climate Change and Land", source_organization="IPCC", year=2019, url_or_doi="https://www.ipcc.ch/srccl/", finding_summary="The IPCC identifies cover crops and maintenance of ground cover as sustainable land-management options that can reduce erosion and nutrient loss and contribute to soil carbon."),
    ],
    "native_hedgerows": [
        ScientificEvidence(title="The assessment report on pollinators, pollination and food production", source_organization="IPBES", year=2016, url_or_doi="https://doi.org/10.5281/zenodo.3402856", finding_summary="IPBES identifies habitat quality, diversity and connectivity as important components of landscapes supporting pollinators and pollination."),
        ScientificEvidence(title="Climate Change and Land", source_organization="IPCC", year=2019, url_or_doi="https://www.ipcc.ch/srccl/", finding_summary="The IPCC discusses habitat restoration, landscape diversity and connectivity as components of sustainable land management and biodiversity conservation."),
    ],
    "water_retention_management": [
        ScientificEvidence(title="Recarbonizing Global Soils", source_organization="FAO", year=2022, url_or_doi="https://www.fao.org/3/cb6386en/cb6386en.pdf", finding_summary="FAO describes ground cover, residue retention and reduced disturbance as practices that protect soil structure and support water-related soil functions."),
    ],
    "soil_ph_management": [
        ScientificEvidence(title="Soil organic carbon and sustainable soil management resources", source_organization="FAO", year=2022, url_or_doi="https://www.fao.org/soils-portal/soil-management/soil-organic-carbon/en/", finding_summary="FAO emphasizes soil testing and site-appropriate soil management; pH management should be matched to crop and soil conditions rather than treated as a universal intervention."),
    ],
}


class EvidenceLinker:
    @staticmethod
    def get_evidence_for_intervention(intervention_key: str, query: str | None = None) -> List[ScientificEvidence]:
        return EVIDENCE_CATALOG.get(intervention_key, [])


evidence_linker = EvidenceLinker()
