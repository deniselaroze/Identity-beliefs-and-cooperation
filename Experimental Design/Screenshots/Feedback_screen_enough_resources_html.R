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
    
    .highlight {
      font-weight: bold;
      color: #2A6773;
    }
    </style>
      </head>
      <body>
      
      <h2>Ronda [t] - Resultados</h2>
      
      <div class="feedback-box">
      
      <!-- Extraction Summary -->
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
      <strong>Promedio de los otros jugadores:</strong> 22.5 tokens
    </div>
      
      <div class="summary-line"><strong>Total extraído:</strong> 70 tokens</div>
      <div class="summary-line"><strong>Recursos disponibles:</strong> 70 tokens</div>
      <div class="summary-line"><strong>Regeneración (+20%):</strong> 6 tokens</div>
      <div class="summary-line"><strong>Total disponible para próxima ronda:</strong> 76 tokens</div>
      
      <hr>
      
      <!-- NO CONFLICT BLOCK (SHOW IF all_extracted <= available) -->
      <div id="no-conflict">
      <div class="summary-line">
      ✅ <span class="highlight">Todos/as recibieron lo que solicitaron.</span>
      </div>
      <div class="summary-line">
      <strong>Tu ganancia:</strong> 25 tokens × 2 = <span class="highlight">50 puntos</span>
      </div>
      </div>
      
      <!-- CONFLICT BLOCK (SHOW IF all_extracted > available) -->
      <!-- Uncomment this if conflict applies instead -->
      <!--
      <div id="conflict">
      <div class="summary-line">
      ⚠️ <span class="highlight">El grupo solicitó más recursos de los disponibles.</span>
      </div>
      <div class="summary-line"><strong>Orden aleatorio:</strong> Jugador(a) 2 → Tú → Jugador(a) 3</div>
      <div class="summary-line"><strong>Tu posición:</strong> 2º</div>
      <div class="summary-line"><strong>Recibiste:</strong> 20 tokens</div>
      <div class="summary-line"><strong>Tu ganancia:</strong> 20 × 2 = <span class="highlight">40 puntos</span></div>
      </div>
      -->
      
      </div>
      
      <p class="small-text">
      El pozo de recursos se regenera parcialmente al final de cada ronda. Si llega a cero, el juego reinicia con el pozo completo en la ronda 1.
    </p>
      
      <button>Continuar</button>
      
      </body>
      </html>
      