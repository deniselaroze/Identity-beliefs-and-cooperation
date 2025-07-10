# Generate example participant sets to test all group types


macro_faculties <- define_macro_faculties()
all_degree_pairs <- create_proximity_df(macro_faculties)
all_degrees <- unlist(macro_faculties)


make_participants <- function(degree, count) {
  paste0(degree, ".", seq_len(count))
}

generate_flexible_participant_set <- function(degrees, total_n = sample(c(15, 18), 1), min_per_degree = 3) {
  repeat {
    num_degrees <- sample(2:4, 1)
    chosen_degrees <- sample(degrees, num_degrees)
    
    # Start with minimum 3 for the primary degree
    counts <- rep(min_per_degree, num_degrees)
    remainder <- total_n - sum(counts)
    
    # Randomly allocate the remainder while keeping total fixed
    if (remainder >= 0) {
      extra <- sample(0:remainder, num_degrees, replace = TRUE)
      while (sum(extra) != remainder) {
        extra <- sample(0:remainder, num_degrees, replace = TRUE)
      }
      final_counts <- counts + extra
      
      # Return the participant vector
      participants <- unlist(mapply(make_participants, chosen_degrees, final_counts, SIMPLIFY = FALSE))
      return(participants)
    }
  }
}

set.seed(42)
example_participant_sets <- replicate(
  8,
  generate_flexible_participant_set(all_degrees),
  simplify = FALSE
)

summarise_group <- function(result, case_id) {
  do.call(rbind, lapply(seq_along(result), function(i) {
    group <- result[[i]]
    data.frame(
      test_case = case_id,
      group_number = i,
      member = group$members,
      identity = group$identities,
      group_type = group$group_type,
      individual_experience = unname(group$individual_experience),
      stringsAsFactors = FALSE
    )
  }))
}

# Combine all test case summaries into one big table

all_tests_table <- do.call(rbind, lapply(seq_along(example_participant_sets), function(i) {
  set.seed(100 + i)
  result <- generate_groups_with_individuals(example_participant_sets[[i]], all_degree_pairs)
  summarise_group(result, i)
}))

# Show full table

#print(all_tests_table)



# Frequency table of individual_experience from all_tests_table

total_participants <- nrow(all_tests_table)
experience_counts <- as.data.frame(table(all_tests_table$individual_experience))
colnames(experience_counts) <- c("individual_experience", "count")

experience_counts$percentage <- round(100 * experience_counts$count / total_participants, 1)

print(experience_counts)


