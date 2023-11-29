import pygame
import sys
import time
from src.Player import Player, RandomBot, MinimaxBot, Bot
from src.constants import Symbol, symbol_to_string, Gamemode
from src.TicTacToe import TicTacToe, Move

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

smallFont = pygame.font.Font("src/OpenSans-Regular.ttf", 20)
mediumFont = pygame.font.Font("src/OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("src/OpenSans-Regular.ttf", 35)
moveFont = pygame.font.Font("src/OpenSans-Regular.ttf", 60)

player_1 = None
gamemode = Gamemode.NONE

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    if gamemode == Gamemode.NONE:

        # Draw title
        title = largeFont.render("Choose gamemode", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        pvb_button = pygame.Rect((width / 16), (height / 2), width / 3, 50)
        pvb = smallFont.render("Minimax vs Player", True, black)
        pvb_rect = pvb.get_rect()
        pvb_rect.center = pvb_button.center
        pygame.draw.rect(screen, white, pvb_button)
        screen.blit(pvb, pvb_rect)

        bvb_button = pygame.Rect(5 * (width / 8), (height / 2), width / 3, 50)
        bvb = smallFont.render("Minimax vs Random", True, black)
        bvb_rect = bvb.get_rect()
        bvb_rect.center = bvb_button.center
        pygame.draw.rect(screen, white, bvb_button)
        screen.blit(bvb, bvb_rect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if pvb_button.collidepoint(mouse):
                time.sleep(0.2)
                gamemode = Gamemode.PVB
            elif bvb_button.collidepoint(mouse):
                time.sleep(0.2)
                gamemode = Gamemode.BVB


    # Let user choose a player.
    elif player_1 is None:
        # Draw title
        title_string = "Choose symbol for minimax bot" if gamemode == Gamemode.BVB else "Pick your symbol"
        title = largeFont.render(title_string, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                player_1 = Player(Symbol.CROSS) if gamemode == Gamemode.PVB else MinimaxBot(Symbol.CROSS)
                player_2 = MinimaxBot(Symbol.CIRCLE) if gamemode == Gamemode.PVB else RandomBot(Symbol.CIRCLE)
                game = TicTacToe(players=(player_1, player_2))

            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                player_1 = Player(Symbol.CIRCLE) if gamemode == Gamemode.PVB else MinimaxBot(Symbol.CIRCLE)
                player_2 = MinimaxBot(Symbol.CROSS) if gamemode == Gamemode.PVB else RandomBot(Symbol.CROSS)
                game = TicTacToe(players=(player_1, player_2))

    else:
        # Draw game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)

                if not game.board.is_empty((i, j)):
                    move = moveFont.render(symbol_to_string(game.board[i][j]), True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = game.board.game_over()

        # Show title
        if game_over:
            winner = game.board.winner()
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {symbol_to_string(winner)} wins."
        elif game.turn == player_1.symbol:
            title = f"{symbol_to_string(player_1.symbol)}\'s turn"
        else:
            title = f"{symbol_to_string(player_2.symbol)}\'s turn"

        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        player_to_move = player_1 if game.turn == player_1.symbol else player_2
        if isinstance(player_to_move, Bot) and not game_over:
            time.sleep(.5)
            game.make_move(player_to_move.make_move(game.board))

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and not (isinstance(player_to_move, Bot) or game_over):
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if game.board.is_empty((i, j)) and tiles[i][j].collidepoint(mouse):
                        player_move = Move((i, j), game.turn)
                        game.make_move(player_move)

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    player_1 = None
                    player_2 = None
                    gamemode = Gamemode.NONE

    pygame.display.flip()
