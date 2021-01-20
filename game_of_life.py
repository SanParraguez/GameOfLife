"""
Juego de la vida
https://www.youtube.com/watch?v=xgZuW6Jz5dc

Santiago Parraguez C.
"""
import pygame
import numpy as np
import time

print('Presione cualquier tecla para pausar o reanudar')
print('Presione ESC para salir')

#%% JUEGO DE LA VIDA
pygame.init()

# Caracteristicas de la pantalla
width, height = 600, 600

nxC, nyC = 60, 60
dim_cw = (width-1)  / nxC
dim_ch = (height-1) / nyC

# Estado inicial del juego
gameState = np.zeros((nxC, nyC))
gameState[21,21] = 1
gameState[22,22] = 1
gameState[22,23] = 1
gameState[21,23] = 1
gameState[20,23] = 1

# Control de ejecución del juego
pauseExect = False

screen = pygame.display.set_mode((height, width))

bg = 50, 50, 50
screen.fill(bg)

gaming = 1
while gaming == 1:
      
    screen.fill(bg)
    
    new_gameState = np.copy(gameState) # Crear nuevo estado
    
    # Registramos eventos en teclado y ratón
    ev = pygame.event.get()
    
    for event in ev:
        # Detectar si se presiona una tecla
        if event.type == pygame.KEYDOWN:
            if event.key == 27: gaming = 0
            pauseExect = not pauseExect
        
        # Detectar si se presiona un botón del ratón
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dim_cw)), int(np.floor(posY / dim_ch))
            new_gameState[celX, celY] = not mouseClick[2]
    
    for y in range(0, nyC):
        for x in range(0, nxC):
            
            if not pauseExect:
                # ================ REGLAS ====================
                n_neigh = gameState[(x-1)%nxC, (y-1)%nyC] + \
                          gameState[(x  )%nxC, (y-1)%nyC] + \
                          gameState[(x+1)%nxC, (y-1)%nyC] + \
                          gameState[(x-1)%nxC, ( y )%nyC] + \
                          gameState[(x+1)%nxC, ( y )%nyC] + \
                          gameState[(x-1)%nxC, (y+1)%nyC] + \
                          gameState[(x  )%nxC, (y+1)%nyC] + \
                          gameState[(x+1)%nxC, (y+1)%nyC]
                            
                # Regla 1: Una célula muerta con exactamente 3 células vecinas vivas, nace
                if gameState[x,y] == 0 and n_neigh == 3: new_gameState[x,y] = 1
                # Regla 2: Una célula viva con 2 o 3 células vecinas vivas sigue viva, en otro caso muere
                elif gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3): new_gameState[x,y] = 0
                
            # Dibujar los cuadraditos
            poly = [((x)   * dim_cw, (y)   * dim_ch),
                    ((x+1) * dim_cw, (y)   * dim_ch),
                    ((x+1) * dim_cw, (y+1) * dim_ch),
                    ((x)   * dim_cw, (y+1) * dim_ch)]
            
            if new_gameState[x,y] == 0:
                pygame.draw.polygon(screen, (120,120,120), poly, 1)
            else:
                pygame.draw.polygon(screen, (250,250,250), poly, 0)
    
    # Actualizar estado
    gameState = np.copy(new_gameState)       
    
    # Actualizar pantalla
    pygame.display.flip()  
    time.sleep(0.02)
    
pygame.display.quit()
