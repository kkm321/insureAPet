namespace SpriteKind {
    export const Pet = SpriteKind.create()
    export const cursor = SpriteKind.create()
}
// takes a string converts it to fully uppercase
function to_uppercase (text: string) {
    let found: boolean;
let i: number;
result = ""
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for (let char of text) {
        found = false
        i = 0
        while (i <= lowercase.length - 1) {
            if (char == lowercase[i]) {
                // Check if char is lowercase
                result = "" + result + uppercase[i]
                // Convert to uppercase
                found = true
                break;
            }
            i += 1
        }
        if (!(found)) {
            result = "" + result + char
        }
    }
    // Keep numbers & symbols unchanged
    return result
}
function takeHealth (x: number) {
    petHealth = Math.max(0, petHealth - x)
    game.showLongText("-" + ("" + x) + " health", DialogLayout.Bottom)
    roundsSurvived += 1
    // Increment rounds survived
    gameOver()
}
// Win condition
function startGame () {
    if (spriteNumber == 1) {
        kitty = sprites.create(assets.image`kittyPet`, SpriteKind.Pet)
        yourPet = sprites.create(assets.image`kittyPetDead`, SpriteKind.Projectile)
        yourPet.setPosition(-100, -100)
    } else if (spriteNumber == 2) {
        kitty = sprites.create(assets.image`pigeonPet`, SpriteKind.Pet)
        yourPet = sprites.create(assets.image`pigeonPetDead`, SpriteKind.Projectile)
        yourPet.setPosition(-100, -100)
    } else {
        kitty = sprites.create(assets.image`puppyPet`, SpriteKind.Pet)
        yourPet = sprites.create(assets.image`puppyPetDead`, SpriteKind.Projectile)
        yourPet.setPosition(-100, -100)
    }
    game.showLongText("Choose the right prompt to keep your pet alive!", DialogLayout.Bottom)
    petHealth = 50
    carProb()
    raccoonProb()
    checkUp()
}
function clearSprites () {
    sprites.destroyAllSpritesOfKind(SpriteKind.Pet)
    sprites.destroyAllSpritesOfKind(SpriteKind.cursor)
}
function checkUp () {
    let bonus_money: number;
let penalty_money: number;
game.showLongText("Your pet needs to be vaccinated!", DialogLayout.Bottom)
    game.showLongText("Should you have A) Wellness or B) Comprehensive", DialogLayout.Bottom)
    response = game.askForString("Enter your choice:")
    if (to_uppercase(response) == "A") {
        game.showLongText("Correct! Your pet got vaccinated AND they did a full general check-up because you're insured!", DialogLayout.Bottom)
        bonus_money = randint(200, 350)
        money = Math.min(1000, money + bonus_money)
        game.showLongText("+" + ("" + bonus_money) + " money", DialogLayout.Bottom)
        addPetHealth(randint(5, 10))
    } else {
        game.showLongText("Yeah, this works and all, but your monthly premium's pretty high and it would've been cheaper out of pocket.", DialogLayout.Bottom)
        penalty_money = randint(200, 350)
        money = Math.max(0, money - penalty_money)
        game.showLongText("-" + ("" + penalty_money) + " money", DialogLayout.Bottom)
        roundsSurvived += 1
        gameOver()
    }
}
// Prevent health from exceeding 100
function addPetHealth (x2: number) {
    petHealth = Math.min(100, petHealth + x2)
    game.showLongText("+" + ("" + x2) + " health", DialogLayout.Bottom)
    roundsSurvived += 1
    // Increment rounds survived
    gameOver()
}
function choose_your_fighter () {
    kitty = sprites.create(assets.image`kittyPet`, SpriteKind.Pet)
    pigeon = sprites.create(assets.image`pigeonPet`, SpriteKind.Pet)
    puppy = sprites.create(assets.image`puppyPet`, SpriteKind.Pet)
    kitty.setPosition(20, 70)
    pigeon.setPosition(70, 60)
    puppy.setPosition(120, 70)
    arrow = sprites.create(assets.image`arrow`, SpriteKind.cursor)
    controller.moveSprite(arrow, 100, 100)
    arrow.setPosition(60, 20)
}
// Check if the game should end
function gameOver () {
    if (petHealth <= 0) {
        game.showLongText("Game Over! Your pet has fainted.", DialogLayout.Top)
        game.setGameOverPlayable(false, music.melodyPlayable(music.wawawawaa), false)
        game.over(false)
    } else if (money <= 0) {
        game.showLongText("Game Over! You ran out of money!", DialogLayout.Top)
        game.setGameOverPlayable(false, music.melodyPlayable(music.wawawawaa), false)
        game.over(false)
    } else if (roundsSurvived >= 3) {
        game.showLongText("Congratulations! You survived three rounds!", DialogLayout.Top)
        game.setGameOverPlayable(true, music.melodyPlayable(music.powerUp), false)
        game.over(true)
    }
}
function carProb () {
    music.play(music.createSoundEffect(WaveShape.Square, 200, 1, 255, 255, 250, SoundExpressionEffect.None, InterpolationCurve.Curve), music.PlaybackMode.UntilDone)
    car = sprites.create(assets.image`car`, SpriteKind.Enemy)
    car.setPosition(74, 54)
    game.showLongText("Oh no! Your pet got hit by a car! The Surgery costs $1500", DialogLayout.Bottom)
    game.showLongText("Should you have gotten A) Comprehensive or B) Accident", DialogLayout.Bottom)
    response = game.askForString("Enter your choice:")
    // sets response to uppercase
    if (to_uppercase(response) == "A") {
        game.showLongText("Correct! Comprehensive allowed for you to afford both the surgery and the pain medication afterward!", DialogLayout.Bottom)
        addPetHealth(randint(20, 30))
    } else {
        game.showLongText("Incorrect! The surgery was paid for, but you couldn't afford the pain medication afterwards since Accident doesn't cover ailments you pet lost some health!", DialogLayout.Bottom)
        money = Math.max(0, money - randint(200, 350))
        game.showLongText("-" + ("" + money) + " money", DialogLayout.Bottom)
        takeHealth(randint(20, 30))
    }
    sprites.destroy(car)
}
function raccoonProb () {
    game.showLongText("Your pet wants to go outside! (Unsupervised)", DialogLayout.Bottom)
    game.showLongText("Let them out (A) or keep them in (B)", DialogLayout.Bottom)
    response = to_uppercase(game.askForString("Enter your choice:"))
    // sets response to uppercase
    if (response == "B") {
        game.showLongText("Good job lol (nothing else happens)", DialogLayout.Bottom)
        roundsSurvived += 1
        return
    } else if (response == "A") {
        // Exits function early, so the rest doesn't run
        car = sprites.create(assets.image`sharkAttack`, SpriteKind.Enemy)
        car.setPosition(95, 59)
        game.showLongText("Oh no! Your pet got attacked by a raccoon! Gotta take a vet visit!", DialogLayout.Bottom)
        money = Math.max(0, money - randint(200, 350))
        game.showLongText("-" + ("" + money) + " money", DialogLayout.Bottom)
        takeHealth(randint(20, 30))
        sprites.destroy(car)
    }
}
// Only destroys the sprite if it was created
sprites.onOverlap(SpriteKind.cursor, SpriteKind.Pet, function (sprite, otherSprite) {
    if (otherSprite == kitty) {
        spriteNumber = 1
        game.splash("You Chose Kitty!")
    } else if (otherSprite == pigeon) {
        spriteNumber = 2
        game.splash("You Chose Pigeon!")
    } else {
        spriteNumber = 3
        game.splash("You Chose Puppy!")
    }
    clearSprites()
    startGame()
})
let car: Sprite = null
let arrow: Sprite = null
let puppy: Sprite = null
let pigeon: Sprite = null
let response = ""
let yourPet: Sprite = null
let kitty: Sprite = null
let spriteNumber = 0
let roundsSurvived = 0
let petHealth = 0
let uppercase = ""
let lowercase = ""
let result = ""
let money = 0
// amount of money that a person has
money = 1000
game.splash("INSURE-A-PET")
scene.setBackgroundImage(assets.image`myImage`)
music.play(music.stringPlayable("C5 B A B A G A G ", 120), music.PlaybackMode.UntilDone)
game.showLongText("Choose your pet!", DialogLayout.Bottom)
choose_your_fighter()
