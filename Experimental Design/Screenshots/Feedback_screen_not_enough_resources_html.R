<!DOCTYPE html>
  <html lang="es">
    <head>
    <meta charset="UTF-8">
      <title>CPR Game - Resultados</title>
      <style>
      body {
        font-family: sans-serif;
        text-align: center;
        padding: 2rem;
        background-color: #fff;
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
    
    .you svg, .you .label {
      color: #2A6773;
    }
    
    .near svg, .near .label {
      color: #655D73;
    }
    
    .far svg, .far .label {
      color: #C2A552;
    }
    
    .feedback-box {
      border: 1px solid #ccc;
      border-radius: 8px;
      padding: 1.5rem;
      margin: 2rem auto;
      max-width: 500px;
      background-color: #f9f9f9;
        text-align: left;
    }
    
    .summary-line {
      font-size: 1rem;
      margin: 1rem 0;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    
    .small-text {
      font-size: 0.7rem;
      line-height: 1.4;
      max-width: 600px;
      margin: 0 auto;
      text-align: justify;
    }
    
    .icon {
      width: 28px;
      height: 28px;
    }
    
    button {
      padding: 0.6rem 1.2rem;
      font-size: 1rem;
      background-color: #2A6773;
        color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      margin-top: 2rem;
    }
    
    hr {
      margin: 1.5rem 0;
      border: none;
      border-top: 1px solid #ccc;
    }
    </style>
      </head>
      <body>
      
      <h2>Ronda [t] - Resultados</h2>
      
      <div class="feedback-box">
      <div class="summary-line">
      <svg class="icon" viewBox="0 0 64 64">
      <circle cx="32" cy="10" r="6" fill="#2A6773"/>
      <line x1="32" y1="16" x2="32" y2="36" stroke="#2A6773" stroke-width="4"/>
      <line x1="20" y1="22" x2="44" y2="22" stroke="#2A6773" stroke-width="4"/>
      <line x1="32" y1="36" x2="24" y2="52" stroke="#2A6773" stroke-width="4"/>
      <line x1="32" y1="36" x2="40" y2="52" stroke="#2A6773" stroke-width="4"/>
      </svg>
      <strong>Tú extrajiste:</strong> 25 tokens
    </div>
      
      <div class="summary-line">
      <svg class="icon" viewBox="0 0 64 64">
      <circle cx="32" cy="10" r="6" fill="#655D73"/>
      <line x1="32" y1="16" x2="32" y2="36" stroke="#655D73" stroke-width="4"/>
      <line x1="20" y1="22" x2="44" y2="22" stroke="#655D73" stroke-width="4"/>
      <line x1="32" y1="36" x2="24" y2="52" stroke="#655D73" stroke-width="4"/>
      <line x1="32" y1="36" x2="40" y2="52" stroke="#655D73" stroke-width="4"/>
      </svg>
      <svg class="icon" viewBox="0 0 64 64">
      <circle cx="32" cy="10" r="6" fill="#C2A552"/>
      <line x1="32" y1="16" x2="32" y2="36" stroke="#C2A552" stroke-width="4"/>
      <line x1="20" y1="22" x2="44" y2="22" stroke="#C2A552" stroke-width="4"/>
      <line x1="32" y1="36" x2="24" y2="52" stroke="#C2A552" stroke-width="4"/>
      <line x1="32" y1="36" x2="40" y2="52" stroke="#C2A552" stroke-width="4"/>
      </svg>
      <strong>Promedio de los otros jugadores:</strong> 32.5 tokens
    </div>
      
      <div class="summary-line"><strong>Total solicitado por el grupo:</strong> 90 tokens</div>
      <div class="summary-line"><strong>Recursos disponibles:</strong> 70 tokens</div>
      <div class="summary-line"><strong>Situación:</strong> Se solicitó más de lo disponible.</div>
      <div class="summary-line"><strong>Orden aleatorio de asignación:</strong> Jugador(a) 2 → Tú → Jugador(a) 3</div>
      <div class="summary-line"><strong>Tu posición en el orden:</strong> 2º</div>
      <div class="summary-line"><strong>Recibiste:</strong> 25 tokens</div>
      <div class="summary-line"><strong>Ganancia en esta ronda:</strong> 50 puntos</div>
      
      <hr>
      
      <div class="summary-line"><strong>Total extraído:</strong> 70 tokens</div>
      <div class="summary-line"><strong>Recursos restantes antes de regeneración:</strong> 0 tokens</div>
      <div class="summary-line"><strong>Regeneración (+20%):</strong> 0 tokens</div>
      <div class="summary-line"><strong>Total de recursos disponibles para la próxima ronda:</strong> 0 tokens</div>
      </div>
      
      <p class="small-text">
      El pozo de recursos se regeneró parcialmente al final de la ronda. Si los recursos llegan a cero, el juego comienza de nuevo en la ronda 1 con el pozo lleno.
    </p>
      
      <button>Continuar</button>
      
      </body>
      </html>