<!DOCTYPE html>
  <html lang="es">
    <head>
    <meta charset="UTF-8">
      <title>CPR Game – Reflexión sobre tu carrera</title>
      <style>
      body {
        font-family: sans-serif;
        text-align: center;
        padding: 2rem;
        background-color: #fff;
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
    h1 {
      font-size: 1.9rem;
      color: #2A6773;
        margin-bottom: 1.3rem;
      text-align: center;
    }
    p {
      font-size: 1.1rem;
      color: #222;
        text-align: justify;
    }
    textarea {
      width: 100%;
      height: 150px;
      padding: 0.5rem;
      font-size: 1rem;
      border-radius: 6px;
      border: 1px solid #ccc;
      resize: vertical;
      margin-top: 1rem;
    }
    .note {
      font-size: 0.9rem;
      color: #555;
        margin-top: 0.3rem;
    }
    button {
      padding: 0.8rem 2.2rem;
      font-size: 1.09rem;
      background-color: #2A6773;
        color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      margin-top: 1.5rem;
      transition: background 0.2s;
      display: block;
      margin-left: auto;
      margin-right: auto;
    }
    button:hover {
      background-color: #1d4851;
    }
    </style>
      </head>
      <body>
      <div class="welcome-box">
      <h1>Reflexión sobre tu carrera</h1>
      <p>
      Por favor, piensa en tu experiencia como estudiante de tu carrera universitaria. En el recuadro a continuación, describe brevemente una experiencia positiva que hayas tenido siendo estudiante de esta carrera. ¿Qué ocurrió? ¿Por qué la consideras significativa?
      </p>
      <textarea id="reflection" placeholder="Escribe aquí tu experiencia..."></textarea>
      <div class="note">Debes escribir al menos <strong>250 caracteres</strong>.</div>
      <button type="button" id="continueBtn">Continuar</button>
      </div>
      
      <script>
      const textarea = document.getElementById('reflection');
    const btn = document.getElementById('continueBtn');
    
    btn.addEventListener('click', () => {
      const text = textarea.value.trim();
      if (text.length < 250) {
        alert(`Por favor, escribe al menos 250 caracteres. Llevas ${text.length}.`);
        return;
      }
      // Aquí puedes proceder a la siguiente pantalla, por ejemplo:
        // window.location.href = 'next_screen.html';
        console.log('Texto válido — continuar');
    });
    </script>
      </body>
      </html>
      