<!DOCTYPE html>
  <html lang="en">
    <head>
    <meta charset="UTF-8">
      <title>CPR Game - Decisión</title>
      <style>
      body {
        font-family: sans-serif;
        text-align: center;
        padding: 2rem;
        background-color: #fdfdfd;
      }
    
    h2 {
      margin-bottom: 2rem;
    }
    
    .group-composition {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 3rem;
      margin-bottom: 2rem;
    }
    
    .player {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    
    .figure {
      width: 70px;
      height: 70px;
    }
    
    .label {
      margin-top: 0.5rem;
      font-weight: bold;
      font-size: 1rem;
    }
    
    .you svg, .you .label {
      color: #2A6773;
    }
    
    .near svg, .near .label {
      color: #655D73;
    }
    
    .far svg, .far .label {
      color: #C2A552;
    }
    
    .decision-box {
      background-color: #f5f5f5;
        border: 1px solid #ddd;
      border-radius: 10px;
      padding: 2rem;
      max-width: 600px;
      margin: 0 auto 2rem auto;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .decision-box p {
      font-size: 1rem;
      margin-bottom: 1.5rem;
    }
    
    .decision-box input[type="number"] {
      padding: 0.5rem;
      font-size: 1rem;
      width: 80px;
      margin-top: 0.5rem;
    }
    
    button {
      padding: 0.6rem 1.5rem;
      font-size: 1rem;
      background-color: #2A6773;
        color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      margin-top: 1.5rem;
    }
    
    .small-text {
      font-size: 0.75rem;
      line-height: 1.4;
      max-width: 600px;
      margin: 0 auto;
      text-align: justify;
      color: #444;
    }
    </style>
      </head>
      <body>
      
      <h2>Ronda [t] - Decisión</h2>
      
      <div class="group-composition">
      <!-- YOU -->
      <div class="player you">
      <svg class="figure" viewBox="0 0 64 64">
      <circle cx="32" cy="10" r="6" fill="currentColor"/>
      <line x1="32" y1="16" x2="32" y2="36" stroke="currentColor" stroke-width="4"/>
      <line x1="20" y1="22" x2="44" y2="22" stroke="currentColor" stroke-width="4"/>
      <line x1="32" y1="36" x2="24" y2="52" stroke="currentColor" stroke-width="4"/>
      <line x1="32" y1="36" x2="40" y2="52" stroke="currentColor" stroke-width="4"/>
      </svg>
      <div class="label">Tú - [Tu carrera]</div>
      </div>
      
      <!-- NEAR -->
      <div class="player near">
      <svg class="figure" viewBox="0 0 64 64">
      <circle cx="32" cy="10" r="6" fill="currentColor"/>
      <line x1="32" y1="16" x2="32" y2="36" stroke="currentColor" stroke-width="4"/>
      <line x1="20" y1="22" x2="44" y2="22" stroke="currentColor" stroke-width="4"/>
      <line x1="32" y1="36" x2="24" y2="52" stroke="currentColor" stroke-width="4"/>
      <line x1="32" y1="36" x2="40" y2="52" stroke="currentColor" stroke-width="4"/>
      </svg>
      <div class="label">Jugador(a) 2 - [Carrera cercana]</div>
      </div>
      
      <!-- FAR -->
      <div class="player far">
      <svg class="figure" viewBox="0 0 64 64">
      <circle cx="32" cy="10" r="6" fill="currentColor"/>
      <line x1="32" y1="16" x2="32" y2="36" stroke="currentColor" stroke-width="4"/>
      <line x1="20" y1="22" x2="44" y2="22" stroke="currentColor" stroke-width="4"/>
      <line x1="32" y1="36" x2="24" y2="52" stroke="currentColor" stroke-width="4"/>
      <line x1="32" y1="36" x2="40" y2="52" stroke="currentColor" stroke-width="4"/>
      </svg>
      <div class="label">Jugador(a) 3 - [Carrera lejana]</div>
      </div>
      </div>
      
      <!-- Decision Box -->
      <div class="decision-box">
      <p>
      Recursos disponibles para el grupo:<br>
      <strong>[(Monto recurso en t-1 - extracción en t-1) * factor regeneración]</strong>
      </p>
      
      <form>
      <label for="extraction">¿Cuántos recursos quieres extraer en esta ronda?</label>
      <br><br>
      <input type="number" id="extraction" name="extraction" min="0" max="76" required>
      <br><br>
      <button type="submit">Continuar</button>
      </form>
      </div>
      
      <!-- Notes -->
      <p class="small-text">
      Recuerde: Si la suma total extraída por los 3 integrantes del grupo supera los recursos disponibles en esta ronda, los recursos se asignarán al azar. Primero se elige aleatoriamente a una persona para asignarle su extracción completa (si hay suficientes recursos). Luego, si queda recurso disponible, se asigna a una segunda persona, y finalmente, si aún hay recursos, se le entrega lo restante a la tercera persona.
    <br><br>
      Si se acaban todos los recursos en esta ronda, el juego se comenzará de nuevo.
    </p>
      
      </body>
      </html>