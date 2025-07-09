###########################################
### Denise Laroze
### started July 2025
###########################################



############################################
#### Group composition function
############################################

# Identity mapping
identity_map <- function(id) {
  if (grepl("^econ", id)) return("econ")
  if (grepl("^psc", id)) return("psc")  
  if (grepl("^psy", id)) return("psy")
  if (grepl("^nut", id)) return("nut")
  return(NA)
}

# Block mapping
which_block <- function(identity) {
  if (identity %in% c("econ", "psc")) return("close")
  if (identity %in% c("psy", "nut")) return("far")
  return(NA)
}

# Individual experience type
individual_experience <- function(self, group) {
  identities <- sapply(group, identity_map)
  self_identity <- identity_map(self)
  others <- setdiff(group, self)
  other_identities <- sapply(others, identity_map)
  
  if (all(other_identities == self_identity)) {
    return("homogeneous")
  }
  
  self_block <- which_block(self_identity)
  others_blocks <- sapply(others, function(x) which_block(identity_map(x)))
  unique_blocks <- unique(others_blocks)
  
  if (length(unique_blocks) == 1) {
    if (unique_blocks == self_block) return("close_mix")
    else return("far_mix")
  } else {
    return("hetero_mix")
  }
}

# Proximity score function
proximity_score <- function(group) {
  identities <- sapply(group, identity_map)
  unique_ids <- unique(identities)
  
  if (length(unique_ids) == 1) {
    return("homogeneous")
  }
  
  close_block <- c("econ", "psc")
  far_block <- c("psy", "nut")
  
  if (all(unique_ids %in% close_block) || all(unique_ids %in% far_block)) {
    return("close_mix")
  } else {
    return("hetero_mix")
  }
}

# Group generator with at least one homogeneous group
generate_groups_with_individuals <- function(participants) {
  repeat {
    shuffled <- sample(participants)
    n <- length(shuffled)
    group_count <- floor(n / 3)
    groups <- split(shuffled[1:(group_count * 3)], rep(1:group_count, each=3))
    
    results <- list()
    has_homogeneous <- FALSE
    
    for (i in seq_along(groups)) {
      g <- groups[[i]]
      ids <- sapply(g, identity_map)
      group_type <- proximity_score(g)
      
      if (group_type == "homogeneous") {
        has_homogeneous <- TRUE
      }
      
      group_result <- list(
        members = g,
        identities = ids,
        group_type = group_type,
        individual_experience = setNames(
          sapply(g, function(self) individual_experience(self, g)),
          g
        )
      )
      
      results[[i]] <- group_result
    }
    
    if (has_homogeneous) return(results)
  }
}


###################################################################
# Flexible balanced sampling helper (allowing groups to be absent)
###################################################################

sample_balanced_session <- function(n_total = 15) {
  identities <- c("econ", "psc", "psy", "nut")
  selected <- sample(identities, sample(2:4, 1))  # random 2 to 4 identities
  dominant <- sample(selected, 1)
  
  identity_pool <- paste0(dominant, ".", 1:9)
  max_n <- length(identity_pool)
  dominant_n <- sample(3:min(6, max_n), 1)
  remaining_n <- n_total - dominant_n
  
  rest_identities <- setdiff(selected, dominant)
  rest_probs <- rep(1, length(rest_identities))
  rest_alloc <- if (length(rest_identities) > 0) rmultinom(1, remaining_n, rest_probs) else NULL
  
  counts <- setNames(c(dominant_n, as.vector(rest_alloc)), c(dominant, rest_identities))
  
  all_samples <- unlist(mapply(function(id, n) {
    identity_pool <- paste0(id, ".", 1:9)
    sample(identity_pool, min(n, length(identity_pool)))
  }, names(counts), counts))
  
  return(all_samples)
}

# Run 12 sessions with flexible sampling
set.seed(1)
total_experiences <- c()
session_compositions <- list()

for (i in 1:12) {
  p1 <- sample_balanced_session(n_total = 15)
  session_compositions[[paste0("Session_", i)]] <- table(sapply(p1, identity_map))
  groups <- generate_groups_with_individuals(p1)
  
  for (group in groups) {
    total_experiences <- c(total_experiences, group$individual_experience)
  }
}

cat("\nTotal summary of individual experience types across 12 sessions:\n")
print(table(total_experiences))

cat("\nComposition of each session (identity counts):\n")
print(session_compositions)