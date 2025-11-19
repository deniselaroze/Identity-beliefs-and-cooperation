<!DOCTYPE html>
  <html lang="es">
    <head>
    <meta charset="UTF-8">
      <title>CPR Game – Encuesta Final</title>
      <style>
      body {
        font-family: sans-serif;
        text-align: center;
        padding: 2rem;
        background: #fff;
      }
    .welcome-box {
      border: 1px solid #ccc;
      border-radius: 10px;
      padding: 2.5rem 2rem;
      margin: 4rem auto 2rem auto;
      max-width: 480px;
      background-color: #f9f9f9;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
      text-align: left;
    }
    .icon {
      width: 58px;
      height: 58px;
      display: block;
      margin: 0 auto 1.2rem auto;
    }
    h1 {
      font-size: 2rem;
      color: #2A6773;
        margin-bottom: 1.3rem;
      font-weight: bold;
      text-align: center;
    }
    label {
      display: block;
      margin: 1.1rem 0 0.2rem 0;
      color: #222;
        font-size: 1.08rem;
      font-weight: bold;
    }
    select, input[type="number"], input[type="text"], input[type="radio"] {
      width: 100%;
      padding: 0.4rem;
      font-size: 1rem;
      margin-bottom: 0.7rem;
      border-radius: 5px;
      border: 1px solid #bdbdbd;
      box-sizing: border-box;
    }
    textarea {
      width: 100%;
      padding: 0.5rem;
      font-size: 1rem;
      border-radius: 6px;
      border: 1px solid #ccc;
      resize: vertical;
      margin-top: 0.5rem;
      min-height: 70px;
      margin-bottom: 0.8rem;
    }
    .inline-radio {
      display: flex;
      gap: 1.5rem;
      margin-bottom: 1rem;
      margin-top: 0.2rem;
    }
    .inline-radio label {
      font-weight: normal;
      margin: 0;
      font-size: 1rem;
      color: #333;
        display: flex;
      align-items: center;
    }
    .btn-wrap {
      text-align: center;
    }
    button {
      padding: 0.8rem 2.2rem;
      font-size: 1.09rem;
      background-color: #2A6773;
        color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      margin-top: 2.2rem;
      transition: background 0.2s;
      display: inline-block;
    }
    button:hover {
      background-color: #1d4851;
    }
    .footer {
      margin-top: 1.4rem;
      font-size: 0.97rem;
      color: #444;
        text-align: center;
    }
    .hidden { display: none; }
    </style>
      </head>
      <body>
      <div class="welcome-box">
      <svg class="icon" viewBox="0 0 64 64">
      <circle cx="32" cy="10" r="8" fill="#2A6773"/>
      <line x1="32" y1="18" x2="32" y2="46" stroke="#2A6773" stroke-width="5"/>
      <line x1="20" y1="28" x2="44" y2="28" stroke="#2A6773" stroke-width="5"/>
      <line x1="32" y1="46" x2="20" y2="60" stroke="#2A6773" stroke-width="5"/>
      <line x1="32" y1="46" x2="44" y2="60" stroke="#2A6773" stroke-width="5"/>
      </svg>
      <h1>Encuesta Final</h1>
      <form id="exit-form" autocomplete="off">
      
      <!-- Edad -->
      <label for="edad">¿Cuál es tu edad?</label>
      <input type="number" min="16" max="100" id="edad" name="edad" required>
      
      <!-- Género -->
      <label>¿Con qué género te identificas?</label>
      <div class="inline-radio">
      <label><input type="radio" name="genero" value="Femenino" required> Femenino</label>
      <label><input type="radio" name="genero" value="Masculino" required> Masculino</label>
      <label><input type="radio" name="genero" value="Otro" required> Otro</label>
      <label><input type="radio" name="genero" value="Prefiero no decirlo" required> Prefiero no decirlo</label>
      </div>
      
      <!-- Años en la carrera -->
      <label for="aniosCarrera">¿Cuántos años llevas estudiando tu carrera?</label>
      <select id="aniosCarrera" name="aniosCarrera" required>
      <option value="" disabled selected>Selecciona una opción...</option>
      <option value="1">1 año</option>
      <option value="2">2 años</option>
      <option value="3">3 años</option>
      <option value="4">4 años</option>
      <option value="5">5 años</option>
      <option value="6">6 años</option>
      <option value="7">7 años</option>
      <option value="8">8 años</option>
      <option value="9">9 años</option>
      <option value="10+">10 años o más</option>
      </select>
      
      <!-- Curso en otra facultad -->
      <label>¿Has tomado algún curso en otra facultad?</label>
      <div class="inline-radio">
      <label><input type="radio" name="otraFacultad" value="Sí" required> Sí</label>
      <label><input type="radio" name="otraFacultad" value="No" required> No</label>
      </div>
      
      <div id="otraFacultadDatos" class="hidden">
      <label for="facultadOtra">¿En qué facultad?</label>
      <select id="facultadOtra" required>
      <option value="" disabled selected>Seleccione la facultad...</option>
      <option>Arquitectura y Arte</option>
      <option>Ciencias de la Salud</option>
      <option>Comunicaciones</option>
      <option>Derecho</option>
      <option>Diseño</option>
      <option>Economía y Negocios</option>
      <option>Ingeniería</option>
      <option>Medicina Clínica Alemana UDD</option>
      <option>Psicología</option>
      </select>
      <label for="carreraOtra">¿Qué carrera?</label>
      <select id="carreraOtra" required>
      <option value="" disabled selected>Seleccione la carrera...</option>
      </select>
      </div>
      
      <!-- Representante de curso -->
      <label>¿Has sido representante de curso alguna vez?</label>
      <div class="inline-radio">
      <label><input type="radio" name="representante" value="Sí" required> Sí</label>
      <label><input type="radio" name="representante" value="No" required> No</label>
      </div>
      
      <!-- Ha gestionado un presupuesto -->
      <label>¿Has gestionado algún presupuesto (por ejemplo, centro de alumnos, grupo de estudiantes, etc.)?</label>
      <div class="inline-radio">
      <label><input type="radio" name="presupuesto" value="Sí" required> Sí</label>
      <label><input type="radio" name="presupuesto" value="No" required> No</label>
      </div>
      
      <!-- Reflexión final -->
      <label for="comentarioFinal">¿Te gustaría comentar algo sobre tu experiencia en este estudio?</label>
      <textarea id="comentarioFinal" name="comentarioFinal" placeholder="Escribe aquí tu reflexión"></textarea>
      
      <div class="btn-wrap">
      <button type="submit">Continuar</button>
      </div>
      </form>
      <div class="footer">
      
      </div>
      </div>
      <script>
      // Mapeo de facultades a carreras
    const degreesByFaculty = {
      "Arquitectura y Arte": ["Arquitectura"],
      "Ciencias de la Salud": [
        "Enfermería","Kinesiología","Nutrición y Dietética",
        "Odontología","Tecnología Médica","Terapia Ocupacional","Fonoaudiología"
      ],
      "Comunicaciones": [
        "Cine","Periodismo y Comunicación","Publicidad"
      ],
      "Derecho": ["Derecho"],
      "Diseño": ["Diseño"],
      "Economía y Negocios": [
        "Ingeniería Comercial","Global Business Administration","Data Business Intelligence"
      ],
      "Ingeniería": [
        "Ingeniería Civil en Informática e Innovación Tecnológica",
        "Ingeniería Civil en Informática e Inteligencia Artificial",
        "Ingeniería Civil Industrial",
        "Ingeniería Civil en Obras Civiles",
        "Ingeniería Civil en Minería",
        "Ingeniería Civil Plan Común",
        "Geología",
        "Ingeniería Civil en BioMedicina"
      ],
      "Medicina Clínica Alemana UDD": [
        "Medicina","Enfermería","Kinesiología","Nutrición y Dietética",
        "Odontología","Tecnología Médica","Terapia Ocupacional","Fonoaudiología"
      ],
      "Psicología": ["Psicología"]
    };
    
    // Mostrar facultad y carrera solo si responde sí a otraFacultad
    document.querySelectorAll('input[name="otraFacultad"]').forEach(function(el) {
      el.addEventListener('change', function() {
        const show = el.value === "Sí";
        document.getElementById('otraFacultadDatos').style.display = show ? "block" : "none";
        if(!show) {
          document.getElementById('facultadOtra').value = "";
          document.getElementById('carreraOtra').innerHTML = '<option value="" disabled selected>Seleccione la carrera...</option>';
        }
      });
    });
    
    // Desplegar carreras según facultad seleccionada
    document.getElementById('facultadOtra').addEventListener('change', function() {
      const faculty = this.value;
      const carreraOtra = document.getElementById('carreraOtra');
      carreraOtra.innerHTML = '<option value="" disabled selected>Seleccione la carrera...</option>';
      if(faculty && degreesByFaculty[faculty]) {
        degreesByFaculty[faculty].forEach(function(carrera) {
          const opt = document.createElement('option');
          opt.value = carrera;
          opt.textContent = carrera;
          carreraOtra.appendChild(opt);
        });
      }
    });
    
    // Validación básica para asegurar que todas las preguntas (menos el comentario) están respondidas
    document.getElementById('exit-form').addEventListener('submit', function(e) {
      // Validar campos tipo select que no aceptan required por defecto
      if (!document.getElementById('aniosCarrera').value) {
        alert("Por favor, selecciona cuántos años llevas estudiando tu carrera.");
        document.getElementById('aniosCarrera').focus();
        e.preventDefault();
        return;
      }
      if(document.querySelector('input[name="otraFacultad"]:checked')?.value === "Sí") {
        if(!document.getElementById('facultadOtra').value) {
          alert("Por favor, indica la facultad del curso en otra facultad.");
          document.getElementById('facultadOtra').focus();
          e.preventDefault();
          return;
        }
        if(!document.getElementById('carreraOtra').value) {
          alert("Por favor, indica la carrera del curso en otra facultad.");
          document.getElementById('carreraOtra').focus();
          e.preventDefault();
          return;
        }
      }
    });
    </script>
      </body>
      </html>
      