@namespace
class SpriteKind:
    Pet = SpriteKind.create()
    cursor = SpriteKind.create()
# takes a string converts it to fully uppercase
def to_uppercase(text: str):
    global result, lowercase, uppercase
    result = ""
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for char in text:
        found = False
        i = 0
        while i <= len(lowercase) - 1:
            if char == lowercase[i]:
                # Check if char is lowercase
                result = "" + result + uppercase[i]
                # Convert to uppercase
                found = True
                break
            i += 1
        if not (found):
            result = "" + result + char
    # Keep numbers & symbols unchanged
    return result
def takeHealth(x: number):
    global petHealth, roundsSurvived
    petHealth = max(0, petHealth - x)
    game.show_long_text("-" + ("" + str(x)) + " health", DialogLayout.BOTTOM)
    roundsSurvived += 1
    # Increment rounds survived
    gameOver()
# Win condition
def startGame():
    global kitty, yourPet, petHealth
    if spriteNumber == 1:
        kitty = sprites.create(assets.image("""
            kittyPet
        """), SpriteKind.Pet)
        yourPet = sprites.create(assets.image("""
                kittyPetDead
            """),
            SpriteKind.projectile)
        yourPet.set_position(-100, -100)
    elif spriteNumber == 2:
        kitty = sprites.create(assets.image("""
            pigeonPet
        """), SpriteKind.Pet)
        yourPet = sprites.create(assets.image("""
                pigeonPetDead
            """),
            SpriteKind.projectile)
        yourPet.set_position(-100, -100)
    else:
        kitty = sprites.create(assets.image("""
            puppyPet
        """), SpriteKind.Pet)
        yourPet = sprites.create(assets.image("""
                puppyPetDead
            """),
            SpriteKind.projectile)
        yourPet.set_position(-100, -100)
    game.show_long_text("Choose the right prompt to keep your pet alive!",
        DialogLayout.BOTTOM)
    petHealth = 50
    carProb()
    raccoonProb()
    checkUp()
def clearSprites():
    sprites.destroy_all_sprites_of_kind(SpriteKind.Pet)
    sprites.destroy_all_sprites_of_kind(SpriteKind.cursor)
def checkUp():
    global response, money, roundsSurvived
    game.show_long_text("Your pet needs to be vaccinated!", DialogLayout.BOTTOM)
    game.show_long_text("Should you have A) Wellness or B) Comprehensive",
        DialogLayout.BOTTOM)
    response = game.ask_for_string("Enter your choice:")
    if to_uppercase(response) == "A":
        game.show_long_text("Correct! Your pet got vaccinated AND they did a full general check-up because you're insured!",
            DialogLayout.BOTTOM)
        bonus_money = randint(200, 350)
        money = min(1000, money + bonus_money)
        game.show_long_text("+" + ("" + str(bonus_money)) + " money",
            DialogLayout.BOTTOM)
        addPetHealth(randint(5, 10))
    else:
        game.show_long_text("Yeah, this works and all, but your monthly premium's pretty high and it would've been cheaper out of pocket.",
            DialogLayout.BOTTOM)
        penalty_money = randint(200, 350)
        money = max(0, money - penalty_money)
        game.show_long_text("-" + ("" + str(penalty_money)) + " money",
            DialogLayout.BOTTOM)
        roundsSurvived += 1
        gameOver()
# Prevent health from exceeding 100
def addPetHealth(x2: number):
    global petHealth, roundsSurvived
    petHealth = min(100, petHealth + x2)
    game.show_long_text("+" + ("" + str(x2)) + " health", DialogLayout.BOTTOM)
    roundsSurvived += 1
    # Increment rounds survived
    gameOver()
def choose_your_fighter():
    global kitty, pigeon, puppy, arrow
    kitty = sprites.create(assets.image("""
        kittyPet
    """), SpriteKind.Pet)
    pigeon = sprites.create(assets.image("""
        pigeonPet
    """), SpriteKind.Pet)
    puppy = sprites.create(assets.image("""
        puppyPet
    """), SpriteKind.Pet)
    kitty.set_position(20, 70)
    pigeon.set_position(70, 60)
    puppy.set_position(120, 70)
    arrow = sprites.create(assets.image("""
        arrow
    """), SpriteKind.cursor)
    controller.move_sprite(arrow, 100, 100)
    arrow.set_position(60, 20)
# Check if the game should end
def gameOver():
    if petHealth <= 0:
        game.show_long_text("Game Over! Your pet has fainted.", DialogLayout.TOP)
        game.set_game_over_playable(False, music.melody_playable(music.wawawawaa), False)
        game.over(False)
    elif money <= 0:
        game.show_long_text("Game Over! You ran out of money!", DialogLayout.TOP)
        game.set_game_over_playable(False, music.melody_playable(music.wawawawaa), False)
        game.over(False)
    elif roundsSurvived >= 3:
        game.show_long_text("Congratulations! You survived three rounds!",
            DialogLayout.TOP)
        game.set_game_over_playable(True, music.melody_playable(music.power_up), False)
        game.over(True)
def carProb():
    global car, response, money
    music.play(music.create_sound_effect(WaveShape.SQUARE,
            200,
            1,
            255,
            255,
            250,
            SoundExpressionEffect.NONE,
            InterpolationCurve.CURVE),
        music.PlaybackMode.UNTIL_DONE)
    car = sprites.create(assets.image("""
        car
    """), SpriteKind.enemy)
    car.set_position(74, 54)
    game.show_long_text("Oh no! Your pet got hit by a car! The Surgery costs $1500",
        DialogLayout.BOTTOM)
    game.show_long_text("Should you have gotten A) Comprehensive or B) Accident",
        DialogLayout.BOTTOM)
    response = game.ask_for_string("Enter your choice:")
    # sets response to uppercase
    if to_uppercase(response) == "A":
        game.show_long_text("Correct! Comprehensive allowed for you to afford both the surgery and the pain medication afterward!",
            DialogLayout.BOTTOM)
        addPetHealth(randint(5, 10))
    else:
        game.show_long_text("Incorrect! The surgery was paid for, but you couldn't afford the pain medication afterwards since Accident doesn't cover ailments you pet lost some health!",
            DialogLayout.BOTTOM)
        money = min(0, money - randint(200, 350))
        game.show_long_text("-" + ("" + str(money)) + " money", DialogLayout.BOTTOM)
        takeHealth(randint(20, 40))
    sprites.destroy(car)
def raccoonProb():
    global response, roundsSurvived, car, money
    game.show_long_text("Your pet wants to go outside! (Unsupervised)",
        DialogLayout.BOTTOM)
    game.show_long_text("Let them out (A) or keep them in (B)", DialogLayout.BOTTOM)
    response = to_uppercase(game.ask_for_string("Enter your choice:"))
    # sets response to uppercase
    if response == "B":
        game.show_long_text("Good job lol (nothing else happens)", DialogLayout.BOTTOM)
        roundsSurvived += 1
        return
    elif response == "A":
        # Exits function early, so the rest doesn't run
        car = sprites.create(assets.image("""
            sharkAttack
        """), SpriteKind.enemy)
        car.set_position(95, 59)
        game.show_long_text("Oh no! Your pet got attacked by a raccoon! Gotta take a vet visit!",
            DialogLayout.BOTTOM)
        money = max(0, money - randint(200, 350))
        game.show_long_text("-" + ("" + str(money)) + " money", DialogLayout.BOTTOM)
        takeHealth(randint(20, 40))
        sprites.destroy(car)
# Only destroys the sprite if it was created

def on_on_overlap(sprite, otherSprite):
    global spriteNumber
    if otherSprite == kitty:
        spriteNumber = 1
        game.splash("You Chose Kitty!")
    elif otherSprite == pigeon:
        spriteNumber = 2
        game.splash("You Chose Pigeon!")
    else:
        spriteNumber = 3
        game.splash("You Chose Puppy!")
    clearSprites()
    startGame()
sprites.on_overlap(SpriteKind.cursor, SpriteKind.Pet, on_on_overlap)

car: Sprite = None
arrow: Sprite = None
puppy: Sprite = None
pigeon: Sprite = None
response = ""
yourPet: Sprite = None
kitty: Sprite = None
spriteNumber = 0
roundsSurvived = 0
petHealth = 0
uppercase = ""
lowercase = ""
result = ""
money = 0
# amount of money that a person has
money = 1000
music.play(music.string_playable("C5 B A B A G A G ", 120),
    music.PlaybackMode.LOOPING_IN_BACKGROUND)
game.splash("INSURE-A-PET")
scene.set_background_image(assets.image("""
    myImage
"""))
game.show_long_text("Choose your pet!", DialogLayout.BOTTOM)
choose_your_fighter()