window.INTEREST_GRAPH = {
    "fluid_aerodynamics": {
        related: ["propulsion_energy_thermal", "flight_control_autonomy", "scientific_ai_computational_digital"],
        weight: 1.0,
        label: { en: "Fluid Mechanics & Aerodynamics", tr: "Akışkanlar Mekaniği ve Aerodinamik" }
    },
    "flight_control_autonomy": {
        related: ["fluid_aerodynamics", "avionics_software_digital", "systems_design_optimization"],
        weight: 1.0,
        label: { en: "Flight Mechanics, Control & Autonomy", tr: "Uçuş Mekaniği, Kontrol ve Otonomi" }
    },
    "space_systems_astronautics": {
        related: ["flight_control_autonomy", "systems_design_optimization", "propulsion_energy_thermal"],
        weight: 1.0,
        label: { en: "Space Systems & Astronautics", tr: "Uzay Sistemleri ve Astronotik" }
    },
    "propulsion_energy_thermal": {
        related: ["fluid_aerodynamics", "space_systems_astronautics", "structures_materials_design"],
        weight: 1.0,
        label: { en: "Propulsion, Energy & Thermal Systems", tr: "İtki, Enerji ve Termal Sistemler" }
    },
    "structures_materials_design": {
        related: ["manufacturing_testing_industry", "systems_design_optimization", "propulsion_energy_thermal"],
        weight: 1.0,
        label: { en: "Structures, Materials & Mechanical Design", tr: "Yapılar, Malzemeler ve Mekanik Tasarım" }
    },
    "systems_design_optimization": {
        related: ["space_systems_astronautics", "structures_materials_design", "flight_control_autonomy"],
        weight: 1.0,
        label: { en: "Systems Engineering, Design & Optimization", tr: "Sistem Mühendisliği, Tasarım ve Optimizasyon" }
    },
    "avionics_software_digital": {
        related: ["flight_control_autonomy", "scientific_ai_computational_digital"],
        weight: 1.0,
        label: { en: "Avionics, Software & Digital Technologies", tr: "Aviyonik, Yazılım ve Sayısal Teknolojiler" }
    },
    "manufacturing_testing_industry": {
        related: ["structures_materials_design", "systems_design_optimization"],
        weight: 1.0,
        label: { en: "Manufacturing, Testing & Industrial Applications", tr: "Üretim, Test ve Endüstriyel Uygulamalar" }
    },
    "scientific_ai_computational_digital": {
        related: ["avionics_software_digital", "fluid_aerodynamics"],
        weight: 1.0,
        label: { en: "Scientific AI, Computational Science & Digital Engineering", tr: "Bilimsel Yapay Zekâ, Hesaplamalı Bilim ve Dijital Mühendislik" }
    }
};

window.getRelatedInterests = function(coreInterest) {
    if (!coreInterest || !window.INTEREST_GRAPH[coreInterest]) return [];
    return window.INTEREST_GRAPH[coreInterest].related;
};
