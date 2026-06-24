const INTEREST_GRAPH = {
  orbital_mechanics: {
    label: { en: "Orbital Mechanics", tr: "Yörünge Mekaniği" },
    neighbors: {
      astrodynamics: 0.95,
      mission_analysis: 0.85,
      orbit_determination: 0.85,
      spacecraft_gnc: 0.70,
      satellite_systems: 0.65,
      monte_carlo_simulation: 0.45,
      surrogate_modeling: 0.35,
      trajectory_optimization: 0.75
    }
  },
  astrodynamics: {
    label: { en: "Astrodynamics", tr: "Astrodinamik" },
    neighbors: {
      orbital_mechanics: 0.95,
      trajectory_optimization: 0.75
    }
  },
  mission_analysis: {
    label: { en: "Mission Analysis", tr: "Görev Analizi" },
    neighbors: {
      orbital_mechanics: 0.85,
      systems_engineering: 0.60,
      optimization: 0.65,
      monte_carlo_simulation: 0.50
    }
  },
  orbit_determination: {
    label: { en: "Orbit Determination", tr: "Yörünge Belirleme" },
    neighbors: {
      orbital_mechanics: 0.85,
      navigation: 0.65
    }
  },
  cfd: {
    label: { en: "CFD", tr: "CFD" },
    neighbors: {
      aerodynamics: 0.90,
      fluid_mechanics: 0.90,
      turbulence: 0.80,
      hypersonics: 0.65,
      aeroacoustics: 0.45,
      heat_transfer: 0.55,
      hpc: 0.55,
      surrogate_modeling: 0.45,
      scientific_ai: 0.40
    }
  },
  fluid_mechanics: {
    label: { en: "Fluid Mechanics", tr: "Akışkanlar Mekaniği" },
    neighbors: { cfd: 0.90 }
  },
  aerodynamics: {
    label: { en: "Aerodynamics", tr: "Aerodinamik" },
    neighbors: { cfd: 0.90 }
  },
  turbulence: {
    label: { en: "Turbulence", tr: "Türbülans" },
    neighbors: { cfd: 0.80 }
  },
  hypersonics: {
    label: { en: "Hypersonics", tr: "Hipersonik" },
    neighbors: { cfd: 0.65 }
  },
  gnc: {
    label: { en: "GNC", tr: "GNC" },
    neighbors: {
      guidance: 0.90,
      navigation: 0.90,
      control_systems: 0.95,
      spacecraft_gnc: 0.85,
      flight_dynamics: 0.75,
      autonomy: 0.60,
      optimization: 0.50
    }
  },
  guidance: {
    label: { en: "Guidance", tr: "Güdüm" },
    neighbors: { gnc: 0.90 }
  },
  navigation: {
    label: { en: "Navigation", tr: "Navigasyon" },
    neighbors: { gnc: 0.90, orbit_determination: 0.65 }
  },
  control_systems: {
    label: { en: "Control Systems", tr: "Kontrol Sistemleri" },
    neighbors: { gnc: 0.95, robotics: 0.45 }
  },
  scientific_ai: {
    label: { en: "Scientific AI", tr: "Bilimsel Yapay Zekâ" },
    neighbors: {
      machine_learning: 0.90,
      physics_informed_ml: 0.90,
      surrogate_modeling: 0.85,
      data_driven_modeling: 0.85,
      digital_twin: 0.65,
      uncertainty_quantification: 0.60,
      optimization: 0.60,
      hpc: 0.55,
      cfd: 0.40,
      orbital_mechanics: 0.35,
      structures: 0.30
    }
  },
  machine_learning: {
    label: { en: "Machine Learning", tr: "Makine Öğrenmesi" },
    neighbors: { scientific_ai: 0.90 }
  },
  physics_informed_ml: {
    label: { en: "Physics-Informed ML", tr: "Fizik Bilgili Makine Öğrenmesi" },
    neighbors: { scientific_ai: 0.90 }
  },
  surrogate_modeling: {
    label: { en: "Surrogate Modeling", tr: "Vekil Modelleme" },
    neighbors: {
      scientific_ai: 0.85,
      cfd: 0.45,
      orbital_mechanics: 0.35,
      trajectory_optimization: 0.55
    }
  },
  digital_twin: {
    label: { en: "Digital Twin", tr: "Dijital İkiz" },
    neighbors: { scientific_ai: 0.65, systems_engineering: 0.60 }
  },
  uncertainty_quantification: {
    label: { en: "Uncertainty Quantification", tr: "Belirsizlik Nicelendirme" },
    neighbors: { scientific_ai: 0.60, monte_carlo_simulation: 0.80 }
  },
  propulsion: {
    label: { en: "Propulsion", tr: "İtki" },
    neighbors: {
      rocket_propulsion: 0.85,
      jet_propulsion: 0.85,
      combustion: 0.75,
      turbomachinery: 0.70,
      thermal_systems: 0.55
    }
  },
  rocket_propulsion: {
    label: { en: "Rocket Propulsion", tr: "Roket İtkisi" },
    neighbors: { propulsion: 0.85, space_systems: 0.55 }
  },
  electric_propulsion: {
    label: { en: "Electric Propulsion", tr: "Elektrikli İtki" },
    neighbors: { spacecraft_systems: 0.65 }
  },
  structures: {
    label: { en: "Structures", tr: "Yapılar" },
    neighbors: {
      aerospace_structures: 0.90,
      fem: 0.80,
      composites: 0.75,
      fatigue_damage: 0.65,
      aeroelasticity: 0.65
    }
  },
  aerospace_structures: {
    label: { en: "Aerospace Structures", tr: "Havacılık Yapıları" },
    neighbors: { structures: 0.90 }
  },
  composites: {
    label: { en: "Composites", tr: "Kompozitler" },
    neighbors: { structures: 0.75, lightweight_design: 0.65 }
  },
  fem: {
    label: { en: "FEM", tr: "Sonlu Elemanlar Yöntemi" },
    neighbors: { structures: 0.80, simulation_modeling: 0.60 }
  }
};

function buildExpandedInterestProfile(userInterests, graph, options = {}) {
  const decay = options.decay ?? 0.75;
  const maxDepth = options.maxDepth ?? 2;
  const minWeight = options.minWeight ?? 0.15;

  const expanded = new Map();

  function propagate(key, weight, currentDepth, visited) {
    if (currentDepth > maxDepth || weight < minWeight) return;

    const existingWeight = expanded.get(key) || 0;
    if (weight > existingWeight) {
      expanded.set(key, weight);
    }

    if (currentDepth < maxDepth) {
      const node = graph[key];
      if (node && node.neighbors) {
        for (const [neighborKey, edgeWeight] of Object.entries(node.neighbors)) {
          if (!visited.has(neighborKey)) {
            const nextVisited = new Set(visited);
            nextVisited.add(key);
            propagate(neighborKey, weight * edgeWeight * decay, currentDepth + 1, nextVisited);
          }
        }
      }
      
      for (const [otherKey, otherNode] of Object.entries(graph)) {
        if (otherNode.neighbors && otherNode.neighbors[key] !== undefined) {
          if (!visited.has(otherKey)) {
            const nextVisited = new Set(visited);
            nextVisited.add(key);
            propagate(otherKey, weight * otherNode.neighbors[key] * decay, currentDepth + 1, nextVisited);
          }
        }
      }
    }
  }

  for (const interest of userInterests) {
    propagate(interest.key, interest.weight, 0, new Set());
  }

  for (const [k, v] of expanded.entries()) {
    expanded.set(k, Math.min(1.0, Math.max(0, v)));
  }

  return expanded;
}

if (typeof window !== 'undefined') {
  window.INTEREST_GRAPH = INTEREST_GRAPH;
  window.buildExpandedInterestProfile = buildExpandedInterestProfile;
}
