import pygame
from musica import *
from pygame import mixer
from player import *
from invaders import *
from sys import exit
from os.path import join
from config import *
from fire import *
from dropdown import *
from obstacles import *

# initialização do pygame (por isso, ao sair do loop do jogo, pygame.quit é necessario)
pygame.init()
mixer.init()

# Algumas configurações iniciais, será necessário reescrever para um codigo
# baseado em OOP
score = 0
nivel = 1
registrou = False   
# to com fome
# Clean code
# PEP8
# OOP 

fps = 60
dropdown.index_selecionado = 1

# Inicializa uma font para posteriormente ser utilizada como surface
font = pygame.font.Font(join('font', 'pixeled.ttf'), 16)

def display_score():
    score_surface = font.render(f'Score: {score}', False, 'white')
    score_rect = score_surface.get_rect(topleft = (10, -10))
    display.blit(score_surface, score_rect)

def display_level_atual(nivel):
    level_surface = font.render(f'Level: {nivel}', False, 'white')
    level_rect = level_surface.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2))
    display.blit(level_surface, level_rect)

def collisions():
    # utilizar global não é recomendado, pode causar um bug inesperado
    # a ideia é transformar tudo para OOP
    '''
    função que será utilizada para TODAS as colisões que ocorrem no jogo
    '''
    global score, lifes_left    # vasco
    
    if player_fire and (nivel % 10 == 0):   # Se o grupo do player_fire for
                                            # falsy o programa nao mostrou o
                                            # tiro do player.
                                            # Alem disso, se o resto da divisao
                                            # do booleano do nivel for igual a
                                            # 0, o codigo resultara em true.  

        boss_hitted = pygame.sprite.groupcollide(
                        invader_group, player_fire,
                        False, True, pygame.sprite.collide_mask
                        )
        # Se true (atingido) vai colidir.
        if boss_hitted:  # se atingido

            for boss in boss_hitted:
                boss.health_left -= 1
                
                # Adicionar efeitos especiais
                explosion_group.add(Explosion(boss.rect.center))
                som_invader_morto.play()              
                
                if boss.health_left == 0:   # se hp menor/igual a que um
                    invader_group.empty()
                    break
                
    else:
        # --> Se invader for atingido, ele desaparece e o tiro também (true, true).
        invader_hitted = pygame.sprite.groupcollide(invader_group, player_fire, True, True, pygame.sprite.collide_mask) 
        
        if invader_hitted: # --> Caso Invader atingido
            #invader_group.empty() # Hack para matar todos com um tiro.
            
            # Loop para ir matando os invaders e dando pontos.
            for invader in invader_hitted:
                score += invader.reward
                explosion_group.add(Explosion(invader.rect.center))
            som_invader_morto.play()

    # --> Se atingir o Invader Special, adiciona ponto e faz a explosão
    if pygame.sprite.groupcollide(player_fire, special_invader_group, True, True):
        explosion_group.add(Explosion(special_invader.rect.center))
        score += special_invader.reward


    # Para cada tiro que atinge o obstaculo ele "mata" o tiro e o obstaculo, diminuindo o cooldown do tiro.
    for fire in player_fire: 
        for obstacle in obstacle_group: 
            if pygame.sprite.collide_rect(fire, obstacle):
                if pygame.sprite.collide_mask(fire, obstacle):
                    player.cooldown = 10
                    fire.kill()
                    obstacle.kill()
                    break

            else:
                player.cooldown = 350   

    # pygame.sprite.groupcollide(obstacle_group, player_fire, True, True, pygame.sprite.collide_mask)
    
    # --> Quando o tiro do invader atinge o obstacle os dois somem. 
    pygame.sprite.groupcollide(obstacle_group, invader_fire, True, True)


    # --> For para saber onde o tiro do Invader atinge

    for fire in invader_fire:
        # --> Caso o tiro atinge o Player ele tira uma vida
        if pygame.sprite.spritecollide(fire, player_sprite, False, pygame.sprite.collide_mask):
            explosion_group.add(Explosion(fire.rect.center))
            fire.kill() # -> Tiro some
            som_ship_exp.play()
            lifes_left -= 1

        # --> Se o tiro atinge outro tiro (do player no caso) os dois somem(True, fire.kill()).
        if pygame.sprite.spritecollide(fire, player_fire, True, pygame.sprite.collide_rect):
            explosion_group.add(Explosion(fire.rect.center))
            som_invader_morto.play()
            fire.kill()



def update_and_draw() -> None:
    """ 
    Função que atualiza a tela e desenha as sprites

    """
    global game_state 
    if game_state != 'transition':
        special_invader_group.update()
        special_invader_group.draw(display)

        invader_group.update()
        invader_group.draw(display)

        invader_fire.update()
        invader_fire.draw(display)
        
        player_sprite.update()
        player_sprite.draw(display)

        player_fire.update()
        # print(player_fire.sprites())
        player_fire.draw(display)

        explosion_group.update()
        explosion_group.draw(display)
         
        obstacle_group.update()
        obstacle_group.draw(display)
        
    else:    
        player_sprite.draw(display)
        obstacle_group.draw(display)
        explosion_group.empty()
        player_fire.empty()
        invader_fire.empty()

def pause_menu():
    '''
    Menu de pausa\n
    Serve para pausar o jogo.\n
    Se 'esc' key for pressionada, inicia a açao de pausa da funçao. O que
    permite o jogador a ter acesso a funcionalidades do jogo.
    Alem de desenhar e congelar o posicionamento dos sprites na tela para a
    visualizaçao do jogador.
    '''
    
    # Usado para mostrar os sprites e o seu posicionamento na tela de pause.
    invader_group.draw(display)
    player_sprite.draw(display)
    player_fire.draw(display)
    invader_fire.draw(display)
    special_invader_group.draw(display) 
    explosion_group.draw(display)
    obstacle_group.draw(display)
    

    # Se botao de 'Play' for mostrado.
    if ps_play_button.draw(display):
        global pause_screen # A variavel sera valida para todo o programa.
        pause_screen = False # Enquanto 'false', o jogo estara pausado.

    # Se botao de 'Options' for mostrado.
    if ps_options.draw(display):
        global game_state
        game_state = 'ps_options'

    # Se botao de 'Back to menu' for mostrado
    if ps_back_to_menu_button.draw(display):
        global nivel
        reset_game() # Reseta o jogo
        game_state = 'menu'

    # Se botao de 'Exit game' for mostrado
    if ps_exit_game.draw(display):
        pygame.quit()
        exit()  # Sai do jogo

def reset_game():
    '''
    Reinicia o jogo.\n
    Reseta o jogo usando o escopo global.
    '''
    # O global e usado para setar os valores nas variaveis em um escopo global.
    global score, lifes_left, pause_screen, registrou, nivel, player
    
    # Vai restaurar para conf inicial se o jogo estiver em game over ou menu .
    if game_state in ('game_over', 'menu'):
        registrou = False
        score = 0
        lifes_left = 5
        nivel = 1
        pause_screen = False
        
        obstacle_group.empty()
        create_obstacles()

        player_sprite.empty()
        player = create_player()

    # if obstacle_group:
    #     if nivel < 10:
    #         for obstacle in obstacle_group:
    #             if obstacle.rect.right < 10 + 25 * nivel:
    #                 obstacle.kill()
                
    #             if obstacle.rect.left > LARGURA_TELA - 25 - 25 * nivel:
    #                 obstacle.kill()
    #     else:
    #         obstacle_group.empty()
 
    # Reiniciando setup para o prox level.
    invader_fire.empty()
    invader_group.empty() 
    create_invaders(nivel)
    special_invader_group.empty()
    player_fire.empty()

def options():
    display.blit(options_background, (0, 0))
    tocar_musica()
    #opções de audio
    musica_text = font.render("Volume da Musica:", True, 'white')
    display.blit(musica_text, (345, 200))

    efeitos_text = font.render("Volume dos Efeitos:", True, 'white')
    display.blit(efeitos_text, (345, 300))

    volume_musica = musica_slider.draw(display)
    volume_efeitos = efeitos_slider.draw(display)

    volume_musica_percent = volume_musica / 100
    mixer.music.set_volume(volume_musica_percent)

    volume_efeitos_percent = volume_efeitos / 100
    som_invader_morto.set_volume(volume_efeitos_percent)
    som_ship_exp.set_volume(volume_efeitos_percent)
    som_shoot.set_volume(volume_efeitos_percent)

    #opções de display
    brilho_text = font.render("Brilho:", True, 'white')
    display.blit(brilho_text, (430, 500))

    brilho = brilho_slider.draw(display)
  
    fps_text = font.render("Taxa de Atualizaçao:", True, 'white')
    display.blit(fps_text, (345, 400))  

    for evento in eventos:
        dropdown.handle_event(evento)

    dropdown.draw(display)

    if dropdown.index_selecionado == 0:
        fps = 30
        pygame.display.set_caption("Space Invaders - FPS: 30")
    elif dropdown.index_selecionado == 1:
        fps = 60
        pygame.display.set_caption("Space Invaders - FPS: 60")
    elif dropdown.index_selecionado == 2:
        fps = 120
        pygame.display.set_caption("Space Invaders - FPS: 120")
    elif dropdown.index_selecionado == 3:
        fps = 144
        pygame.display.set_caption("Space Invaders - FPS: 240")

def registrar_score():
    with open("scoreboard.txt", 'a') as arquivo:  # Modo 'a' adiciona ao final do arquivo
        arquivo.write(f'{user_text}')      # username
        arquivo.write(f'{score}' + '\n')          # score
    return True

def show_names_scores(lista_argumentos, numero_argumentos):
   
    names = [] # Armazena os nomes.
    scores = [] # Armazena os pontos.
    
    # Separa os nomes dos pontos.
    for index in range(numero_argumentos):
        if index % 2 == 0:
            names.append(lista_argumentos[index])
        else:
            scores.append(lista_argumentos[index])

    scores_values = [int(score) for score in scores] # Lista com os valores inteiros dos scores.
    highest_scores = [] # Armazena os maiores pontos.
    highest_names = [] # Armazena os nomes que fizeram os maiores pontos.

    # Exibe os nomes e os pontos, de acordo com as maiores pontuações.
    for score_index in range(len(scores)):
        if score_index <= 6:
            max_score = max(scores_values)
            index_max_score = scores_values.index(max_score)
            highest_scores.append(max_score)
            highest_names.append(names[index_max_score])
            scores_values.remove(max_score)
            names.remove(names[index_max_score])
            points_surface = font.render(f'{highest_scores[score_index]}', False, 'white')
            points_rect = points_surface.get_rect(topleft = ((745), (340+(score_index*50))))
            names_surface = font.render(f'{highest_names[score_index]}', False, 'white')
            names_rect = names_surface.get_rect(topleft = ((428), (340+(score_index*50))))
            display.blit(points_surface, points_rect)
            display.blit(names_surface, names_rect)

#Obstacle
create_obstacles()

#Invaders
create_invaders(nivel)

#Player
player = create_player()

running = True
clock = pygame.time.Clock()

game_state = 'player_identify'
pause_screen = False

mixer.music.play(-1)

# Jogo rodando em loop
while running:

    # limita a taxa de atualização da tela
    clock.tick(fps)

    # fundo com a cor da for_code
    display.fill("#1E1647")
    
    # enquanto o jogo esta rodando procuramos por eventos
    eventos = pygame.event.get()

    # for para tratar os eventos
    for event in eventos:
        
        # pygame.QUIT event significa que o usuario fechou a janela no X
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # logica username
        if event.type == pygame.KEYDOWN and game_state == 'player_identify':
            start_typing = True
            
            # digitar e apagar o texto
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode
            
            # se apertar ENTER, vai pro menu e salva o username    
            if event.key == pygame.K_RETURN:
                game_state = 'menu'
        
        #  se o jogo estiver rodando
        if game_state == 'playing':

            # esc in-game pausa o jogo e so despausa ao apertar esc novamente
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not pause_screen:
                print("pause")
                pause_screen = True

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and pause_screen:
                print("saindo do pause")
                pause_screen = False
                
            # caso aperte 0, o cooldown do player é reduzido
            if event.type == pygame.KEYDOWN and event.key == pygame.K_0 and game_state == 'playing':
                player.cooldown = 100

            # cria invaders
            if event.type == INVADERFIRE and not pause_screen:
                invaders_fire(-(8+nivel))

            # cria special invader  
            if event.type == SPECIALINVADER and not special_invader_group:
                special_invader = SpecialInvader()
                special_invader_group.add(special_invader)

    # Match para saber em que estado o jogo se encontra
    match game_state:

        # caso o estado seja player_identify (digitar o nome do jogador)
        case 'player_identify':
            display.fill("#1E1647") # fundo com a cor da for_code
            
            # cria a instrução para o jogador digitar seu nome
            instruction_surface = pygame.font.Font(join('font', 'pixeled.ttf'), 25).render('DIGITE SEU USERNAME:', True, '#FFFF00')
            instruction_rect = instruction_surface.get_rect()
            instruction_rect.center = (LARGURA_TELA // 2, 80)
            
            display.blit(instruction_surface, instruction_rect) # desenha a instrução na tela
            
            # se o jogador começou a digitar, mostre a instrução para apertar 'ENTER' para entrar no jogo
            if start_typing: 
                enter_name_surface = font.render('APERTE \'ENTER\' PARA ENTRAR NO JOGO', True, WHITE)
                enter_name_rect = enter_name_surface.get_rect()
                enter_name_rect.center = (LARGURA_TELA // 2, ALTURA_TELA - 30)
                
                # efeito de piscar o texto
                blink_time += clock.get_time()
                
                if blink_time >= 500:  # Alterna a cada 500ms (0.5 segundos)
                    show_text = not show_text 
                    blink_time = 0


                if show_text: # se show_text for True, mostre o texto
                    display.blit(enter_name_surface, enter_name_rect)
            
            # cria a surface com o texto digitado pelo jogador
            text_surface = font.render(user_text, True, WHITE)
            
            # cria um retângulo para centralizar o texto na tela
            text_rect = text_surface.get_rect()
            text_rect.center = (LARGURA_TELA // 2, ALTURA_TELA // 2)
            
            # desenha o texto na tela
            display.blit(text_surface, text_rect)
    
        case 'menu':
            reset_game()
            tocar_musica()
            
            display.blit(menu_background, (0,0))

            if scoreboard_button.draw(display):
                game_state = 'scoreboard'

            elif options_button.draw(display):
                game_state = 'options'

            elif play_button.draw(display):
                display.blit(ingame_background, (0,0))
                display_score()
                display_level_atual(nivel)
                update_and_draw()
                pygame.display.update()

                pygame.time.delay(1500)
                game_state = 'playing'

            elif credits_button.draw(display):
                game_state = 'credits'

        case 'scoreboard':
            tocar_musica() # não precisa comentar a função tocar_musica()
            display.blit(score_board_background, (0, 0))

            with open('scoreboard.txt', 'r') as arquivo:  # Modo 'a' adiciona ao final do arquivo
                lista_argumentos = [linha.strip() for linha in arquivo.readlines()] # Lista que armazena o conteudo do arquivo
                numero_argumentos = len(lista_argumentos)  # Conta o número de linhas/argumentos
            show_names_scores(lista_argumentos, numero_argumentos)

            if back_to_menu_button.draw(display):
                game_state = 'menu'      

        case 'options':
            display.blit(options_background, (0, 0))

            options()
            if back_to_menu_button.draw(display):
                game_state = 'menu'
            
        case 'ps_options':
            # pause screen options
            options()
            
            if back_to_game_button.draw(display):
                game_state = 'playing'
                pause_screen = 'false'

            # if back_to_menu_button.draw(display):
            #     game_state = 'menu'
            #     pause_screen = 'false'

        case 'credits':
            display.blit(credits_background, (0, 0))

            if back_to_menu_button.draw(display):
                game_state = 'menu'

        case 'playing':
            if not invader_group:
                nivel += 1
                lifes_left += 1 if lifes_left < 5 else 0
                display.blit(ingame_background, (0, 0))
                display_level_atual(nivel)
                game_state = 'transition'
                update_and_draw()
                display_score()
                pygame.display.update()
                
                pygame.time.delay(1500)
                game_state = 'playing'
                reset_game()
                
            pygame.mixer_music.stop()
            if lifes_left <= 0:
                game_state = 'game_over'
                som_gover.play()
            else:
                display.blit(ingame_background, (0, 0))
                display_score()

                for i in range(lifes_left):
                    display.blit(lifes_left_image, (coordinate_x_lifes - (i*40), 0))

                if pause_screen:
                    pause_menu()
                else:
                    update_and_draw()
                    check_invader_position()
                    collisions()

        case 'game_over':
            display.blit(game_over_background, (0, 0))

  
            if not registrou:
                registrou = registrar_score()

            if play_again_game_over_button.draw(display):
                reset_game()
                game_state = 'playing'
            
            elif back_to_menu_game_over_button.draw(display):
                reset_game()
                game_state = 'menu'
                
            elif scoreboard_game_over_button.draw(display):
                reset_game()
                game_state = 'scoreboard'
            
            elif exit_game_game_over_button.draw(display):
                pygame.quit()
                exit()

    
    pygame.display.update()
