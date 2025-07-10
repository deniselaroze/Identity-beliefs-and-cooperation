# Define macro faculties

define_macro_faculties <- function() {
  list(
    "Ciencias de la Salud y Medicina" = c("Medicina", "Enfermería", "Kinesiología", "Tecnología Médica", "Nutrición y Dietética", "Odontología", "Obstetricia", "Terapia Ocupacional", "Química y Farmacia", "Fonoaudiología"),
    "Ingeniería y Ciencias Aplicadas" = c("Ingeniería Civil Plan Común", "Ingeniería Civil Industrial", "Ingeniería Civil en Informática e Innovación Tecnológica", "Ingeniería Civil en Informática e Inteligencia Artificial", "Ingeniería Civil en Minería", "Ingeniería Civil en Obras Civiles", "Ingeniería Civil en BioMedicina", "Geología", "Data Business Intelligence"),
    "Artes, Diseño y Comunicación" = c("Arquitectura", "Diseño", "Cine", "Publicidad", "Periodismo y Comunicación", "Bachillerato en Diseño"),
    "Ciencias Sociales, Derecho, Negocios y Educación" = c("Derecho", "Ingeniería Comercial", "Global Business Administration", "Bachillerato en Ingeniería Comercial", "Ciencia Política y Políticas Públicas", "Pedagogía en Educación Básica", "Pedagogía en Educación de Párvulos", "Programa de Formación Pedagógica", "Psicología", "Bachillerato en Psicología")
  )
}

# Create proximity data frame

create_proximity_df <- function(macro_faculties) {
  degree_list <- unlist(macro_faculties)
  names(degree_list) <- NULL
  
  all_pairs <- expand.grid(from = degree_list, to = degree_list, stringsAsFactors = FALSE)
  
  all_pairs$proximity <- apply(all_pairs, 1, function(row) {
    if (row["from"] == row["to"]) {
      return("self")
    }
    
    same_macro <- any(sapply(macro_faculties, function(degs) {
      row["from"] %in% degs && row["to"] %in% degs
    }))
    
    if (same_macro) {
      return("near")
    } else {
      return("far")
    }
  })
  
  # Enforce symmetry (both (A,B) and (B,A))
  reversed <- all_pairs
  names(reversed) <- c("to", "from", "proximity")
  reversed <- reversed[, c("from", "to", "proximity")]
  
  symmetric_df <- unique(rbind(all_pairs, reversed))
  return(symmetric_df)
}

# Identity mapping

identity_map <- function(id) {
  degree <- sub("\\.\\d+$", "", id)
  return(degree)
}

# Proximity score function

proximity_score_df <- function(group, all_degree_pairs) {
  identities <- sapply(group, identity_map)
  unique_ids <- unique(identities)
  
  if (length(unique_ids) == 1) {
    return("homogeneous")
  }
  
  pairs <- expand.grid(from = unique_ids, to = unique_ids, stringsAsFactors = FALSE)
  df <- merge(pairs, all_degree_pairs, by = c("from", "to"), all.x = TRUE)
  proximities <- unique(df$proximity)
  
  if (setequal(proximities, c("self", "near"))) {
    return("near_mix")
  } else if (setequal(proximities, c("self", "far"))) {
    return("hetero.far")
  } else if (setequal(proximities, c("near", "far"))) {
    return("hetero.mixed")
  } else if (identical(proximities, "near")) {
    return("near")
  } else if (identical(proximities, "far")) {
    return("far")
  } else {
    return("error2")
  }
}

# Individual experience type


individual_experience_df <- function(self, group, all_degree_pairs) {
  self_identity <- identity_map(self)
  others <- setdiff(group, self)
  other_identities <- sapply(others, identity_map)
  
  # Search for all relevant (from, to) or (to, from) proximity rows
  df <- subset(all_degree_pairs, 
               (from == self_identity & to %in% other_identities) |
                 (to == self_identity & from %in% other_identities))
  
  proximities <- unique(df$proximity)
  
  if (length(proximities) == 0) {
    return("Error")
  }
  
  # Convert to sorted character vector for matching
  prox_sorted <- sort(proximities)
  
  if (all(prox_sorted == "self")) {
    return("homogeneous")
  } else if (all(prox_sorted == "near")) {
    return("near")
  } else if (all(prox_sorted == "far")) {
    return("far")
  } else if (setequal(prox_sorted, c("near", "self"))) {
    return("hetero.near")
  } else if (setequal(prox_sorted, c("far", "self"))) {
    return("hetero.far")
  } else if (setequal(prox_sorted, c("far", "near"))) {
    return("hetero.mixed")
  } else {
    return("Error2")
  }
}


# Group generator with at least one homogeneous group

# Group generator with retry limit to prevent infinite loop
generate_groups_with_individuals <- function(participants, all_degree_pairs, max_attempts = 1000) {
  for (attempt in 1:max_attempts) {
    shuffled <- sample(participants)
    n <- length(shuffled)
    group_count <- floor(n / 3)
    
    if (group_count == 0) break  # Not enough participants to form even one group
    
    group_indices <- rep(1:group_count, each = 3)
    groups <- split(shuffled[1:(group_count * 3)], group_indices)
    
    results <- vector("list", length(groups))
    has_homogeneous <- FALSE
    
    # Step 1 & 2: Calculate proximity and individual experience
    for (i in seq_along(groups)) {
      group <- groups[[i]]
      identities <- sapply(group, identity_map)
      group_type <- proximity_score_df(group, all_degree_pairs)
      if (group_type == "homogeneous") has_homogeneous <- TRUE
      
      individual_experience <- sapply(group, function(self) {
        individual_experience_df(self, group, all_degree_pairs)
      })
      
      results[[i]] <- list(
        members = group,
        identities = identities,
        group_type = group_type,
        individual_experience = setNames(individual_experience, group)
      )
    }
    
    # Step 3: Randomly assign one group to Baseline
    baseline_group_index <- sample(seq_along(results), 1)
    results[[baseline_group_index]]$group_type <- "Baseline"
    results[[baseline_group_index]]$individual_experience <- 
      setNames(rep("Baseline", 3), results[[baseline_group_index]]$members)
    
    if (has_homogeneous) {
      return(results)
    }
  }
  
  stop("No homogeneous group found after ", max_attempts, " attempts.")
}

