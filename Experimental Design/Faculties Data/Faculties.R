### Faculties and Undergraduate Degrees at San Carlos de Apoquindo – RESB Campus (UDD)
# 
# #### Faculty of Architecture and Design
# - Arquitectura
# - Diseño
# - Cine
# - Publicidad *(Doble Titulación)*
#   - Bachillerato en Diseño
# 
# #### Faculty of Law and Social Sciences
# - Derecho
# - Periodismo y Comunicación *(Doble Titulación)*
#   - Bachillerato en Derecho, Ciencias Sociales y Humanidades
# 
# #### Faculty of Government
# - Ciencia Política y Políticas Públicas
# 
# #### Faculty of Business and Economics
# - Ingeniería Comercial
# - Global Business Administration
# - Bachillerato en Ingeniería Comercial
# 
# #### Faculty of Medicine / Health Sciences
# - Medicina
# - Enfermería
# - Kinesiología
# - Tecnología Médica
# - Nutrición y Dietética
# - Odontología
# - Obstetricia
# - Terapia Ocupacional
# - Química y Farmacia *(Nueva 2025)*
#   - Fonoaudiología
# 
# #### Faculty of Psychology
# - Psicología
# - Bachillerato en Psicología
# 
# #### Faculty of Education
# - Pedagogía en Educación Básica con Menciones: Inglés y Educación Especial e Inclusión
# - Pedagogía en Educación de Párvulos con Menciones: Inglés y Aprendizaje al Aire Libre
# - Programa de Formación Pedagógica para Licenciados y Profesionales
# 
# #### Faculty of Engineering
# - Ingeniería Civil Plan Común
# - Ingeniería Civil Industrial *(Doble Titulación)*
#   - Ingeniería Civil en Informática e Innovación Tecnológica *(Doble Titulación)*
#   - Ingeniería Civil en Informática e Inteligencia Artificial *(Nueva 2025, Doble Titulación)*
#   - Ingeniería Civil en Minería
# - Ingeniería Civil en Obras Civiles
# - Ingeniería Civil en BioMedicina *(Nueva 2025)*
#   - Geología
# - Data Business Intelligence

##################################
### Proximity matrix Faculties
##################################

# Define degrees grouped by faculty
faculties <- list(
  "Architecture and Design" = c("Arquitectura", "Diseño", "Cine", "Publicidad", "Bachillerato en Diseño"),
  "Law and Social Sciences" = c("Derecho", "Periodismo y Comunicación", "Bachillerato en Derecho, Ciencias Sociales y Humanidades"),
  "Government" = c("Ciencia Política y Políticas Públicas"),
  "Business and Economics" = c("Ingeniería Comercial", "Global Business Administration", "Bachillerato en Ingeniería Comercial"),
  "Medicine / Health Sciences" = c("Medicina", "Enfermería", "Kinesiología", "Tecnología Médica", "Nutrición y Dietética", "Odontología", "Obstetricia", "Terapia Ocupacional", "Química y Farmacia", "Fonoaudiología"),
  "Psychology" = c("Psicología", "Bachillerato en Psicología"),
  "Education" = c("Pedagogía en Educación Básica", "Pedagogía en Educación de Párvulos", "Programa de Formación Pedagógica"),
  "Engineering" = c("Ingeniería Civil Plan Común", "Ingeniería Civil Industrial", "Ingeniería Civil en Informática e Innovación Tecnológica", "Ingeniería Civil en Informática e Inteligencia Artificial", "Ingeniería Civil en Minería", "Ingeniería Civil en Obras Civiles", "Ingeniería Civil en BioMedicina", "Geología", "Data Business Intelligence")
)

# Flatten list into data.frame
degrees <- unlist(faculties)
names(degrees) <- NULL
all_pairs <- expand.grid(from = degrees, to = degrees, stringsAsFactors = FALSE)

# Label proximity
all_pairs$proximity <- apply(all_pairs, 1, function(row) {
  same_faculty <- any(sapply(faculties, function(degs) row["from"] %in% degs && row["to"] %in% degs))
  if (row["from"] == row["to"]) "self" else if (same_faculty) "near" else "far"
})

# Convert to matrix
proximity_matrix <- reshape2::acast(all_pairs, from ~ to, value.var = "proximity")

# View subset
proximity_matrix[1:5, 1:5]


##########################################################################################
#### Proximity matrix Faculties - recoded so each has aprox 5-10 degrees considered near. 
##########################################################################################




# Define degrees grouped by macro-faculty
macro_faculties <- list(
  "Health Sciences & Medicine" = c("Medicina", "Enfermería", "Kinesiología", "Tecnología Médica", "Nutrición y Dietética", "Odontología", "Obstetricia", "Terapia Ocupacional", "Química y Farmacia", "Fonoaudiología"),
  "Engineering & Applied Sciences" = c("Ingeniería Civil Plan Común", "Ingeniería Civil Industrial", "Ingeniería Civil en Informática e Innovación Tecnológica", "Ingeniería Civil en Informática e Inteligencia Artificial", "Ingeniería Civil en Minería", "Ingeniería Civil en Obras Civiles", "Ingeniería Civil en BioMedicina", "Geología", "Data Business Intelligence"),
  "Arts, Design & Communication" = c("Arquitectura", "Diseño", "Cine", "Publicidad", "Periodismo y Comunicación", "Bachillerato en Diseño"),
  "Social Sciences, Law, Business & Education" = c("Derecho", "Ingeniería Comercial", "Global Business Administration", "Bachillerato en Ingeniería Comercial", "Ciencia Política y Políticas Públicas", "Pedagogía en Educación Básica", "Pedagogía en Educación de Párvulos", "Programa de Formación Pedagógica", "Psicología", "Bachillerato en Psicología")
)

# Flatten list into data.frame
macro_degrees <- unlist(macro_faculties)
names(macro_degrees) <- NULL
all_macro_pairs <- expand.grid(from = macro_degrees, to = macro_degrees, stringsAsFactors = FALSE)

# Label proximity
all_macro_pairs$proximity <- apply(all_macro_pairs, 1, function(row) {
  same_macro <- any(sapply(macro_faculties, function(degs) row["from"] %in% degs && row["to"] %in% degs))
  if (row["from"] == row["to"]) "self" else if (same_macro) "near" else "far"
})

# Convert to matrix
macro_proximity_matrix <- reshape2::acast(all_macro_pairs, from ~ to, value.var = "proximity")

# View subset
macro_proximity_matrix[1:5, 1:5]










