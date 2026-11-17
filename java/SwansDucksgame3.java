//the game checklist, random number:CHECK, 1 indentify player has one: CHECK, calculate the number of guesses: CHECK, scanner input:CHECK
//informing user of malformed guesses: I programmed the game that if you have less than 4 numbers or have double numbers that the game ask again,
//if it is malformed the game won't show the number of Swans and Ducks, that is how you can see when it is malformed:CHECK
//correct amount of swans and ducks: CHECK


import java.util.InputMismatchException;
		import java.util.Random;
		import java.util.Scanner;
		//We have imported 3 (librarys) that we need to use different functions in the code down below 
public class SwansDucksgame3 {
public static void main(String[] args){
				Random gen= new Random();
				int target;
				//generates a random number
				while(hasDupes(target= (gen.nextInt(9000) + 1000)));
				//the number has to be 4 digits so the number must be between 1000 and 9999
				String targetStr = target +"";
				boolean guessed = false;
				Scanner input = new Scanner(System.in);
				//creates a field for the player of this game to insert his own number
				int guesses = 0;
				//the guesses start at zero
				do{
					int Swans = 0;
					int Ducks = 0;
					System.out.print("Guess a 4-digit number with no duplicate digits: ");
					//tells the player what to do
					int guess;
					try{
						guess = input.nextInt();
						if(hasDupes(guess) || guess < 1000) continue;
						//checks if the guess is malformed
						
					}catch(InputMismatchException e){
						continue;
					}
					guesses++;
					//ads one to the total number of guesses
					String guessStr = guess + "";
					for(int i= 0;i < 4;i++){
						if(guessStr.charAt(i) == targetStr.charAt(i)){
							Swans++;
							//ads a number to the swans if the number is in the correct place
						}else if(targetStr.contains(guessStr.charAt(i)+"")){
							Ducks++;
							//ads a number to the ducks if the number is not in the correct place but is in the 4numbers
						}
					}
					if(Swans == 4){
						guessed = true;
					}else{
						System.out.println(Ducks+" Ducks and "+Swans+" Swans.");
					}
					//if you dont have 4 swans it will write down the number of swans and ducks you have
				}while(!guessed);
				System.out.println("You won after "+guesses+" guesses!");
				//if you have 4 Swans you automatically win the game, it gives you the total number of guesses you used in the entire game
			}
		 
			public static boolean hasDupes(int num){
				boolean[] digs = new boolean[10];
				while(num > 0){
					if(digs[num%10]) return true;
					digs[num%10] = true;
					num/= 10;
					//checks if the number in malformed
				}
				return false;
			}

	}
